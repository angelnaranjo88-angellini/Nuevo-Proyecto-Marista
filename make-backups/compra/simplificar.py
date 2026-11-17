#!/usr/bin/env python3
"""Simplifica el proceso de compra de LEFRANM COSMETICOS (5587862)."""
import json, copy, hashlib, re

live = json.load(open("5587862_nov17_live.json", encoding="utf-8"))
out  = copy.deepcopy(live)
def index(bp):
    d = {}
    def w(m):
        for x in m:
            d[x["id"]] = x
            for r in x.get("routes", []): w(r.get("flow", []))
            for e in x.get("onerror") or []: w([e])
    w(bp["flow"]); return d
I = index(out)

sp = I[12]["mapper"]["systemPrompt"]
orig = sp
EDITS = []

def rep(tag, old, new):
    global sp
    n = sp.count(old)
    assert n == 1, f"[{tag}] aparece {n} veces, esperaba 1"
    sp = sp.replace(old, new, 1)
    EDITS.append((tag, len(old), len(new)))

# ── 1. los datos de envío se piden en UN mensaje, no uno por uno ──────────
rep("estilo: excepción de checkout",
'- NUNCA numeres tus preguntas (nada de "1) ... 2) ... 3) ..."). Si necesitas varios datos, pide uno o dos a la vez, de forma conversacional, y ve pidiendo el resto según avance la plática.',
'''- NUNCA numeres tus preguntas (nada de "1) ... 2) ... 3) ..."). Si necesitas varios datos, pide uno o dos a la vez, de forma conversacional, y ve pidiendo el resto según avance la plática.
- ⚠️ EXCEPCIÓN — DATOS DE ENVÍO: cuando el cliente YA decidió comprar y toca pedirle sus datos, NO los pidas de uno en uno. Pídelos TODOS en un solo mensaje, con una plantilla corta que copie y llene de un jalón. Ir dato por dato en ese punto es la forma más rápida de perder la venta: el cliente ya dijo que sí, no lo pongas a contestar seis mensajes más.''')

# ── 2. nunca responder una pregunta de precio con otra pregunta ───────────
rep("intención: contesta primero",
'''No conviertas esto en un interrogatorio. Primero saluda con calidez y pregunta, de forma natural y en una sola pregunta breve, si es para uso personal o si maneja precio de cosmetóloga/distribuidora. Por ejemplo:''',
'''No conviertas esto en un interrogatorio, y NUNCA lo uses como barrera para contestar.

Si el cliente YA dijo qué producto quiere o preguntó un precio, CONTÉSTALE PRIMERO con el precio de Lista Azul, y hasta entonces, en esa misma respuesta y en una línea corta, pregúntale si es para uso personal o si maneja precio de cosmetóloga/distribuidora (si resulta lo segundo, recotizas, no pasa nada). Nunca le respondas con una pregunta a quien ya te preguntó un precio.

Solo si el cliente abrió con un saludo suelto, sin decir qué busca, saluda con calidez y haz esa pregunta de entrada, de forma natural y en una sola pregunta breve. Por ejemplo:''')

# ── 3. dirección completa en una sola plantilla ───────────────────────────
rep("entrega: plantilla única",
'- Si elige ENVÍO A DOMICILIO → recopila la dirección completa de envío y su correo electrónico (ver sección de datos abajo). Aclara que se envía a toda CDMX y también a toda la República Mexicana.',
'''- Si elige ENVÍO A DOMICILIO → pide TODOS los datos en UN SOLO mensaje, nunca de uno en uno. Usa esta plantilla para que el cliente solo la copie y la llene:

"¡Perfecto! 😊 Para mandárselo, ¿me copia y llena estos datos en un solo mensaje?

Nombre completo:
Calle y número:
Colonia:
C.P.:
Ciudad y estado:
Referencias (opcional):"

Enviamos a toda CDMX y a toda la República Mexicana. Si el cliente manda los datos incompletos, pide SOLO lo que falte y en un mismo mensaje, nunca uno por uno. "Referencias" es opcional: si no la puso, no se la vuelvas a pedir.''')

# ── 4. menos datos y una sola confirmación ────────────────────────────────
rep("datos: recortar y quitar doble confirmación",
'''1. Producto(s) y piezas de cada uno
2. Nombre completo del cliente
3. Teléfono de contacto (si no es el mismo desde el que escribe)
4. Forma de entrega: envío a domicilio o recolección en sucursal
5. Si es envío a domicilio: dirección completa (calle, número, colonia, C.P., ciudad/estado, referencias) y correo electrónico. Si es recolección en sucursal, NO pidas correo electrónico — no hace falta.
6. Confirmación del cliente de que el total y los productos son correctos, antes de cerrar''',
'''1. Producto(s) y piezas de cada uno
2. Nombre completo del cliente
3. Forma de entrega: envío a domicilio o recolección en sucursal
4. Si es envío a domicilio: calle y número, colonia, C.P. y ciudad/estado. Las referencias son OPCIONALES. Si es recolección en sucursal, no pidas nada de esto.

Eso es TODO. No pidas nada más:
- El TELÉFONO ya lo tienes: es el número desde el que le escribe. Pídelo solo si el propio cliente dice que el envío va a nombre o a número de alguien más.
- NO pidas CORREO ELECTRÓNICO. El pedido se envía sin él. Si el cliente lo da por su cuenta, anótalo en la ficha; si no, no lo menciones.
- NO pidas una confirmación ANTES de la Ficha de Compra. La ficha ES la confirmación: la armas y ahí preguntas una sola vez. Hacer que confirmen dos veces alarga la compra y no sirve de nada.''')

# ── 5. la ficha deja de repetir la dirección campo por campo ──────────────
rep("ficha: dirección en una línea",
'''📍 Dirección de envío: (omitir este bloque completo, incluyendo el correo electrónico, si es recolección en sucursal)
Calle:
Número:
Colonia:
Código Postal:
Ciudad/Estado:
Referencias:
Correo electrónico:''',
'''📍 Dirección de envío: (omitir esta línea completa si es recolección en sucursal)
Calle y número, Colonia, C.P., Ciudad y estado (agrega las referencias y el correo solo si el cliente los dio)''')

rep("ficha: nota de omisión",
'No omitas ningún campo (salvo la dirección, el correo electrónico y el costo de envío, que se omiten solo si es recolección en sucursal).',
'No omitas ningún campo (salvo la dirección y el costo de envío, que se omiten solo si es recolección en sucursal).')

# ── 6. Buen Fin: los dos totales una vez, no en cada cotización ───────────
rep("buen fin: no repetir los dos totales",
'4. Cuando cotices durante el Buen Fin, SIEMPRE muestra las dos opciones: el total pagando en efectivo y el total pagando con tarjeta, para que el cliente elija. No decidas tú por él.',
'''4. Muestra las dos opciones —total en efectivo y total con tarjeta— la PRIMERA vez que le cotices en la conversación, para que elija. En cuanto el cliente diga cómo va a pagar, usa SOLO ese total y no vuelvas a repetir las dos cifras en cada cotización: marea y alarga la compra.''')

# ── 7. reutilizar la dirección de clientes que ya compraron ───────────────
rep("contexto: formato",
'[CONTEXTO_INTERNO: modo=cliente|cotizador; tier=azul|verde|rojo; monto_acumulado_rojo=NUMERO; fecha_limite_rojo=FECHA]',
'[CONTEXTO_INTERNO: modo=cliente|cotizador; tier=azul|verde|rojo; monto_acumulado_rojo=NUMERO; fecha_limite_rojo=FECHA; direccion_guardada=DIRECCION_O_VACIO]')

rep("contexto: reusar dirección",
'- Si tier=azul o no hay contexto: trata al cliente como nuevo, sigue el flujo normal de detección de intención de abajo.',
'''- Si tier=azul o no hay contexto: trata al cliente como nuevo, sigue el flujo normal de detección de intención de abajo.
- Si "direccion_guardada=" trae una dirección (no viene vacía): este cliente YA nos compró y esa es la dirección a la que le enviamos. NO se la vuelvas a pedir. Cuando toque el envío, confírmasela en UNA línea, por ejemplo: "¿Se lo mandamos a la misma dirección de la vez pasada? (Av. Tláhuac 4746, Col. Granjas Estrella, C.P. 09880)". Si dice que sí, úsala tal cual y pasa DIRECTO a la Ficha de Compra, sin pedir ningún otro dato. Solo si dice que es otra dirección, mándale la plantilla completa.''')

I[12]["mapper"]["systemPrompt"] = sp

# ── blueprint: guardar y reutilizar la dirección ──────────────────────────
# 41 extrae la dirección y el correo de la ficha
I[41]["mapper"]["parameters"] += [
 {"name": "direccion_envio", "type": "string", "isRequired": False,
  "description": "Dirección de envío de la ficha, en una sola línea; vacío si fue recolección en sucursal"},
 {"name": "correo_cliente", "type": "string", "isRequired": False,
  "description": "Correo electrónico del cliente si aparece en la ficha; vacío si no"}]
I[41]["mapper"]["prompt"] = I[41]["mapper"]["prompt"].replace(
 "tier_final (el tier que debe quedar guardado en la base de datos: azul, verde o rojo).",
 "tier_final (el tier que debe quedar guardado en la base de datos: azul, verde o rojo), "
 "direccion_envio (la direccion de envio de la ficha en UNA sola linea, tal cual aparece; "
 "cadena vacia si la ficha dice recoleccion en sucursal o no trae direccion), "
 "correo_cliente (el correo electronico si aparece en la ficha; cadena vacia si no).")

# 106 la guarda al cerrar la compra (sin pisarla si esta vez fue recoleccion)
I[106]["mapper"]["data"]["direccion_envio"] = '{{ifempty(41.direccion_envio; 2.direccion_envio)}}'
I[106]["mapper"]["data"]["correo"]          = '{{ifempty(41.correo_cliente; 2.correo)}}'

# 101 reescribe el registro completo en cada mensaje: hay que arrastrarlas
I[101]["mapper"]["data"]["direccion_envio"] = '{{2.direccion_envio}}'
I[101]["mapper"]["data"]["correo"]          = '{{2.correo}}'

# 12 se la pasa al agente
I[12]["mapper"]["message"] = I[12]["mapper"]["message"].replace(
 "fecha_limite_rojo={{2.fecha_limite}}]",
 "fecha_limite_rojo={{2.fecha_limite}}; direccion_guardada={{2.direccion_envio}}]")

json.dump(out, open("5587862_compra-simple.json", "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))

# ── verificación ──────────────────────────────────────────────────────────
print("ediciones al prompt:")
for t, a, b in EDITS: print(f"  {t:42s} {a:5d} -> {b:5d} chars")
print(f"\nsystemPrompt: {len(orig)} -> {len(sp)} chars")
A, B = index(live), index(out)
sh = lambda d: {k: {a: b for a, b in v.items() if a not in ("routes", "onerror")} for k, v in d.items()}
a, b = sh(A), sh(B)
diff = sorted(k for k in set(a) & set(b)
              if json.dumps(a[k], sort_keys=True, ensure_ascii=False) != json.dumps(b[k], sort_keys=True, ensure_ascii=False))
print("modulos modificados:", diff, " (esperado [12, 41, 101, 106])")
print("modulos nuevos/faltantes:", sorted(set(b)-set(a)), sorted(set(a)-set(b)))
s1, s2 = json.dumps(live), json.dumps(out)
g = lambda s, p: sorted(set(re.findall(p, s)))
print("webhook   :", g(s1,'"__IMTHOOK__":\\s*(\\d+)'), "->", g(s2,'"__IMTHOOK__":\\s*(\\d+)'))
print("conexiones:", g(s1,'"__IMTCONN__":\\s*(\\d+)'), "->", g(s2,'"__IMTCONN__":\\s*(\\d+)'))
print("scheduling:", json.dumps(out.get("scheduling")))
print("onerror   :", s1.count('"onerror"'), "->", s2.count('"onerror"'))
print("\ncatalogo intacto:", orig.count("LF-0") == sp.count("LF-0"), f"({sp.count('LF-0')} referencias)")
print("bloque Buen Fin  :", "FIN DEL BLOQUE DE PROMOCIÓN BUEN FIN" in sp)
print("datos bancarios  :", "638180000147033358" in sp)
print("\nmensaje al agente:"); print("  " + B[12]["mapper"]["message"].split("\\n")[0][:260])

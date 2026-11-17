#!/usr/bin/env python3
"""Regresa el correo electronico al flujo, dentro de la misma plantilla."""
import json, copy, difflib

src = json.load(open("5587862_compra-simple.json", encoding="utf-8"))
out = copy.deepcopy(src)
def index(bp):
    d = {}
    def w(m):
        for x in m:
            d[x["id"]] = x
            for r in x.get("routes", []): w(r.get("flow", []))
            for e in x.get("onerror") or []: w([e])
    w(bp["flow"]); return d
I = index(out)
sp = I[12]["mapper"]["systemPrompt"]; before = sp
E = []
def rep(tag, old, new):
    global sp
    assert sp.count(old) == 1, f"[{tag}] aparece {sp.count(old)} veces"
    sp = sp.replace(old, new, 1); E.append(tag)

# 1) el correo entra en la MISMA plantilla, no en un mensaje aparte
rep("plantilla: agregar correo",
'''Ciudad y estado:
Referencias (opcional):"''',
'''Ciudad y estado:
Correo electrónico:
Referencias (opcional):"''')

# 2) vuelve a ser obligatorio, pero solo en envío a domicilio
rep("datos: correo obligatorio en envío",
'''4. Si es envío a domicilio: calle y número, colonia, C.P. y ciudad/estado. Las referencias son OPCIONALES. Si es recolección en sucursal, no pidas nada de esto.''',
'''4. Si es envío a domicilio: calle y número, colonia, C.P., ciudad/estado y CORREO ELECTRÓNICO. Las referencias son OPCIONALES. Si es recolección en sucursal, no pidas nada de esto (tampoco el correo).''')

rep("datos: nota del correo",
'''- NO pidas CORREO ELECTRÓNICO. El pedido se envía sin él. Si el cliente lo da por su cuenta, anótalo en la ficha; si no, no lo menciones.''',
'''- El CORREO ELECTRÓNICO sí hace falta cuando es envío a domicilio: el equipo lo usa para mandarle los datos de rastreo de su paquete. Pero ya va DENTRO de la plantilla de arriba — nunca lo pidas en un mensaje aparte. Si el cliente lo deja en blanco, pídeselo una sola vez, en una línea, explicando para qué es ("es para mandarle la guía de rastreo"). En recolección en sucursal no lo pidas.''')

# 3) en la ficha, su propia línea para que el dueño lo copie fácil
rep("ficha: línea de correo",
'''📍 Dirección de envío: (omitir esta línea completa si es recolección en sucursal)
Calle y número, Colonia, C.P., Ciudad y estado (agrega las referencias y el correo solo si el cliente los dio)''',
'''📍 Dirección de envío: (omitir esta línea completa si es recolección en sucursal)
Calle y número, Colonia, C.P., Ciudad y estado (agrega las referencias solo si el cliente las dio)

📧 Correo electrónico: (omitir esta línea completa si es recolección en sucursal)
correo@delcliente.com''')

rep("ficha: nota de omisión",
'No omitas ningún campo (salvo la dirección y el costo de envío, que se omiten solo si es recolección en sucursal).',
'No omitas ningún campo (salvo la dirección, el correo electrónico y el costo de envío, que se omiten solo si es recolección en sucursal).')

I[12]["mapper"]["systemPrompt"] = sp
json.dump(out, open("5587862_compra-simple.json", "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))

print("ediciones:", len(E))
for t in E: print("  -", t)
print(f"\nsystemPrompt: {len(before)} -> {len(sp)} chars")
d = list(difflib.unified_diff(before.split("\n"), sp.split("\n"), lineterm="", n=0))
print("bloques de cambio:", len([l for l in d if l.startswith("@@")]))
A, B = index(src), index(out)
sh = lambda x: {k: {a: b for a, b in v.items() if a not in ("routes","onerror")} for k, v in x.items()}
a, b = sh(A), sh(B)
print("modulos modificados:", sorted(k for k in set(a)&set(b)
      if json.dumps(a[k],sort_keys=True,ensure_ascii=False)!=json.dumps(b[k],sort_keys=True,ensure_ascii=False)))
print("\n--- la plantilla como queda ---")
i = sp.find('¿me copia y llena estos datos')
print(sp[i-40:i+230])

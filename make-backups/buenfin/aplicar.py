#!/usr/bin/env python3
"""Inyecta las promociones del Buen Fin y arregla el envio de imagenes.
Uso: python3 aplicar.py ID_PRODUCTOS ID_CONOTERAPIA ID_VENTOSAS ID_PIERNAS ID_DERMAPEN"""
import json, sys, copy, hashlib, re

ids = dict(zip(["PRODUCTOS","CONOTERAPIA","VENTOSAS","PIERNAS","DERMAPEN"], sys.argv[1:6]))
assert len(ids) == 5 and all(ids.values()), "faltan los 5 IDs de Drive"
URL = lambda k: f"https://lh3.googleusercontent.com/d/{ids[k]}=w1000"

def blk(path):
    t = open(path, encoding="utf-8").read()
    for k in ids:
        t = t.replace(f"PLACEHOLDER_{k}", URL(k))
    assert "PLACEHOLDER" not in t
    return t

def index(bp):
    o = {}
    def w(m):
        for x in m:
            o[x["id"]] = x
            for r in x.get("routes", []): w(r.get("flow", []))
            for e in x.get("onerror") or []: w([e])
    w(bp["flow"]); return o

def resume(eid, x, y):
    return [{"id": eid, "module": "builtin:Resume", "version": 1, "mapper": {},
             "metadata": {"designer": {"x": x, "y": y}}}]

def report(tag, before, after):
    A, B = index(before), index(after)
    sh = lambda d: {k: {a: b for a, b in v.items() if a not in ("routes", "onerror")} for k, v in d.items()}
    a, b = sh(A), sh(B)
    diff = sorted(k for k in set(a) & set(b)
                  if json.dumps(a[k], sort_keys=True, ensure_ascii=False) != json.dumps(b[k], sort_keys=True, ensure_ascii=False))
    s1, s2 = json.dumps(before), json.dumps(after)
    g = lambda s, p: sorted(set(re.findall(p, s)))
    print(f"\n===== {tag} =====")
    print("  modulos nuevos      :", sorted(set(b) - set(a)))
    print("  modulos modificados :", diff)
    print("  webhook   ", g(s1,'"__IMTHOOK__":\\s*(\\d+)'), "->", g(s2,'"__IMTHOOK__":\\s*(\\d+)'))
    print("  conexiones", g(s1,'"__IMTCONN__":\\s*(\\d+)'), "->", g(s2,'"__IMTCONN__":\\s*(\\d+)'))
    print("  scheduling", json.dumps(before.get("scheduling")), "->", json.dumps(after.get("scheduling")))
    print("  onerror   ", s1.count('"onerror"'), "->", s2.count('"onerror"'))

# ─────────────────────────── CITAS 5645150 ───────────────────────────
live = json.load(open("5645150_citas_live.json", encoding="utf-8"))
out  = copy.deepcopy(live)
I    = index(out)

# 1) bloque Buen Fin, justo despues del bloque de promos de octubre
sp  = I[3]["mapper"]["systemPrompt"]
mark = "FIN DEL BLOQUE DE PROMOCIONES TEMPORAL"
p = sp.find(mark); assert p > 0, "no encuentro el fin del bloque de octubre"
p = sp.find("\n", sp.find("═══", p))          # final de la linea de cierre
I[3]["mapper"]["systemPrompt"] = sp[:p+1] + blk("buenfin/bloque_citas.txt") + sp[p+1:]

# 2) modulo 17: separa link y texto de verdad (antes decia "texto", el campo se llama "Text")
I[17]["mapper"]["prompt"] = (
 'Eres un clasificador de respuestas de un asistente de WhatsApp de un spa.\n'
 'Vas a recibir el mensaje que generó el asistente como respuesta al cliente.\n\n'
 'Busca en el mensaje una imagen de promoción, que puede venir de dos formas:\n'
 '  a) una línea con la marca exacta [ENVIAR_IMAGEN: URL]\n'
 '  b) un link suelto que empiece con "https://lh3.googleusercontent.com"\n\n'
 'Si encuentras cualquiera de las dos:\n'
 '- Copia esa URL tal cual, completa, sin recortarla ni modificarla, en "link_imagen".\n'
 '- En "Text" pon el resto del mensaje EXACTAMENTE igual pero quitando la marca o el link '
 '(y los saltos de línea extra que queden). Si al quitarlo no queda nada de texto, deja "Text" vacío.\n\n'
 'Si NO encuentras ninguna de las dos, deja "link_imagen" completamente vacío (cadena vacía) '
 'y copia el mensaje completo tal cual en "Text".\n\n'
 'No inventes contenido. No resumas. No agregues nada que no esté en el mensaje original.')
I[17]["mapper"]["parameters"] = [
 {"name": "link_imagen", "type": "string", "isRequired": False,
  "description": "URL de la imagen de la promoción (de la marca [ENVIAR_IMAGEN: ...] o de un link lh3 suelto); vacío si no hay"},
 {"name": "Text", "type": "string", "isRequired": False,
  "description": "El mensaje para el cliente sin la marca ni el link; vacío si el mensaje era solo la imagen"}]

# 3) modulo 4: manda el texto Y deja que el 19 mande la imagen; nunca con cuerpo vacio
TXT = ('{{ifempty(17.Text; ifempty(if(17.link_imagen = ""; 30.mensaje_limpio; ""); '
       'if(17.link_imagen = ""; 3.response; "")))}}')
I[4]["mapper"]["text"]["body"] = TXT
I[4]["filter"] = {"name": "Hay texto que enviar",
                  "conditions": [[{"a": TXT, "o": "text:notequal", "b": ""}]]}

# 4) manejadores de error donde no habia (un 429 de OpenAI mataba la conversacion)
for mid, (x, y) in {3:(600,300), 30:(900,300), 17:(1200,300), 4:(1500,0),
                    19:(1500,300), 31:(1500,600), 40:(1800,600), 51:(2100,600),
                    34:(1500,900)}.items():
    if mid in I and not I[mid].get("onerror"):
        I[mid]["onerror"] = resume(400 + mid, x, y)

json.dump(out, open("5645150_citas_BUENFIN.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
report("CITAS 5645150", live, out)
print("  systemPrompt", len(sp), "->", len(index(out)[3]["mapper"]["systemPrompt"]), "chars")
print("  filtro mod 4:", out and index(out)[4]["filter"]["name"])

# ──────────────────────── COSMETICOS 5587862 ────────────────────────
live2 = json.load(open("5587862_cosmeticos_live.json", encoding="utf-8"))
out2  = copy.deepcopy(live2)
J     = index(out2)

# 1) bloque Buen Fin, antes de la seccion de fichas tecnicas
sp2 = J[12]["mapper"]["systemPrompt"]
anchor = "FICHAS TÉCNICAS Y CATÁLOGO EN PDF"
q = sp2.find(anchor); assert q > 0, "no encuentro la seccion de fichas tecnicas"
q = sp2.rfind("═══", 0, q); q = sp2.rfind("\n", 0, q) + 1   # antes de su cabecera
J[12]["mapper"]["systemPrompt"] = sp2[:q] + blk("buenfin/bloque_cosmeticos.txt").lstrip("\n") + "\n" + sp2[q:]

# 2) modulo 60: que tambien extraiga la imagen de la promo
J[60]["mapper"]["parameters"].append(
 {"name": "promo_img_url", "type": "string", "isRequired": False,
  "description": "URL de la imagen de la promoción si el mensaje trae la marca [ENVIAR_IMAGEN: ...]; vacío si no"})
J[60]["mapper"]["prompt"] = (J[60]["mapper"]["prompt"]
 .replace("[AVISAR_HUMANO: motivo]", "[AVISAR_HUMANO: motivo]\n[ENVIAR_IMAGEN: URL]")
 .replace("([ENVIAR_ARCHIVO: ...] y [AVISAR_HUMANO: ...])",
          "([ENVIAR_ARCHIVO: ...], [AVISAR_HUMANO: ...] y [ENVIAR_IMAGEN: ...])")
 .replace("No inventes URLs ni nombres de archivo.",
          '3. Si existe la marca [ENVIAR_IMAGEN: ...], extrae en "promo_img_url" la URL completa tal cual '
          'aparece, sin recortarla ni modificarla. Si esa marca no existe, deja "promo_img_url" vacío.\n\n'
          "No inventes URLs ni nombres de archivo."))

# 3) ruta nueva en el router 90 para mandar la imagen
img = {"id": 62, "module": "whatsapp-business-cloud:sendMessage", "version": 1,
       "parameters": {"__IMTCONN__": 9795431},
       "filter": {"name": "Hay imagen de promoción para enviar",
                  "conditions": [[{"a": "{{60.promo_img_url}}", "o": "text:notequal", "b": ""}]]},
       "mapper": {"to": "{{1.contacts[].wa_id}}", "type": "image",
                  "image": {"link": "{{60.promo_img_url}}"}, "fromId": "587701384435147"},
       "metadata": {"designer": {"x": 2700, "y": 900}},
       "onerror": resume(321, 3000, 900)}
J[90]["routes"].append({"flow": [img]})

json.dump(out2, open("5587862_cosmeticos_BUENFIN.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
report("COSMETICOS 5587862", live2, out2)
print("  systemPrompt", len(sp2), "->", len(index(out2)[12]["mapper"]["systemPrompt"]), "chars")
print("  rutas del router 90:", len(index(out2)[90]["routes"]))
for f in ("5645150_citas_BUENFIN.json", "5587862_cosmeticos_BUENFIN.json"):
    json.load(open(f, encoding="utf-8")); print(f"\n{f}: JSON valido")

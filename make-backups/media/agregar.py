#!/usr/bin/env python3
"""Agrega lectura de fotos y transcripcion de audios a LEFRANM COSMETICOS."""
import json, copy, re

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
CONN_WA, CONN_AI = 9795431, 6001715
def resume(eid, x, y):
    return [{"id": eid, "module": "builtin:Resume", "version": 1, "mapper": {},
             "metadata": {"designer": {"x": x, "y": y}}}]

VISION_PROMPT = (
"Eres el ojo de un asistente de ventas de cosméticos mexicano. Vas a recibir la foto que "
"un cliente mandó por WhatsApp.\n\n"
"Describe en español, en 2 a 4 líneas y sin adornos, lo que realmente se ve:\n"
"1. TODO el texto legible del envase o la etiqueta, tal cual aparece (nombre del producto, "
"marca, contenido en g o mL, código). Esto es lo más importante: cópialo literal, no lo "
"interpretes ni lo corrijas.\n"
"2. Qué tipo de producto parece (crema, gel, jabón, mascarilla, loción, aceite, protector "
"solar...), su color y el tipo de envase (frasco, pomo, tubo, botella, sobre).\n"
"3. Si la foto NO es de un producto —es una persona, una pantalla, un comprobante de pago, "
"una receta, un lugar— dilo claramente en la primera línea y describe brevemente qué es.\n\n"
"No saludes, no recomiendes nada, no inventes lo que no esté visible. Si algo no se alcanza "
"a leer, escribe \"no se alcanza a leer\".")

# ── módulos nuevos ───────────────────────────────────────────────────────
getmedia = {
 "id": 500, "module": "whatsapp-business-cloud:getMedia", "version": 1,
 "parameters": {"__IMTCONN__": CONN_WA},
 "mapper": {"mediaId": "{{ifempty(1.messages[].image.id; 1.messages[].audio.id)}}"},
 "metadata": {"designer": {"x": 600, "y": 300}},
 "onerror": resume(510, 600, 600)}

vision = {
 "id": 501, "module": "openai-gpt-3:analyzeImages", "version": 1,
 "parameters": {"__IMTCONN__": CONN_AI},
 "mapper": {"prompt": VISION_PROMPT, "model": "gpt-5.2", "max_tokens": 500,
            "images": [{"imageUploadType": "imageFile",
                        "imageFileData": "{{500.mediaData}}"}]},
 "metadata": {"designer": {"x": 900, "y": 300}},
 "onerror": resume(511, 900, 600)}

audio = {
 "id": 502, "module": "openai-gpt-3:CreateTranscription", "version": 1,
 "parameters": {"__IMTCONN__": CONN_AI},
 "mapper": {"fileName": "{{500.mediaName}}", "fileData": "{{500.mediaData}}",
            "model": "gpt-4o-mini-transcribe",
            "prompt": "Audio de un cliente mexicano preguntando por productos cosméticos "
                      "de la marca Lefranm: cremas, geles, jabones, mascarillas, lociones, "
                      "protector solar, precios, envíos y pedidos."},
 "metadata": {"designer": {"x": 1200, "y": 300}},
 "onerror": resume(512, 1200, 600)}

flow = out["flow"]
pos = next(i for i, m in enumerate(flow) if m["id"] == 200) + 1
flow[pos:pos] = [getmedia, vision, audio]

# ── el agente recibe texto, transcripción o descripción de la foto ───────
msg = I[12]["mapper"]["message"]
old = "{{1.messages[].text.body}}"
assert msg.count(old) == 1
nuevo = (
 '{{ifempty(1.messages[].text.body; 502.text; '
 'if(501.result; "[EL CLIENTE MANDÓ UNA FOTO. Esto es lo que se ve en ella: " + 501.result + "]"'
 ' + if(1.messages[].image.caption; " Junto con la foto escribió: " + 1.messages[].image.caption; ""); "");'
 ' "[El cliente mandó un archivo que no puedes leer (un video, un sticker o una ubicación). '
 'Pídele con amabilidad que te escriba o te mande un audio diciendo qué necesita.]")}}')
I[12]["mapper"]["message"] = msg.replace(old, nuevo, 1)

# ── el prompt: qué hacer con fotos y audios ──────────────────────────────
sp = I[12]["mapper"]["systemPrompt"]
ancla = "═══════════════════════════════════════\nDEVOLUCIONES Y CAMBIOS"
assert sp.count(ancla) == 1
BLOQUE = '''═══════════════════════════════════════
FOTOS Y AUDIOS DEL CLIENTE
═══════════════════════════════════════
Los clientes pueden mandarte fotos y notas de voz. Un proceso interno las convierte a texto antes de que te lleguen.

AUDIOS: te llegan ya transcritos, como texto normal. Trátalos igual que cualquier mensaje escrito. NUNCA menciones que era un audio ni que se transcribió, y nunca le pidas al cliente que mejor escriba: mucha gente mayor prefiere el audio y hay que atenderla igual de bien.

FOTOS: te llegan como una línea que empieza con "[EL CLIENTE MANDÓ UNA FOTO. Esto es lo que se ve en ella: ...]". Eso NO lo escribió el cliente — es la descripción de la foto hecha por el sistema. Nunca se la repitas tal cual, nunca le menciones que recibiste una "descripción", y nunca digas que "no puedes ver imágenes".

Qué hacer con una foto:

- Si por el texto de la etiqueta reconoces el producto en el CATÁLOGO COMPLETO, dilo con seguridad, explícale en una o dos líneas para qué sirve, y dale el precio de la lista que le corresponda. Ejemplo: "¡Claro! Es nuestro Jabón Dermolimpiador 🙂 Sirve para limpiar la piel a profundidad sin resecarla. Le queda en $X."
- Si la etiqueta se lee a medias y hay dos o tres productos nuestros que podrían ser, NO adivines: menciona los que podrían ser y pregúntale cuál tiene, o pídele otra foto de la etiqueta de frente.
- Si el producto NO es de Lefranm, dilo con amabilidad y sin hablar mal de la otra marca, y ofrécele el equivalente nuestro del CATÁLOGO COMPLETO.
- Si no se alcanza a leer nada, pídele con calidez otra foto un poco más cerca de la etiqueta y con buena luz.
- Si la foto es un COMPROBANTE DE PAGO, una transferencia o un recibo: tú no confirmas pagos. Agradécele, dile que el equipo lo va a verificar y se pondrá en contacto, y agrega la marca [AVISAR_HUMANO: comprobante de pago recibido].
- Si la foto es una receta médica, una lesión en la piel, una persona, o cualquier cosa que implique dar un diagnóstico: NO opines ni recomiendes tratamientos. Dile con amabilidad que prefieres que lo vea alguien del equipo y agrega la marca [AVISAR_HUMANO: foto que requiere revisión humana].

NUNCA inventes un producto que no esté en el CATÁLOGO COMPLETO solo porque la foto se le parece. Si no está en el catálogo, no existe.

'''
I[12]["mapper"]["systemPrompt"] = sp.replace(ancla, BLOQUE + ancla, 1)

json.dump(out, open("5587862_media.json", "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))

# ── verificación ─────────────────────────────────────────────────────────
A, B = index(src), index(out)
sh = lambda d: {k: {a: b for a, b in v.items() if a not in ("routes","onerror")} for k, v in d.items()}
a, b = sh(A), sh(B)
print("modulos nuevos     :", sorted(set(b)-set(a)))
print("modulos eliminados :", sorted(set(a)-set(b)))
print("modulos modificados:", sorted(k for k in set(a)&set(b)
      if json.dumps(a[k],sort_keys=True,ensure_ascii=False)!=json.dumps(b[k],sort_keys=True,ensure_ascii=False)))
print("\norden del flujo principal:", [m["id"] for m in out["flow"]])
s1,s2 = json.dumps(src), json.dumps(out)
g = lambda s,p: sorted(set(re.findall(p,s)))
print("webhook   :", g(s2,'"__IMTHOOK__":\\s*(\\d+)'))
print("conexiones:", g(s1,'"__IMTCONN__":\\s*(\\d+)'), "->", g(s2,'"__IMTCONN__":\\s*(\\d+)'))
print("scheduling:", json.dumps(out.get("scheduling")))
print("onerror   :", s1.count('"onerror"'), "->", s2.count('"onerror"'))
print("systemPrompt:", len(sp), "->", len(B[12]["mapper"]["systemPrompt"]))
print("\nmensaje al agente:\n ", B[12]["mapper"]["message"].split("\\n")[-1][:400])

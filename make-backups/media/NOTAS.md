# Lectura de fotos y transcripción de audios — 17 nov 2026

El dueño pidió que el bot pueda leer fotos de producto y entender notas de voz,
porque las personas mayores prefieren mandar audio.

## Hallazgo previo: las fotos y audios YA entraban, y mal

El filtro del módulo 12 revisaba únicamente la pausa:

```
"No pausado (o pausa vencida)" → {{200.pausado_hasta}} notexist / date:less
```

No filtraba por tipo de mensaje. Así que una foto o un audio **sí disparaban el
escenario**, pero el agente recibía solo la línea de contexto interno y ningún
texto, porque el mapeo era `{{1.messages[].text.body}}` y venía vacío. El
cliente recibía una respuesta desconcertada.

(El escenario de citas sí lo filtra: su módulo 3 tiene *"**Texto** y no
pausado"*. Cosméticos no, y por eso procesaba lo que no podía leer.)

## Las piezas

El webhook ya entregaba todo lo necesario — no se tocó:
`messages[].type`, `messages[].image.id`, `messages[].image.caption`,
`messages[].audio.id`.

| Módulo | App | Para qué |
|---|---|---|
| **500** | `whatsapp-business-cloud:getMedia` | baja el archivo por su ID → `mediaName` + `mediaData` |
| **501** | `openai-gpt-3:analyzeImages` | lee la foto (`gpt-5.2`) |
| **502** | `openai-gpt-3:CreateTranscription` | transcribe el audio (`gpt-4o-mini-transcribe`) |

Más sus manejadores `builtin:Resume` 510, 511 y 512.

La salida de `getMedia` encaja directo con lo que piden los otros dos:
`mediaData` → `imageFileData` y `fileData`; `mediaName` → `fileName`.

Las tres configuraciones se validaron con `validate_module_configuration`
contra el esquema real de Make: `valid: true`, cero errores. El validador pidió
`logProbs: false` como default en la transcripción y se agregó.

Modelos tomados de `rpc_execute getModels` (no inventados):
`gpt-5.2` para visión, `gpt-4o-mini-transcribe` para audio. El campo de salida
de la transcripción (`text`) se confirmó con el RPC `audioMappings`.

## Por qué van en la línea principal y no en un router

En Make, **un filtro que bloquea detiene toda la rama**, y las rutas de un
router no se vuelven a juntar. Poner un filtro "solo si es imagen" sobre un
módulo de la línea principal haría que los mensajes de texto murieran ahí.

Por eso los tres módulos corren siempre y fallan sin consecuencia (`Resume`)
cuando no aplican: en un mensaje de texto, `getMedia` recibe un ID vacío,
falla, y el flujo sigue.

**Costo: +3 operaciones por mensaje entrante**, también en los de texto.

La alternativa barata —router al inicio, la rama de media guarda el texto en la
base y la rama normal lo lee— cuesta +1 en texto, pero obliga a meter toda la
cadena actual dentro de una ruta de router. Se descartó por riesgo, no por
desconocimiento. Si las operaciones aprietan, se migra sin tocar el prompt.

### Contexto de operaciones (17 nov)

| | |
|---|---|
| Plan Core | 40,000 operaciones/mes |
| Usadas desde el 13 de nov | 6,546 en ~4 días |
| Ritmo | ~1,577/día → ~47,000 proyectados |

Va apretado, pero el 13-17 de noviembre es justo la semana del Buen Fin con los
anuncios corriendo, así que lo más probable es que sea pico y no la norma.
Conviene revisarlo cerrando el mes.

## Lo que recibe el agente

`message` del módulo 12, con cascada:

```
{{ifempty(1.messages[].text.body; 502.text; if(501.result; "[EL CLIENTE MANDÓ UNA FOTO. Esto es lo que se ve en ella: " + 501.result + "]" + if(1.messages[].image.caption; " Junto con la foto escribió: " + 1.messages[].image.caption; ""); ""); "[El cliente mandó un archivo que no puedes leer...]")}}
```

Simulado en los cinco casos:

| Entrada | Lo que recibe el agente |
|---|---|
| Texto | el texto tal cual |
| Audio | la transcripción, como texto normal |
| Foto sin pie | `[EL CLIENTE MANDÓ UNA FOTO. Esto es lo que se ve...]` |
| Foto con pie | lo anterior + `Junto con la foto escribió: ...` |
| Video, sticker, ubicación | un aviso para que pida que le escriban |

## El bloque nuevo del prompt

`FOTOS Y AUDIOS DEL CLIENTE`, insertado antes de `DEVOLUCIONES Y CAMBIOS`.

Lo que cubre:

- **Audios**: tratarlos como texto normal. Nunca mencionar que era un audio ni
  pedirle al cliente que mejor escriba — mucha gente mayor prefiere el audio.
- **Fotos de producto**: si la etiqueta se lee y el producto está en el
  catálogo, nombrarlo y cotizarlo. Si se lee a medias, preguntar entre dos o
  tres candidatos en vez de adivinar. Si no es de Lefranm, ofrecer el
  equivalente sin hablar mal de la otra marca.
- **Comprobantes de pago**: el bot no confirma pagos. Agradece, avisa que el
  equipo verifica y agrega `[AVISAR_HUMANO: comprobante de pago recibido]`.
- **Recetas médicas, lesiones en la piel, personas**: no opinar ni recomendar
  tratamientos. `[AVISAR_HUMANO: foto que requiere revisión humana]`.
- Nunca inventar un producto que no esté en el `CATÁLOGO COMPLETO` solo porque
  la foto se le parece.

El prompt de visión (módulo 501) está afinado para lo que de verdad importa:
copiar **literal** todo el texto legible de la etiqueta, que es lo que permite
al agente cruzarlo con el catálogo.

## Verificación

Construido sobre `5587862_compra-simple.json`, que el usuario todavía no había
importado, así que **un solo import trae las dos cosas**: la simplificación de
compra y la lectura de media.

| | vivo | entregado |
|---|---:|---:|
| Módulos | 36 | 42 |
| `onerror` | 17 | 20 |
| `systemPrompt` | 41,211 | 46,534 |

Flujo principal: `1 → 2 → 101 → 200 → 500 → 501 → 502 → 12 → 70 → 60 → 42 → 38 → 90`

Módulos modificados respecto a `compra-simple`: **solo el 12**. Webhook
`2547718`, conexiones `10484205 / 6001715 / 9795431`, `scheduling: immediately`
— sin cambio. Catálogo (93 referencias), CLABE, Kit, Buen Fin, tarifas de
envío, modo cotizador, regla de cabina, devoluciones y las marcas internas:
intactos.

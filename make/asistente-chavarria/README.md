# Asistente Chavarria (Make)

Copia versionada del prompt del asistente de WhatsApp del CUT Tláhuac.

- **Escenario en Make:** `Asistente Chavarria` (id `5982362`, equipo `1436402`)
- **Módulo:** `3` — *AI Agent* (`ai-local-agent:RunLocalAIAgent`)
- **Archivo:** [`system-prompt.md`](./system-prompt.md)

El contenido de `system-prompt.md`, a partir del encabezado `# Daniela — Asistente de
Admisiones CUT Tláhuac`, es exactamente el texto que va en el campo *System prompt* del
módulo. Si se edita aquí, hay que copiarlo también en Make (y viceversa) para que no se
desincronicen.

## Versión 2 — respuestas cortas

Cambio respecto a la v1: el asistente mandaba un solo mensaje enorme con todo
(costos + documentos + ventajas + horarios). Ahora la sección 0 impone:

- máximo 5 líneas y 4 viñetas por mensaje
- responder solo lo preguntado y ofrecer el resto
- prohibido juntar costos, documentos, ventajas y horarios en un mismo mensaje
- cerrar siempre con una sola pregunta
- formato de WhatsApp (`*negritas*` con un asterisco, sin `##` ni `**`)
- ejemplos de respuesta correcta e incorrecta

Los datos institucionales, costos, documentos y las marcas internas
(`[CIERRE: ...]` / `[AVISAR_HUMANO: ...]`) no cambiaron: el módulo 30 y los de
Airtable/Calendar/Gmail siguen funcionando igual.

## Versión 2.1 — dos cosas que el asistente prometía sin poder cumplir

- **Plan de materias en PDF.** La v1 decía "Ofrece el plan de materias en PDF" en la
  sección 4, pero el escenario solo puede mandar texto por WhatsApp: no hay módulo que
  envíe archivos. El asistente lo ofrecía y luego respondía "listo, te lo comparto" sin
  mandar nada. Se quitó esa instrucción y se agregó una regla dura en la sección 9:
  no puede prometer PDF, folletos ni ningún archivo; si se lo piden, resume en el chat
  y marca `[AVISAR_HUMANO: pide plan de materias]`.
- **Citas inventadas.** Proponía días y horas que nadie mencionó ("¿te agendo mañana a
  las 14:00?"), lo que puede terminar creando un evento falso en el Google Calendar del
  plantel. Ahora debe preguntar qué día y hora le acomodan, y solo escribe fecha en
  `[CIERRE: ...]` si la persona la dijo o la aceptó.

## Versión 3 — el bot vende, la directora solo cierra

El prompt decía "Empuja el siguiente paso: agendar cita o apartar lugar" en el paso 5
del proceso de venta, así que el asistente usaba la cita como respuesta a cualquier
duda ("¿quieres que agende una cita para explicártelo en el plantel?"). Resultado: el
trabajo de venta terminaba cayendo en la directora en vez de resolverse en el chat.

La sección 8 se reescribió como **"TÚ LLEVAS TODA LA VENTA"**:

- Prohibido usar la cita, el plantel o la directora como respuesta a una duda, con las
  frases típicas listadas explícitamente.
- Solo se menciona cita o pasar con una persona en tres casos: lo pide el prospecto,
  es convalidación/queja/caso especial, o ya cerró.
- Semáforo de cuatro etapas (apenas empieza / explorando / casi decidido / cerró) que
  define qué toca en cada momento.
- Lista de preguntas de cierre de mensaje que sí sirven, para que no caiga siempre en
  la cita.
- La sección 13 ahora aclara que "me interesa" o preguntar precios **no** es cierre.

También en la sección 4: al pedir el plan de materias, resume en el chat y pregunta qué
parte le interesa, en vez de remitir al plantel; y solo puede nombrar materias que estén
en las listas del prompt (había inventado "Mercadotecnia digital" y "Proyecto integrador").

## Versión 4 — prohibición absoluta de inventar

La regla "nunca inventes información" estaba enterrada en la sección 9 y no bastó: el
asistente inventó las materias "Mercadotecnia digital" y "Proyecto integrador", que no
aparecen en ningún lado del prompt.

Se agregó una **REGLA INQUEBRANTABLE al inicio del prompt**, antes que cualquier otra
instrucción:

- Todo dato que diga tiene que estar escrito literalmente en el prompt. Lo que no está,
  no existe: no se deduce, no se completa "por lógica", no se toma de lo que el modelo
  sabe de otras escuelas.
- Aplica a materias, carreras, precios, descuentos, becas, fechas, horarios, requisitos,
  instalaciones, convenios, certificaciones, nombres de personas y formas de pago.
- Lista los tres errores reales ya cometidos (materias inventadas, PDF inexistente, cita
  inventada) como ejemplos de lo que no se repite.
- Cuando falte el dato: decirlo ("déjame confirmarlo con el equipo") y marcar
  `[AVISAR_HUMANO: ...]`. Nunca rellenar con algo aproximado.
- Chequeo final antes de enviar: si un dato no se puede señalar dentro del prompt, se borra.

La sección 4 y la sección 9 ahora apuntan a esta regla en lugar de repetirla a medias.

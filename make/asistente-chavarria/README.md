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

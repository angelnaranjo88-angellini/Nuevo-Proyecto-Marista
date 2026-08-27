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

## Versión 5 — fecha y hora reales inyectadas

El módulo 3 ya no recibe solo el mensaje del prospecto. El mapper del campo *Message*
antepone una línea de sistema:

```
[SISTEMA] Fecha y hora ahora en CDMX: {{formatDate(now; "dddd YYYY-MM-DD HH:mm"; "America/Mexico_City")}}
```

Con eso el asistente sabe qué día es y puede: saber si está dentro del horario de
atención humana, calcular cuántos días faltan para el inicio de clases y para el cierre
de inscripciones, entender "mañana" o "el lunes", y escribir el año correcto en
`[CIERRE: ... cita=...]`. La sección FECHA Y HORA le prohíbe mencionar o repetir esa
línea, y le prohíbe calcular fechas de memoria.

## Versión 6 — dejó de inventar la hora de la cita

El asistente seguía proponiendo "mañana a las 14:00" aunque la regla lo prohibía.
Causa: **el propio prompt traía esa frase literal tres veces como ejemplo de lo que NO
debía hacer**, y el modelo la copiaba. Los ejemplos negativos con texto concreto priman
la respuesta.

- Se quitaron todas las horas concretas de los ejemplos; ahora van como `<día>` y `<hora>`.
- Se agregó la subsección *Prohibición absoluta sobre días y horas de cita*, con las
  frases prohibidas en placeholder y las tres preguntas que sí puede hacer.

## Versión 7 — la cita acordada ya no se pierde

Síntoma: el prospecto confirmaba día y hora, pero el correo a la dirección llegaba con
"Sin fecha acordada" y no se creaba el evento en Google Calendar. Confirmado por el
conteo de operaciones de las ejecuciones (6 ops = sin correo ni calendario; 8 = correo;
9 = correo + calendario).

Causa: el prompt exigía una segunda confirmación, así que el asistente cerraba con
"¿va?" y nunca emitía `[CIERRE]`. Ahora:

- **El día y la hora que dice la persona YA son el acuerdo.** La marca `[CIERRE: ...]`
  va en ese mismo mensaje.
- Prohibido cerrar con "¿va?", "¿te parece?" o "¿confirmas?".
- Si después cambia la fecha, se manda otra vez la marca con la nueva.

También se pusieron manejadores **Skip** (`builtin:Ignore`) en el módulo 41
(Google Calendar) y en el 42 (Gmail), para que un fallo de esos servicios no cuente
como error del escenario ni lo desactive (`maxErrors: 3`).

## Versión 8 — se presentaba en cada mensaje

Mismo patrón de la v6: el prompt traía `Primer mensaje tipo: ¡Hola! Soy Daniela...`, y el
modelo lo repetía en todos los mensajes. Se cambió por una regla explícita de una sola
vez ("si en el historial ya hay un mensaje tuyo, ya te presentaste") más un ejemplo MAL,
y se subió `iterationsFromHistoryCount` a 25 para que tenga memoria suficiente de la
conversación.

## Versión 9 — vender en vez de interrogar, y escalar poco

Dos problemas reportados en la misma prueba: el asistente hacía pregunta por pregunta
antes de dar información, y le mandaba correo a la directora por cualquier dato que le
faltara.

- Nueva subsección **"El paquete"**: en cuanto la persona nombra un programa, va todo en
  un solo mensaje (qué es, duración, modalidades con horario, inscripción y mensualidad
  de cada una, inicio del periodo y un diferenciador), sin preguntarle nada antes.
- Regla *responde primero, pregunta después*; prohibido contestar una pregunta con otra.
- `[AVISAR_HUMANO]` se acotó a **cuatro casos** (piden hablar con alguien, queja o alumno
  inscrito con problema, convalidación o caso especial de pago, ya quiere inscribirse),
  con la regla explícita: *NUNCA la uses solo porque te falte un dato*.
- Se cargaron los primeros cinco mapas curriculares oficiales en
  `### PLANES DE ESTUDIO QUE SÍ TIENES`, cada uno con una línea de "Ganchos" de venta.

## Versión 10 — diez planes de estudio oficiales

Se agregaron los cinco mapas curriculares restantes que entregó el cliente, extraídos de
los PDF oficiales con `pdftotext -layout`:

- Ingeniería en Sistemas Computacionales (9 cuatrimestres)
- Ingeniería en Seguridad Industrial e Higiene (8 semestres)
- Maestría en Docencia (5 cuatrimestres)
- Maestría en Educación Inclusiva (5 cuatrimestres)
- Maestría en Juicios Orales (5 cuatrimestres, materia **penal** — distinta de la de
  Derecho Laboral; el prompt lo advierte para que no las confunda)

La sección 4 pasó de "cinco programas" a "diez programas", y sigue vigente la regla de
no recitar un periodo completo: menciona 4 o 5 materias representativas.

Ajuste de consistencia: el mapa oficial de **Ing. en Seguridad Industrial e Higiene es
semestral, de 8 semestres**, no cuatrimestral de 3 años como decía la lista general de
licenciaturas. Se corrigió en los dos lugares donde aparecía.

### Deporte y Lengua de Señas (resuelto)

El cliente confirmó que los alumnos **sí llevan actividades deportivas**, y que **Lengua
de Señas es extracurricular**. Ninguna de las dos aparece en el mapa curricular oficial,
así que se agregaron a la sección BACHILLERATO como *actividades extracurriculares*, con
la instrucción explícita de mencionarlas siempre como actividades y nunca como
asignaturas del plan de estudios.

### Pendiente de confirmar con la dirección

- **Modalidad de la Maestría en Administración de Servicios de Salud.** Su PDF oficial
  dice "MODALIDAD NO ESCOLARIZADA / OPCIÓN EDUCATIVA EN LÍNEA O VIRTUAL", mientras que la
  regla general de maestrías del prompt dice "sabatino o en línea". El prompt ya marca
  esta maestría como solo en línea; si también se ofrece sabatina, hay que corregirlo.

### Mapas curriculares que todavía faltan (14 de 24 programas)

El asistente ya vende estos programas con duración, modalidades, horarios y costos, pero
**sin materias** — dice que el plan completo se lo entregan en el plantel. Cuando lleguen
los PDF se cargan igual que los otros diez.

Licenciaturas e ingenierías (7): Administración de Empresas · Contaduría Pública ·
Derecho · Pedagogía · Criminalística y Criminología · Ciencias del Deporte ·
Ing. en Calidad y Productividad

Maestrías (2): Pedagogía · Administración y Negocios

Doctorados (5): Administración · Alta Dirección y Liderazgo Empresarial · Dirección y
Supervisión de Instituciones Educativas · Ciencias de la Educación · Derecho
Constitucional y Derechos Humanos

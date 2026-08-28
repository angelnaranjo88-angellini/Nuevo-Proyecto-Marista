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

## Versión 11 — cinco licenciaturas más (cuatro de ellas parciales)

Se agregaron, desde las imágenes de los mapas curriculares oficiales:

| Programa | Lo que quedó cargado |
|---|---|
| Administración de Empresas | 1º–6º de 9 cuatrimestres |
| Contaduría Pública | 1º–6º de 9 cuatrimestres |
| Criminalística y Criminología | 1º–6º de 9 cuatrimestres |
| Derecho | 1º–6º (el plan es de 2 años 4 meses) |
| Pedagogía | los 6 semestres completos |

Las imágenes llegaban cortadas en el 6º periodo, así que **cada uno de esos cuatro
bloques lleva su propia advertencia** de que solo tiene los primeros 6 periodos y de que
del resto no puede decir ni una materia. La sección 4 lo repite de forma general.

También se corrigió un riesgo que ya existía: el ejemplo BIEN de la sección 0 usaba
materias de **Seguridad Pública** bajo un encabezado genérico, justo debajo de otro
ejemplo sobre Criminalística. Ahora el encabezado nombra explícitamente Seguridad
Pública, para que el modelo no cruce los dos planes.

Total: **15 planes cargados de 24 programas**.

## Versión 12 — Ciencias del Deporte, dos maestrías y el primer doctorado

Cuatro planes más, de los PDF oficiales (el quinto archivo era otra copia del de Ing. en
Seguridad Industrial e Higiene, que ya estaba cargado):

| Programa | Lo que quedó cargado |
|---|---|
| Lic. en Ciencias del Deporte | los 9 cuatrimestres completos |
| Mtría. en Pedagogía | los 4 cuatrimestres del mapa oficial |
| Mtría. en Administración y Negocios | los 4 cuatrimestres del mapa oficial |
| Dr. en Ciencias de la Educación | los 6 semestres completos |

Total: **19 planes cargados de 24 programas.**

La Maestría en Pedagogía lleva además el aviso de no confundirla con la *Licenciatura* en
Pedagogía, que es semestral y tiene otro plan completamente distinto.

### Discrepancia: maestrías de 4 vs. 5 cuatrimestres

La sección general de MAESTRÍAS dice "1 año 8 meses (5 cuatrimestres)", pero los mapas
oficiales de **Pedagogía** y de **Administración y Negocios** solo traen 4 cuatrimestres.
No se tocó la regla general; cada uno de esos dos bloques dice que el mapa que tiene son 4
cuatrimestres, que la duración es la de la sección general, y que **no invente materias de
un quinto cuatrimestre**. Hay que confirmar con la dirección cuál de los dos datos manda.

### Correcciones de tipografía sobre los PDF

Los originales traen erratas evidentes que se normalizaron para que el asistente no se las
mande a un prospecto. No son cambios de contenido, pero conviene verificarlas:

- Ciencias del Deporte: "Prespectiva" → Perspectiva · "Admistración" → Administración ·
  "Mercadotectenia" → Mercadotecnia · "Lógistica" → Logística · "Acuaticos" → Acuáticos
- Mtría. en Pedagogía: "Investigacón" → Investigación · **"Gramificación" → Gamificación**
  (esta es la única que no es una errata obvia de acento; va junto a "Realidad Aumentada y
  Educación 4.0", así que casi seguro es Gamificación, pero vale confirmarla)

## Versión 15 — los cinco doctorados y todos los datos de negocio

### Planes de estudio: 23 de 24

Se cargaron los cinco doctorados. Con eso el asistente tiene el mapa curricular de
**23 de los 24 programas**. El único que sigue sin materias es **Ing. en Calidad y
Productividad**.

| Doctorado | Estructura |
|---|---|
| Administración | 6 semestres |
| Derecho Constitucional y Derechos Humanos | 6 semestres |
| Alta Dirección y Liderazgo Empresarial | 6 cuatrimestres |
| Dirección y Supervisión de Instituciones Educativas | 6 cuatrimestres |
| Ciencias de la Educación | 6 cuatrimestres |

### Datos de negocio que entraron

- **Formas de pago:** efectivo (en plantel) y transferencia. Sin tarjeta, sin MSI.
  Inscripción pagable en dos partes. Colegiaturas del 1 al 10; recargo del 10% después.
  12 mensualidades al año en todos los niveles.
- **Descuento bachillerato:** 30% el mismo día antes de las 6 pm — $1,750 en vez de $2,500.
  Ahora es el primer punto de la sección de urgencia.
- **Lic./Mtría./Doc.:** no hay descuento ni becas, pero sí *inscripción única* y
  *colegiatura congelada*. Convertido en el argumento central de esas objeciones.
- **Uniforme:** pants $1,450 · polo $500 · sudadera $850, en el plantel.
- **Reprobar:** extraordinario $800, recursamiento $2,500.
- **Devolución:** 100% de la inscripción.
- **Seguro escolar:** $1,000/año con Mapfre, cubre accidentes dentro del plantel.
- **Sin certificado de secundaria:** sí se puede, con constancia de trámite cuya fecha de
  egreso caiga en el ciclo (julio de 2026 para este año). Antes el bot no sabía qué decir.
- **Edades:** bachillerato 15–20, licenciatura 18+, maestría 21+, doctorado 24+.
- **Modalidad en línea:** clases en vivo por videollamada (Zoom, Meet, Classroom),
  exámenes en línea por Google Forms.
- **Centro de Idiomas Trilingüe:** qué es, requisito de titulación B1, y el contacto
  (56-19-88-42-35 / centrodeidiomas@centrotrilingue.edu.mx), que solo se comparte si
  preguntan por idiomas.
- **Resultados reales:** de cada 20 egresados, 9 se quedan en UNAM/IPN/UPN/UAM, 4 en otras
  universidades del gobierno, 5 siguen en el CUT, 2 al campo laboral. Sembrado en tres
  objeciones distintas con la instrucción de no inflarlo ni redondearlo.
- **Deportes y talleres:** basquetbol, futbol, acondicionamiento físico y terapias
  psicológicas — por nombre, sin agregar otros.

### Tres decisiones que hay que validar con la dirección

1. **Se quitó la "Reinscripción $1,000 por periodo" de Licenciatura escolarizado.** El
   dato nuevo del cliente ("la inscripción es única, no pagas reinscripciones") contradice
   directamente esa línea del costeo anterior. Se conservó el dato nuevo. Si la
   reinscripción de $1,000 sigue existiendo, hay que regresarla.
2. **Hay dos mapas distintos del Doctorado en Ciencias de la Educación.** Uno semestral
   (6 semestres) y otro cuatrimestral (6 cuatrimestres), con materias completamente
   diferentes. Se dejó cargado el cuatrimestral, porque viene en el mismo lote que los
   otros dos doctorados cuatrimestrales. Falta confirmar cuál es el vigente.
3. **La duración de los doctorados cuatrimestrales.** La regla general decía "3 años",
   pero 6 cuatrimestres no son 3 años. La sección DOCTORADOS ahora separa semestrales de
   cuatrimestrales y le prohíbe al asistente afirmar los años en los cuatrimestrales:
   dice "6 cuatrimestres" y remite al plantel.

### Lo que sigue faltando

- Mapa curricular de **Ing. en Calidad y Productividad**.
- Confirmar si las maestrías en Pedagogía y en Administración y Negocios son de 4 o de 5
  cuatrimestres.

## Versión 16 — planes completos de las cuatro licenciaturas que estaban a medias

Llegaron los PDF completos y se cerraron los últimos periodos que faltaban:

| Programa | Lo que se agregó |
|---|---|
| Administración de Empresas | 7º, 8º y 9º |
| Contaduría Pública | 7º, 8º y 9º |
| Criminalística y Criminología | 7º, 8º y 9º |
| Derecho | 7º (el último) |

Con eso desaparecieron las cuatro advertencias de "solo tienes los primeros 6
cuatrimestres". Los únicos planes parciales que quedan son las dos maestrías de 4
cuatrimestres, y la sección 4 ahora lo dice nombrándolas.

**Corrección de duración en Derecho.** El mapa oficial tiene 7 cuatrimestres, que es lo que
da los 2 años 4 meses. Antes el prompt solo decía "2 años 4 meses" sin el número de
periodos, y el encabezado de LICENCIATURAS tampoco lo aclaraba. Ahora ambos lo dicen.

**Ing. en Calidad y Productividad** se queda como está: el asistente la vende con duración,
modalidades, horarios y costos, y dice que el plan completo se lo entregan en el plantel.
Es el único de los 24 programas sin mapa curricular.

## Versión 17 — mandan los mapas oficiales, no la regla general

Decisión del cliente: **cuando el mapa curricular oficial contradiga la regla general de la
sección, gana el mapa.**

Eso resuelve el caso de las dos maestrías cuyos mapas traen 4 cuatrimestres mientras la
sección general decía 5. Ahora la sección MAESTRÍAS separa las dos duraciones en lugar de
afirmar una sola:

- **5 cuatrimestres (1 año 8 meses):** Docencia · Educación Inclusiva · Juicios Orales ·
  Juicios Orales en Derecho Laboral · Administración de Servicios de Salud
- **4 cuatrimestres (1 año 4 meses):** Pedagogía · Administración y Negocios

Con la instrucción explícita de no decir "1 año 8 meses" de forma general y de tratar la
duración más corta como argumento de venta, no como carencia. En los dos bloques
correspondientes se quitó la advertencia de "puede faltar un quinto cuatrimestre" y el
encabezado ahora dice el número real de periodos.

Consecuencia en la sección 4: **ya no hay planes parciales**. Los 23 planes cargados están
completos de principio a fin, y el prompt lo dice así en lugar de nombrar excepciones.

## Versión 18 — la reinscripción de licenciatura escolarizada vuelve, acotada por modalidad

El cliente confirmó que **los $1,000 de reinscripción por periodo en licenciatura
escolarizada sí siguen vigentes**. La línea se restauró en la sección 5.

Contexto de por qué se había quitado: al responder la pregunta de descuentos, el cliente
escribió *"la inscripción es única, es decir no pagas reinscripciones cuatrimestrales o
semestrales"*, lo que contradecía esa línea. El dato de los $1,000 no venía de esta ronda de
información — estaba en el prompt desde el primer commit del repo (`42041f0`), o sea desde la
copia original que ya vivía en Make.

La forma de conciliar los dos datos sin que el asistente prometa algo falso: **la inscripción
única se acota por modalidad**, que es justo lo que refleja la lista de costos.

| | Reinscripción |
|---|---|
| Licenciatura sabatino | no paga |
| Licenciatura en línea | no paga |
| Maestría | no paga |
| Doctorado | no paga |
| **Licenciatura escolarizado** | **$1,000 por periodo** |
| Bachillerato | $2,500 semestral (no cambió) |

La **colegiatura congelada** sí aplica a los tres niveles sin excepción, así que ese quedó
como el argumento principal y la inscripción única como el secundario.

Se ajustaron los cinco lugares donde aparecía la promesa genérica: diferenciadores,
descuentos, becas, la objeción de "está caro" y la de "en otra escuela es más barato". Y se
agregó una advertencia explícita: *fíjate en la modalidad antes de decir "inscripción única";
prometerle a alguien de escolarizado que no paga reinscripción es un problema el día que le
cobren.*

## Versión 19 — se acabaron los correos duplicados a la dirección

El cliente reportó que la dirección estaba recibiendo muchos correos y que **ninguno era un
cierre de venta**. El diagnóstico se hizo con la aritmética de operaciones de `executions_list`,
porque `executions_get-detail` no devuelve el detalle por módulo en este escenario.

Línea base de una ejecución normal: **6 operaciones** (trigger → AI Agent → transform →
búsqueda en Airtable → envío por WhatsApp → alta o actualización en Airtable). A partir de ahí:

| Operaciones | Qué pasó |
|---|---|
| 6 | conversación normal, sin correo |
| 7 | se disparó el correo de escalación (`necesita_aviso`, sin cierre) |
| 8 | correo + módulo 45 (cierre sobre un prospecto existente) |
| 9 | lo anterior + evento de calendario |

El 27 de agosto hubo **8 ejecuciones de 7 operaciones** y **ninguna de 8 ni de 9**. Es decir:
los 8 correos salieron, y ni uno solo correspondía a un cierre real. Coincide exactamente con
lo que reportó el cliente.

Un mismo prospecto generó 4 correos, todos de 7 operaciones. Como su registro en Airtable ya
existía desde el primero, el módulo 45 habría disparado (8 operaciones) si `es_cierre` fuera
verdadero — no disparó nunca. O sea: `es_cierre` era **falso** y aun así el asunto del correo
decía "Prospecto listo para inscripcion".

### Causa 1 — el asunto del correo mentía (arreglo en el blueprint)

El asunto del módulo 42 usaba `{{if(30.es_cierre; ...)}}`. En Make, `if()` evalúa la cadena
`"false"` como verdadera, porque es una cadena no vacía. Resultado: todo correo salía con el
asunto de cierre, aunque el filtro (que sí compara bien, con `text:equal`) lo hubiera dejado
pasar por `necesita_aviso`. Se cambió a una comparación de texto real:

```
{{if(contains(lower(30.es_cierre); "true"); "CUT - Prospecto listo para inscripcion: "; "CUT - Prospecto necesita atencion: ")}}
```

El filtro del módulo 42 no se tocó: estaba bien.

### Causa 2 — las marcas se repetían en cada mensaje (arreglo en el prompt)

El asistente volvía a escribir `[AVISAR_HUMANO]` en cada respuesta mientras el motivo siguiera
vigente. Alguien que pregunta por vacantes y manda cinco mensajes generaba cinco correos
idénticos. Se agregaron tres reglas:

- Sección 15, `[AVISAR_HUMANO]`: **una sola vez por conversación**. Antes de escribirla hay que
  revisar el historial; solo procede una segunda marca si el motivo es *distinto*. Y después de
  mandarla, se sigue atendiendo normal, sin anunciarle al prospecto que "ya avisó".
- Sección 15, `[CIERRE]`: no se repite. Solo se vuelve a mandar si cambió algo real — el día,
  la hora, el nombre, el programa o la modalidad. Repetirla creaba además un evento duplicado
  en el calendario.
- Sección 10 (quién no es prospecto): la misma regla de una sola vez, en el primer mensaje en
  que se detecta el caso.

Desde las 01:57 del 28 de agosto no ha salido ningún correo: las 16 ejecuciones posteriores
son todas de 6 operaciones.

### Pendientes

- Confirmar cuál es el mapa vigente del Doctorado en Ciencias de la Educación. Aquí el
  criterio "manda el mapa" no desempata, porque los dos candidatos **son** mapas oficiales:
  uno semestral (6 semestres) y otro cuatrimestral (6 cuatrimestres), con materias
  completamente distintas. Está cargado el cuatrimestral, por venir en el mismo lote que los
  otros dos doctorados cuatrimestrales.

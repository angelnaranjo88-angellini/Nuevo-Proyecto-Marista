# LEFRANM CITASS — prompt del agente (Make, escenario 5645150)

Historial del *system prompt* del módulo `ai-local-agent:RunLocalAIAgent`.
Make no guarda versiones del prompt, así que se versiona aquí.

| Archivo | Estado |
|---|---|
| `prompt-v1-anterior.txt` | Versión en producción hasta el 2026-09-04 |
| `prompt-v2-catalogo-maestro.txt` | Versión nueva |

## Por qué cambió

El asistente ofreció por WhatsApp un "Masaje anti-estrés 90 min $390" que no
existe. La cadena `90 min` no aparecía ni una vez en `prompt-v1`: el modelo
compuso el dato en vez de copiarlo.

Causas estructurales corregidas en v2:

1. **Tres nombres para el mismo servicio.** El masaje anti-estrés aparecía como
   `anti-estrés de espalda` (tabla de calendarios), `Anti-estrés de espalda` /
   `Masaje anti stres de Cuerpo completo` (catálogo, con typo) y
   `Masaje anti-estrés de espalda` / `Masaje cuerpo completo` (tabla de
   duraciones). Al no ser una fila única, nombre, duración y precio se
   recombinaban.
2. **Precio y duración en tablas separadas**, a ~70 líneas de distancia, más
   una tercera tabla para los calendarios. Tres "joins" que el modelo tenía que
   resolver de memoria.
3. **La regla anti-invención sólo cubría el agendado**, no la cotización.

## Qué hace v2

- **Catálogo maestro único**: un renglón por servicio con
  `nombre | duración | precio | ID de calendario`. Sin joins.
- Se elimina la tabla `DURACIÓN EXACTA POR SERVICIO` y la tabla
  `CALENDARIOS POR SERVICIO`; su contenido vive ahora en el catálogo maestro.
- **Regla de cita literal**: obliga a copiar nombre, duración y precio textuales,
  prohíbe combinar campos de servicios distintos e invalida explícitamente
  cualquier dato del historial de la conversación que no esté en el catálogo.

## Discrepancias encontradas al fusionar las tablas

En v1 el catálogo y la tabla de duraciones no coincidían. En v2 se tomó la
tabla de duraciones (la que se usaba para calcular el `end` de la cita):

| Servicio | Catálogo v1 | Duraciones v1 | v2 |
|---|---|---|---|
| Facial antiacné | `2h+` | `2 h 30` | 2 h 30 min |
| Extensión de pestañas | `2-3h` | `3 h` | 3 h |
| Retoque de pestañas | `1-2h` | `2 h` | 2 h |
| Masaje reductivo | `25-30min` | `30 min` | 30 min |

Otros hallazgos:

- **Ceja con diseño** venía listada bajo DEPILACIÓN pero su calendario asignado
  es el de Henna Browns / Laminado de cejas. En v2 se respeta el calendario.
- **Laminado de cejas** tiene calendario asignado pero no tiene duración ni
  precio en ninguna parte del prompt. En v2 queda marcada como "no agendar ni
  cotizar, derivar al contacto humano" en vez de inventarle datos.
- **Fibroblast** ya no lleva ID de calendario: nunca se agenda por WhatsApp.

## Capacitaciones

Lefranm **sí** imparte capacitaciones, pero sus datos (temario, formato,
duracion, precio, fechas, cupo, requisitos) no estan en el prompt. La v1 decia
lo contrario ("NO ofrece cursos, capacitaciones ni talleres de ningun tipo"),
lo que hacia que el asistente negara un servicio real.

En v2 el asistente confirma que si se imparten, no da ningun dato y deriva
siempre al contacto humano con la marca `[AVISAR_HUMANO: ...]`. El cambio toco
cinco puntos del prompt que se contradecian entre si: el bloque
`CURSOS Y CAPACITACIONES`, la `REGLA DE CATALOGO CERRADO` (que afirmaba que el
spa "no ofrece nada" fuera del catalogo), la linea de "tampoco inventes", el
bloque `LIMITES` y la lista de casos que disparan `[AVISAR_HUMANO]`.

## Pendiente

Subir el modelo del módulo. En v1 estaba en `defaultModel: "large"`, que la
etiqueta del blueprint resuelve a **gpt-5-mini con reasoning low** — corto para
un prompt de este tamaño.

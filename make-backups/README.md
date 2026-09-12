# Migración Airtable → Make Data Store (LEFRANM)

## Motivo

El 27/08/2026 los escenarios que usan la base de Airtable `appOrTYs2MmWclqwM`
empezaron a fallar con `RateLimitError [429]` en el módulo
`airtable:ActionSearchRecords`.

- 06:29 CDMX — primer 429 en `LEFRANM SEGUIMIENTO CITAS` (5747451)
- 07:37 CDMX — primer 429 en `LEFRANM CITASS` (5645150), 12 ejecuciones caídas
- El bloqueo duró más de 4 horas y afectó **solo** a esa base. Los escenarios
  sobre otras bases, con la misma conexión de Airtable (`6485517`), siguieron
  funcionando → el límite es **por base**, no por token.

### Confirmado en Airtable (27/08/2026)

Panel del workspace **My First Workspace** (plan Free), donde vive la base
`appOrTYs2MmWclqwM`:

| Métrica | Valor |
|---|---|
| **Llamadas a la API pública (mensuales)** | **5,785 / 1,000** ← en rojo |
| Registros por base | 380 / 1,000 |
| Archivos adjuntos | 4.6 MB / 1 GB |

Consumo real: **5.8x el tope**. La estimación previa a partir de las
ejecuciones de Make (~5,400) resultó correcta.

Las demás bases (`Air Table Chavarria`, `Log_Eventos`, `Lista de clientes`)
viven en el workspace **ASISTENTE**, con su propia cuota. Por eso los
escenarios de cosmeticos siguieron funcionando con la misma conexión de
Airtable mientras los de citas estaban muertos: la cuota es **por workspace**.

Borrar registros viejos NO libera esto: son límites distintos, y de hecho el
de registros está a un tercio de su capacidad.

Ajustar frecuencias tampoco alcanza: apagar por completo el escenario de
seguimiento ahorra ~1,400 llamadas y aun así quedarían ~4,400 contra un tope
de 1,000. Con esos volúmenes solo hay dos salidas: pagar el plan, o sacar la
tabla de Airtable.

### Prueba directa

Escenario temporal de un módulo (una lectura de un registro, sin concurrencia)
corrido a las 11:19 CDMX, casi 5 horas después del primer 429:

```
[429] RateLimitError - airtable: ActionSearchRecords
```

Una petición aislada devolviendo 429 descarta el límite de 5 req/s, que se
libera en ~30 segundos. El escenario temporal fue borrado.

## Estado

| Escenario | ID | Estado |
|---|---|---|
| LEFRANM SEGUIMIENTO CITAS | 5747451 | ✅ Migrado a Data Store |
| LEFRANM CITASS | 5645150 | ✅ Migrado a Data Store |
| LEFRANM COSMETICOS CORECTA (copy) | 5587862 | ⛔ Bloqueado (ver abajo) |
| LEFRANM COSMETICOS SEGUIMIENTO | 5866647 | ⛔ Bloqueado (ver abajo) |

### Infraestructura creada

- Data structure `LEFRANM Seguimiento Citas` — id **475267**
  (`telefono` text, `nombre` text, `ultimo_mensaje` date,
  `cita_agendada` boolean, `seguimiento_enviado` boolean)
- Data store `LEFRANM_Seguimiento_Citas` — id **139497** (5 MB)

## Aplicado: LEFRANM CITASS (5645150)

Se aplicó importando `5645150_LEFRANM_CITASS.after.json` desde el editor de
Make (⋯ → Import Blueprint), no por API: el blueprint pesa 40 KB e incluye
18 KB de system prompt del agente con 13 IDs de calendario y el catálogo de
precios. Transmitirlo por API obligaba a regenerarlo carácter por carácter,
con riesgo de corromper en silencio precios o IDs de calendario. La
importación lo transfiere byte por byte.

Verificado con diff contra el archivo: módulos, mappers y parámetros
idénticos; `systemPrompt` byte por byte igual (18,059 caracteres).

Los dos cambios:

1. **Módulo 32** `airtable:ActionSearchRecords` → `datastore:GetRecord`
   - Data store: `LEFRANM_Seguimiento_Citas`
   - Key: `{{2.contacts[].wa_id}}`
   - Manejador de error `builtin:Resume` con
     `{telefono:"", nombre:"", cita_agendada:false, seguimiento_enviado:false}`
     (esto es lo que evita que la ejecución muera y el cliente se quede sin respuesta)

2. **Rutas 4 y 5 del router 18** (`airtable:ActionCreateRecord` +
   `airtable:ActionUpdateRecords`) → una sola ruta sin filtro con
   `datastore:AddRecord`, `overwrite: true` (upsert):
   - key: `{{2.contacts[].wa_id}}`
   - telefono: `{{2.contacts[].wa_id}}`
   - nombre: `{{2.contacts[].profile.name}}`
   - ultimo_mensaje: `{{now}}`
   - cita_agendada: `{{if(30.cita_agendada; true; if(32.cita_agendada; true; false))}}`
   - seguimiento_enviado: `false`

Las cuatro configuraciones de módulo están validadas contra la API de Make.

### Dos trampas encontradas al aplicarlo

1. **Import crea un escenario nuevo.** La primera importación se hizo desde
   la lista de escenarios y Make creó `LEFRANM CITASS V2` en vez de reemplazar
   el original. Como el webhook `2574977` ("LEFRANM CITAS OFICIAL") seguía
   ocupado por el original, Make le asignó a V2 otro webhook (`2568114`), y los
   mensajes del número real no le llegaban. Hay que importar **dentro** del
   escenario original, que es el dueño del webhook.

2. **Make ignora el `scheduling` del blueprint.** Tras importar, el escenario
   quedó en `indefinitely / 900` (revisar cada 15 min) en vez de `immediately`.
   El bot respondía, pero con hasta 15 minutos de retraso. Se corrigió por API
   con `scenarios_update` pasando solo `scheduling`, sin tocar el blueprint.

`LEFRANM CITASS V2` (6071321) quedó desactivado; se puede borrar.

## Bloqueado: LEFRANM COSMETICOS

La tabla `tblp4g68UDcXYDHX6` (base `appfzByzbpSh9ZUHc`) **no es solo estado de
conversación**: guarda el programa de lealtad de los clientes —
`Tier`, `monto acumulado`, `fecha activacion`, `fecha limite`.

Repuntar los módulos a un Data Store vacío borraría los saldos acumulados y
todos los clientes caerían al tier por defecto (`azul`), en silencio.

Esa base **no está bloqueada** — sus escenarios funcionaron todo el día. No es
urgente y no debe migrarse sin exportar primero los datos.

Además los dos escenarios de cosmeticos deben migrarse **juntos**: 5587862
escribe la tabla y 5866647 la lee. Migrar solo el de seguimiento apagaría los
recordatorios de cosmeticos sin que nadie se entere.

Orden correcto cuando se haga:
1. Crear data structure + data store para cosmeticos (incluir campos de lealtad).
2. Escenario temporal de un solo uso: Airtable Search (todos los registros) →
   Data Store AddRecord. Correrlo y verificar que el conteo coincide.
3. Recién ahí repuntar 5587862 y 5866647.

## Fuera de alcance

`CUT - Seguimiento Prospectos` (6055110) usa otra base (`appdjQSTUD9s41Fbt`) de
otro cliente y no presentó fallos. No se tocó.

---

# LEFRANM COSMETICOS (5587862) — mensaje vacío rechazado por WhatsApp

## Síntoma

`RuntimeError [400] [100] ... JSON field 'text' ... missing: 'body'` en
`whatsapp-business-cloud:sendMessage` (módulo 38). Intermitente: 1 sept 19:15
CDMX y 2 sept 10:21 CDMX. Cada fallo deja a una clienta sin ninguna respuesta.

## Causa raíz

El módulo 60 (`openai-gpt-3:transformTextToStructuredData`, gpt-5.2) limpia las
marcas internas `[ENVIAR_ARCHIVO: ...]` y `[AVISAR_HUMANO: ...]` de la respuesta
del agente y devuelve `mensaje_limpio`. Sus tres campos de salida estaban
declarados `isRequired: false`.

Al ser todos opcionales, el modelo puede devolver un bundle **completamente
vacío** — y eso fue lo que ocurrió (confirmado en el historial: `Output →
Bundle 1: Empty`, con el módulo marcado como completado, sin error).

El módulo 38 mapeaba `{{60.mensaje_limpio}}` directo en `text.body`. Sin ese
campo, el cuerpo iba vacío y Meta rechazaba el envío con 400.

La respuesta del agente sí existía (`{{12.response}}`, entra al 60 como
`rawText`). Se perdía en el paso que solo debía quitarle dos líneas.

## Por qué NO se usó un filtro

La primera propuesta fue filtrar la entrada al módulo 38 cuando
`mensaje_limpio` viniera vacío. Es incorrecta: en Make un filtro que bloquea
detiene **toda la rama posterior**, así que se habrían perdido igual el router,
el envío de PDF, el correo de ficha de compra, la actualización de tier en
Airtable, el escalamiento a humano y la escritura de la pausa. Cambiaba un
fallo ruidoso por uno silencioso.

## Cambios aplicados (3, verificados con diff)

1. **Módulo 60** — `mensaje_limpio` pasa a `isRequired: true`. Ataca la causa:
   el modelo queda obligado a devolver el campo.
2. **Módulo 38** — el cuerpo deja de poder quedar vacío:
   `{{ifempty(60.mensaje_limpio; ifempty(12.response; "<mensaje de respaldo>"))}}`
   Si falta el texto limpio usa la respuesta cruda del agente; si tampoco,
   un mensaje neutro. La clienta siempre recibe algo.
3. **Módulo 38** — manejador de error `builtin:Resume`, para que un fallo de
   envío no tumbe el resto del flujo.

Diff verificado: solo esos tres bloques cambian. `systemPrompt` del agente
intacto (36,433 caracteres), conexiones y webhook intactos. La configuración
del módulo 38 validada contra la API de Make.

## Aplicado y verificado — 2 sept 2026, 11:53 CDMX

Importado dentro del escenario existente. Verificación contra el archivo
preparado:

| Comprobación | Resultado |
|---|---|
| Diff blueprint (servidor vs archivo) | Sin diferencias fuera de `scheduling` |
| `systemPrompt` del agente | Idéntico al original — 36,433 caracteres |
| Webhook | `2575353`, el original |
| Conexiones (WhatsApp, Airtable, agente, OpenAI) | Intactas |
| Módulo 60 · `mensaje_limpio` | `isRequired: true` |
| Módulo 38 · body | `ifempty` con doble respaldo |
| Módulo 38 · onerror | `builtin:Resume` (id 300) |

Make volvió a ignorar el `scheduling` del blueprint y dejó el escenario en
`indefinitely / 900` (sondeo cada 15 min). Corregido por API a `immediately`;
`nextExec` quedó en null, que es lo correcto para un escenario por webhook.

Es la segunda vez que la importación hace esto — conviene revisarlo siempre
después de importar.

---

# Blindaje de LEFRANM COSMETICOS (5587862) — meta: 0 errores

## Auditoría de partida

20 módulos, **solo 2 con manejador de error** (el 200 y el 38). Los otros 18
podían tumbar la ejecución completa, dejando al cliente sin respuesta.

Historial real de caídas de este escenario:

| Fecha | Error | Módulo |
|---|---|---|
| 1 y 2 sept | `[400] missing 'body'` | 38 · WhatsApp |
| 4 sept | `[429] no credits remaining` (OpenAI) | 60/70/42 · OpenAI |
| 5 sept | `Failed to verify connection 'LEFRAN CATALOGO' [400]` | inicialización |

## Criterio aplicado

Antes de blindar, se mapeó qué módulo consume la salida de cuál. Solo se
agregó manejador donde el fallo degrada sin cambiar el comportamiento:

**Terminales — nadie usa su salida, un `Resume` es inocuo:**
61, 43 (envíos WhatsApp), 105, 71 (Gmail), 106, 50, 51 (escrituras Airtable),
201 (Data Store).

**Salida consumida, pero por filtros que exigen `"true"` o `exist`:**
70, 60, 42, 41. Con el `Resume` vacío esos filtros no disparan — que es
exactamente el comportamiento correcto cuando el parser falló.

**Agente (12):** `Resume` con una respuesta de respaldo, para que el cliente
reciba algo en vez de silencio.

**Upsert de Airtable (101):** su único consumidor es el 106, que queda
protegido. El costo de un fallo pasa a ser "un mensaje no se registró", no
"se perdió la conversación".

## Deliberadamente SIN proteger

**Módulo 2 (`airtable:ActionSearchRecords`).** Su salida decide crear vs.
actualizar mediante `{{2.__IMTLENGTH__}}`, y `{{2.id}}` es el `recordId` del
upsert del módulo 101. Un `Resume` ahí dejaría `__IMTLENGTH__` indefinido y el
upsert podría **crear registros duplicados de clientes**. Eso sí cambiaría el
funcionamiento, así que se dejó como está.

Es el único módulo cuyo fallo todavía mata la conversación. La solución de
fondo es la misma que se aplicó en citas —sacar esa tabla de Airtable— pero
requiere migrar antes los saldos del programa de lealtad.

Los módulos 1 (trigger), 90 y 52 (routers) no admiten manejador de error.

## Resultado

**Cobertura: 16 de 20 módulos** (17 de 17 protegibles, menos el 2 por decisión).

Diff verificado: **71 claves cambian y todas están dentro de bloques
`onerror`**. Cero cambios fuera de eso. `systemPrompt` del agente intacto,
mapper del módulo 38 intacto, todas las conexiones intactas.

## Riesgo pendiente: cuota de Airtable del workspace ASISTENTE

Cosmeticos gasta ~2-3 llamadas de Airtable por conversación, y
`LEFRANM COSMETICOS SEGUIMIENTO` sondea cada 30 min (~1,440 búsquedas al mes
por sí solo). Es la misma aritmética que tumbó a citas el 27 de agosto contra
un tope de 1,000 llamadas/mes del plan gratuito.

Conviene revisar el contador de API del workspace **ASISTENTE** en Airtable
antes de que reviente igual.

---

# Los PDF llegan a WhatsApp como `BIN` en vez de PDF

**Síntoma reportado por el cliente (12 sep 2026):** el catálogo principal no
abre directo en el teléfono. WhatsApp lo muestra como

```
Catalogo-Lefranm.pdf
75 MB  •  BIN
```

y al tocarlo Android ofrece "Abrir con → Billetera de Google / Google /
vista previa de archivo", ninguna de las cuales lee PDF. De ahí el error de
Google AR que mandó el cliente.

## Causa

`BIN` es la etiqueta que pone WhatsApp cuando recibe
`Content-Type: application/octet-stream`.

Los dos módulos que mandan documentos usan URLs de Drive con el endpoint de
descarga:

| Módulo | Qué manda | Origen del link |
|---|---|---|
| 61 | catálogo / fichas (lo elige el agente) | `{{60.pdf_url}}` |
| 43 | listas de precios (roja / verde / azul) | URLs fijas en el mapper |

Todas con la forma:

```
https://drive.google.com/uc?export=download&id=FILE_ID
```

`uc?export=download` es un endpoint de **descarga**, no de publicación.
Responde a propósito con `Content-Type: application/octet-stream` y
`Content-Disposition: attachment` para que el navegador guarde el archivo en
vez de abrirlo. WhatsApp copia ese Content-Type tal cual al mensaje.

La extensión `.pdf` del nombre no salva nada: Android decide con qué app
abrir según el MIME, no según el nombre.

**Los archivos están bien.** En Drive los seis son `application/pdf`
correctos. Lo que está mal es la URL por la que se entregan.

## Inventario real de los PDF (metadata de Drive, 12 sep 2026)

| Archivo | ID | Bytes | Tamaño |
|---|---|---:|---:|
| Catálogo Lefranm Interactivo.pdf | `1bNnhW8Z_paykFNKXOLYppF8xNlT8NWp5` | 75,057,202 | **71.6 MiB** |
| Fichas Tecnicas Lefranm.pdf | `1R8sErJz0sethdGPSlKiDjeJT-ZSTH1e0` | 42,886,202 | **40.9 MiB** |
| Lista de Precios Mayor a 10,000.pdf | `19XRzcbYiqsGX_szuwpQvq6guRTMv-mYu` | 691,863 | 676 KiB |
| Lista-de-Precios-Cosmetologas-y-Esteticas.pdf | `1g7e4AnE-EMsfbOxcC0xeadmk-lxaV8Hg` | 689,658 | 673 KiB |
| Lista de Precios al Público.pdf | `1T6SQKhXpbM_w05v8pCAY89nEQd1hCoxC` | 686,156 | 670 KiB |
| Kit de distribuidor inical 25 productos.pdf | `1THmrKQt7_s67amVE9ptjC_bfGXdaLkNR` | 200,218 | 195 KiB |

Todos en la carpeta `1u7-YJ8P96xlmG5iSyeo07ABPrqiWqOfq`.

## Segundo problema, independiente del MIME: el peso

El catálogo pesa **110 veces** más que una lista de precios. Aunque se
arregle el Content-Type, 71.6 MiB por datos móviles es una descarga que
mucha gente va a abandonar o que se va a cortar. El tope de WhatsApp Cloud
API para documentos es 100 MB, así que pasa raspando.

Objetivo razonable para un catálogo: **4-8 MB**. El peso casi siempre viene
de imágenes incrustadas a 300 dpi; reexportar a calidad web lo resuelve.

Los dos archivos que hay que comprimir son el catálogo (71.6 MiB) y las
fichas técnicas (40.9 MiB). Los otros cuatro ya están bien de tamaño.

## Arreglos posibles

### A. Hospedar los PDF fuera de Drive (recomendado)

Cualquier servidor web normal sirve un `.pdf` como `application/pdf`. El
sitio propio, `www.cosmeticoslefranm.com`, es Wix (se ve por las rutas
`/product-page/...` que ya aparecen ~14 veces en el prompt del agente). El
Administrador de medios de Wix hospeda documentos y entrega URLs
`...filesusr.com/ugd/....pdf` que sí declaran `application/pdf`.

Una vez subidos, se cambian las URLs en los módulos 61 y 43. Sin caducidad,
sin mantenimiento.

### B. Mandar por `media_id` en vez de `link`

La app de WhatsApp Business Cloud en Make tiene el módulo
`uploadMedia` ("Upload a Media"), que permite declarar el MIME explícito.
Se sube el PDF una vez, WhatsApp devuelve un `media_id`, y el módulo de
envío usa `document.id` en lugar de `document.link`.

Ventaja: el MIME queda garantizado y ya no depende de ningún host externo.
Desventaja: WhatsApp conserva los archivos subidos **30 días**, así que hay
que volver a subirlos con un escenario mensual. Es mantenimiento recurrente.

### C. Probar `export=view` (rápido, pero no sirve para los grandes)

```
https://drive.usercontent.google.com/uc?id=FILE_ID&export=view
```

`export=view` pide a Drive que sirva el archivo en línea con su Content-Type
real en vez de forzar descarga. **Sin verificar:** este entorno tiene
`drive.google.com` bloqueado por el proxy (403 en CONNECT), así que no se
pudieron leer las cabeceras HTTP desde aquí. Cuesta dos minutos probarlo con
una lista de precios.

Aunque funcione, **no sirve para el catálogo ni para las fichas**: arriba de
25 MB Drive mete una página intermedia de "no se pudo analizar en busca de
virus" en vez del archivo.

## Orden recomendado

1. Comprimir catálogo y fichas técnicas a 4-8 MB. Esto hay que hacerlo
   con cualquiera de los tres arreglos.
2. Rehospedar (opción A) o probar `export=view` (opción C) en una lista de
   precios chica para confirmar el diagnóstico.
3. Cambiar las URLs en los módulos 61 y 43.

---

# Se perdió el acceso de API a la cuenta de Make de Lefranm

**Detectado el 12 sep 2026.** El conector de Make ya no apunta a la cuenta
donde viven los escenarios de Lefranm.

`environment_get` devuelve ahora:

```
zona:         eu2.make.com
organización: 5601227  "My Organization"
equipo:       2904200  "My Team"
```

Ese equipo contiene los escenarios de **Tersil** (`Asistente Tersil`,
`Asistente Tersil V2`, `Tersil - Seguimiento 10 h`, ...), no los de Lefranm.

Lefranm vive en organización **5357289** / equipo **1436402**, que este token
ya no alcanza. Cualquier llamada contra 1436402 responde:

```
MakeApiError: Insufficient rights, admin permission "organization view" is needed.
```

`users_me` sí funciona y devuelve la misma persona
(`bombochoabril@gmail.com`), o sea que el token es válido — simplemente está
autorizado contra la otra cuenta/zona.

**Consecuencia:** desde aquí ya no se puede leer el blueprint de 5587862, ni
aplicar `5587862_v4.blindado.json`, ni revisar el estado de la conexión
`LEFRAN CATALOGO`. Para recuperarlo hay que volver a autorizar el conector de
Make contra la cuenta donde está Lefranm.

---

# Verificación de `5587862_v4.blindado.json` (12 sep 2026)

Contrastado módulo por módulo contra `5587862_v3.actual.json`:

| Comprobación | Resultado |
|---|---|
| JSON válido | sí |
| Módulos principales | 20 en ambos, mismos IDs |
| Manejadores `onerror` | 2 → **16** (14 nuevos) |
| `systemPrompt` módulo 12 | 36,433 chars, `sha256 4cc058e0…` **idéntico** |
| Prompts módulos 70 / 60 / 42 / 41 | idénticos (826 / 914 / 1506 / 1289 chars) |
| Conexiones | `10484205, 6001715, 6485517, 9880453` — iguales |
| Webhook | `2567974` — igual |
| Mappers modificados | **ninguno** |
| Filtros modificados | **ninguno** |

Se puede importar con confianza: solo agrega manejadores de error.

## Hallazgo: `LEFRAN CATALOGO` ya no aparece en este escenario

Las cuatro conexiones del blueprint son `10484205` (Gmail), `6001715`
(OpenAI), `6485517` (Airtable) y `9880453` (WhatsApp). **La conexión rota
`9795318` (`LEFRAN CATALOGO`) no está.** Los tres módulos de WhatsApp —38
(texto), 61 (catálogo/fichas) y 43 (listas)— usan los tres `9880453`.

Si el blueprint capturado refleja el estado vivo, esa conexión rota ya dejó
de ser un problema para 5587862. No se pudo confirmar contra Make porque el
token de API ya no alcanza esa cuenta.

---

# Arreglo del MIME sin mover los PDF de Drive

`www.googleapis.com` **sí** responde desde este entorno (a diferencia de
`drive.google.com`, que el proxy bloquea). El endpoint de la API de Drive

```
https://www.googleapis.com/drive/v3/files/FILE_ID?alt=media&key=API_KEY
```

entrega el archivo con su `Content-Type` real —`application/pdf`— en vez de
`application/octet-stream`. Probado sin credenciales devuelve
`403 Method doesn't allow unregistered callers`, o sea que el endpoint está
vivo y lo único que falta es una API key.

**Los seis PDF ya cumplen el requisito:** `get_file_permissions` devuelve
`{"role":"reader","type":"anyone"}` en los seis. Son públicos por link.

Ventajas sobre rehospedar: los archivos se quedan en Drive, no hay que
subir nada, no caduca nada, y **no aplica el corte de 25 MB** de la página
de análisis de virus, así que sirve igual para el catálogo de 71.6 MB.

## Por qué basta con cambiar dos campos

El agente nunca le enseña la URL al cliente. La emite como marca interna al
final de su respuesta:

```
[ENVIAR_ARCHIVO: <url> | <archivo>.pdf]
```

y el prompt dice textualmente *"el cliente nunca debe ver esta línea, un
proceso interno la retira antes de enviar tu mensaje"*. El módulo 60 la
extrae a `pdf_url` / `pdf_filename`.

Por eso no hace falta tocar el `systemPrompt` (36,433 chars, con 8 URLs
dentro): basta con reescribir la URL en el momento del envío, en los dos
módulos que mandan documentos.

### Módulo 61 — campo `document.link`

```
{{replace(trim(60.pdf_url); "https://drive.google.com/uc?export=download&id="; "https://www.googleapis.com/drive/v3/files/")}}?alt=media&key=TU_API_KEY
```

### Módulo 43 — campo `document.link`

Se envuelve el `if()` que ya existe, sin tocarlo por dentro:

```
{{replace(trim(<el if() actual, sin las llaves>); "https://drive.google.com/uc?export=download&id="; "https://www.googleapis.com/drive/v3/files/")}}?alt=media&key=TU_API_KEY
```

El `trim()` además corrige un riesgo latente: si el agente deja un espacio
al final de la URL, hoy se manda con el espacio pegado.

## Cómo sacar la API key

1. `console.cloud.google.com` → crear un proyecto.
2. *APIs y servicios → Biblioteca* → buscar **Google Drive API** → Habilitar.
3. *Credenciales → Crear credenciales → Clave de API*.
4. Restringirla a **Google Drive API** (botón *Restringir clave*).

Es gratis. La cuota de la API de Drive (20,000 peticiones por 100 s) queda
lejísimos del volumen de este bot.

## `5587862_v5.pdf-mime-fix.PLANTILLA.json`

Es `v4` con esos dos campos ya reescritos, pero con el literal
`PEGA_AQUI_TU_API_KEY` en lugar de la clave.

> ⚠️ **No importar tal cual.** Sin la clave real, los seis PDF responderían
> 403 y el cliente no recibiría nada — peor que hoy, donde al menos llegan
> aunque salgan como `BIN`. Hay que sustituir las dos apariciones de
> `PEGA_AQUI_TU_API_KEY` antes de importar.

Diff contra `v4`, verificado: **cambian exactamente dos claves**,
`61.mapper.document.link` y `43.mapper.document.link`. El router 90 aparece
distinto solo porque contiene a esos dos como hijos; en sí mismo es
idéntico. `systemPrompt` intacto (`sha256 4cc058e0…`), conexiones intactas,
webhook intacto, los 16 `onerror` intactos.

## Esto no quita que haya que comprimir

El arreglo de MIME hace que el PDF **abra**. No hace que pese menos. El
catálogo de 71.6 MB y las fichas de 40.9 MB siguen siendo descargas que
mucha gente va a abandonar por datos móviles. Las dos cosas son
independientes y las dos hacen falta.

---

# Revisión con acceso restaurado — 12 sep 2026

El conector de Make volvió a apuntar a la cuenta correcta:
`us2.make.com`, organización **5357289**, equipo **1436402**.

## 1. El escenario está en 0 errores

`executions_list` sobre 5587862: **todas las ejecuciones visibles tienen
`status: 1` (éxito)**. Ni un solo `status 3` (error) ni `status 2`
(advertencia). La más reciente, hoy 19:41 UTC, 11 operaciones, 18.3 s.

El arreglo del cuerpo vacío (módulo 60 con `isRequired` + la cascada
`ifempty` en el 38) funcionó. La meta de 0 errores ya está cumplida en la
práctica; lo que queda es blindaje y el defecto de los PDF.

## 2. Mi captura `v3` estaba equivocada en lo más delicado

Al comparar el blueprint vivo contra `5587862_v3.actual.json`:

| | v3 (mi captura) | **vivo** |
|---|---|---|
| Webhook (módulo 1) | 2567974 — *"LEFRANM CITAS"* | **2547718 — *"Lefran Cosmeticos"*** |
| Conexión WhatsApp (38, 43, 61) | 9880453 — *"LEFRANM CITAS"* | **9795431 — *"Lefran Cosmeticos"*** |

Mi captura apuntaba al webhook y a la conexión **de citas**. Importar
`v4` o `v5` habría puesto el bot de cosméticos a escuchar el webhook de
citas y a responder por la conexión de citas.

**Por eso `5587862_v4.blindado.json` y `5587862_v5.pdf-mime-fix.json`
quedan obsoletos y no se deben importar.** El archivo bueno es
`5587862_v6.FINAL.json`, construido sobre el blueprint vivo.

El resto del blueprint sí coincidía: `systemPrompt` con el mismo
`sha256 4cc058e0…`, mismos 22 módulos, mismos mappers y filtros.

## 3. `LEFRAN CATALOGO` no la usa nadie

`connections_list` devuelve para la conexión `9795318` (`LEFRAN CATALOGO`):

```
"scenarioUsages": []
```

**Cero escenarios.** No puede estar causando errores. Dije varias veces que
hacía falta reautorizarla con Facebook; era innecesario. Se puede borrar.

Conexiones de WhatsApp sin usar, todas del mismo número
`Lefranm Beaute ok (1570246936970929)`:

| ID | Nombre | Uso |
|---|---|---|
| 9795318 | LEFRAN CATALOGO | ninguno |
| 9795807 | LEFRAN CITAS | ninguno |
| 9880453 | LEFRANM CITAS | ninguno |
| 9880986 | LEFRANM CITASS | ninguno |
| **9795431** | **Lefran Cosmeticos** | **5587862 y 5866647** |

Y `9908117` (`LEFRANM CITAS OFICIAL`, número `salud y belleza`) es la que
usan los dos escenarios de citas. También sobra `6108362`
(`My Airtable Token NARANJO`), expirada desde el 31 de enero y sin uso.

## 4. `5587862_v6.FINAL.json`

Construido sobre el blueprint vivo, con dos cambios y nada más:

| Cambio | Detalle |
|---|---|
| 14 manejadores `onerror` nuevos | ids 301–314, sobre los módulos 12, 41, 42, 43, 50, 51, 60, 61, 70, 71, 101, 105, 106, 201 |
| 2 campos `document.link` | módulos 61 y 43 |

Verificado contra el vivo:

| Comprobación | Resultado |
|---|---|
| Módulos preexistentes cuyo cuerpo cambia | **solo 43 y 61**, y solo su `mapper` |
| Conexiones | `10484205, 6001715, 6485517, 9795431` — iguales |
| Webhook | `2547718` — igual |
| `scheduling` | `immediately, 100/min` — igual |
| Nombre | `LEFRANM COSMETICOS CORECTA (copy)` — igual |
| `systemPrompt` y los 4 prompts | `sha256` idénticos |
| Total de `onerror` | 2 → **16** |

### La fórmula se desarma sola

```
{{if(substring("PEGA_AQUI_TU_API_KEY"; 0; 4) = "AIza";
     replace(trim(60.pdf_url); "<url vieja>"; "<url nueva>") + "?alt=media&key=" + "PEGA_AQUI_TU_API_KEY";
     trim(60.pdf_url))}}
```

Mientras el marcador siga ahí, `substring(...) = "AIza"` es falso y se usa
la URL de siempre: **el escenario se comporta exactamente como hoy**. En
cuanto se sustituye el marcador por una clave real de Google (todas empiezan
con `AIza`), la condición se vuelve verdadera y cambia sola a la URL de la
API de Drive, que entrega `application/pdf`.

O sea que se puede importar hoy sin clave, sin riesgo, y activar el arreglo
del MIME después.

Simulado en los cuatro casos —con y sin clave, con y sin espacio al final de
la URL— y da el resultado correcto en los cuatro.

### Por qué no se subió por API

El blueprint son 68,319 caracteres, de los cuales **36,433 son el
`systemPrompt`** con el catálogo y los precios dentro. `scenarios_update`
reemplaza el blueprint entero, así que subirlo por API obliga a transcribir
ese prompt carácter por carácter. Sobre un bot de ventas en vivo eso no vale
la pena: el import por archivo desde la interfaz de Make es byte-exacto.

> Al importar, hacerlo **dentro del escenario** (abrir 5587862 → menú "…" →
> *Import Blueprint*), nunca desde la lista de escenarios. Desde la lista,
> Make crea un escenario nuevo con un webhook nuevo — es exactamente lo que
> pasó el 30 de agosto y dejó el huérfano `LEFRANM CITASS V2`.
>
> Make además reinicia el `scheduling` al importar. Después del import hay
> que confirmar que siga en *Immediately*.

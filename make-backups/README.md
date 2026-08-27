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

Volumen estimado sobre esa base: ~5,400 llamadas/mes contra un tope de 1,000
del plan gratuito de Airtable.

Borrar registros viejos NO libera esto: el tope de 1,000 registros por base y
el tope de 1,000 llamadas de API al mes son límites distintos.

## Estado

| Escenario | ID | Estado |
|---|---|---|
| LEFRANM SEGUIMIENTO CITAS | 5747451 | ✅ Migrado a Data Store |
| LEFRANM CITASS | 5645150 | ⏳ Blueprint preparado, sin aplicar |
| LEFRANM COSMETICOS CORECTA (copy) | 5587862 | ⛔ Bloqueado (ver abajo) |
| LEFRANM COSMETICOS SEGUIMIENTO | 5866647 | ⛔ Bloqueado (ver abajo) |

### Infraestructura creada

- Data structure `LEFRANM Seguimiento Citas` — id **475267**
  (`telefono` text, `nombre` text, `ultimo_mensaje` date,
  `cita_agendada` boolean, `seguimiento_enviado` boolean)
- Data store `LEFRANM_Seguimiento_Citas` — id **139497** (5 MB)

## Pendiente: LEFRANM CITASS (5645150)

Blueprint listo en `5645150_LEFRANM_CITASS.after.json`. Dos cambios:

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

Hasta que esto se aplique, `LEFRANM SEGUIMIENTO CITAS` lee un Data Store vacío
y no manda recordatorios. Tampoco los mandaba antes: Airtable llevaba horas
devolviendo 429.

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

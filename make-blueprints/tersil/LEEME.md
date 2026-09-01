# Tersil — Blueprints actualizados (Make)

> **Estado actual (1 sep 2026):** ya aplicado en la cuenta `bombochoabril@gmail.com` (zona eu2, team 2904200).
>
> | Recurso | Estado |
> |---|---|
> | Data store `TERSIL_Seguimiento` (id **182352**) | ✅ creado |
> | Escenario `Tersil - Seguimiento 23 h` (id **9738949**) | ✅ creado, cada 30 min, **desactivado** |
> | `Asistente Tersil V2` (id **9597789**) — reloj | ✅ regresado a "inmediatamente" |
> | `Asistente Tersil V2` — data store en los 2 módulos nuevos | ⚠️ **pendiente, 2 clics en la UI** |

## Lo único que falta

En **Asistente Tersil V2**, abre estos dos módulos y en "Data store" elige **TERSIL_Seguimiento**:

1. **"Registrar para seguimiento"** (va justo después de mandar el mensaje de WhatsApp)
2. **"Sacar de seguimiento"** (el último, después del correo)

Verifica que en "Registrar para seguimiento" queden mapeados:
`nombre` = nombre del contacto · `telefono` = wa_id · `ultimo_mensaje` = `{{now}}` · `ultimo_seguimiento` = `{{now}}` · `seguimientos` = `0`

Guarda. Después, activa el escenario `Tersil - Seguimiento 23 h`.

---

## Qué hace cada cosa

**Seguimiento cada 23 h**
- Cada 30 min busca clientes con 23 h sin escribir y les manda un recordatorio.
- Hasta 3 seguimientos, uno cada 23 h (≈23 h, 46 h y 69 h). Después los saca de la lista.
- Si el cliente contesta, el contador se reinicia solo.
- Si el cliente ya hizo pedido (bot pausado), deja de seguirlo.

**Datos de pago directos**
- Ya no pregunta "¿cómo prefieres pagar?": manda A) SPEI y B) OXXO juntos, con el monto exacto.
- El comprobante se pide en la misma conversación, sin mandar a otros números.

**Bienvenida más aireada**
- Bloques separados con renglones en blanco + regla general de formato para todos los mensajes.

---

## Ojo con la ventana de 24 h de WhatsApp

WhatsApp solo deja mandar mensajes libres dentro de las 24 h siguientes al último mensaje **del cliente**.

- **Seguimiento 1 (23 h): siempre entra.** Por eso son 23 h y no 24.
- **Seguimientos 2 y 3:** solo se entregan si el cliente contestó en el intermedio. Si nunca contestó, WhatsApp los rechaza.
- El escenario ya está preparado: marca el registro **antes** de enviar y cada envío tiene manejo de errores "Ignore", así que un rechazo no se repite ni apaga el escenario.
- Si quieres que los seguimientos 2 y 3 lleguen siempre, hay que cambiarlos por **plantillas aprobadas** de WhatsApp.

---

## Ojo al reimportar un blueprint

Al importar, Make **borra el reloj del escenario** y lo deja en "cada 15 minutos". Si vuelves a importar el asistente, acuérdate de regresarlo a **"Immediately as data arrives"**, o el bot contestará con retraso.

## Para cambiar cosas

- **Textos de seguimiento:** en los 3 módulos de WhatsApp del escenario de seguimiento (rutas 1, 2 y 3).
- **Intervalo:** en el módulo "Clientes con 23 h sin responder", las dos condiciones `{{addHours(now; -23)}}`. Cambia el `-23` en ambas.
- **Cuántos seguimientos:** la condición `seguimientos < 3` del mismo módulo.

## Archivos

| Archivo | Qué es |
|---|---|
| `1-Asistente_Tersil_V2.blueprint.json` | El asistente actualizado, ya con el data store 182352 asignado |
| `2-Tersil_Seguimiento_23h.blueprint.json` | El escenario de seguimiento (copia de respaldo; ya está creado en la cuenta) |

## Estructura del data store `TERSIL_Seguimiento`

| Campo | Tipo |
|---|---|
| `nombre` | Text |
| `telefono` | Text |
| `ultimo_mensaje` | Date |
| `ultimo_seguimiento` | Date |
| `seguimientos` | Number |

# Tersil — Blueprints actualizados (Make)

Dos archivos para importar:

| Archivo | Qué es |
|---|---|
| `1-Asistente_Tersil_V2.blueprint.json` | El asistente de siempre, ya actualizado (reemplaza el actual) |
| `2-Tersil_Seguimiento_23h.blueprint.json` | Escenario nuevo de seguimiento cada 23 horas |

---

## Cambios incluidos

**1. Escenario de seguimiento cada 23 h** (igual al de Lefranm, pero con reintentos)
- Cada 30 min busca clientes que llevan 23 h sin escribir y les manda un recordatorio.
- Manda hasta 3 seguimientos, uno cada 23 h (≈23 h, 46 h y 69 h). Después los saca de la lista.
- Si el cliente contesta, el contador se reinicia solo.
- Si el cliente ya hizo su pedido (bot pausado), deja de seguirlo automáticamente.

**2. Datos de pago directos**
- Ya no pregunta "¿cómo prefieres pagar?".
- Al confirmar la ficha manda de golpe: A) Transferencia SPEI y B) Depósito OXXO, con el monto exacto.
- Ya no manda a otros números: "Una vez que realices tu pago, por favor envíanos aquí mismo tu comprobante…".

**3. Mensaje de bienvenida más aireado**
- Bloques separados con renglones en blanco + regla general de formato para todos los mensajes del bot.

---

## Cómo instalarlo (15 min)

### Paso 1 — Crear el data store `TERSIL_Seguimiento`
En Make: **Data stores → Add data store**
- Nombre: `TERSIL_Seguimiento`
- Data structure: crear una nueva con estos campos **exactamente así** (los nombres importan):

| Nombre del campo | Tipo | Requerido |
|---|---|---|
| `nombre` | Text | no |
| `telefono` | Text | no |
| `ultimo_mensaje` | Date | no |
| `ultimo_seguimiento` | Date | no |
| `seguimientos` | Number | no |

### Paso 2 — Importar el asistente actualizado
Abre el escenario **Asistente Tersil V2** → menú `…` → **Import Blueprint** → sube `1-Asistente_Tersil_V2.blueprint.json`.

Después de importar, abre estos 2 módulos nuevos y selecciona en cada uno el data store `TERSIL_Seguimiento`:
- **"Registrar para seguimiento"** (va después de mandar el mensaje de WhatsApp)
- **"Sacar de seguimiento"** (el último, después del correo)

Verifica que los campos del registro queden mapeados así en "Registrar para seguimiento":
`nombre` = nombre del contacto · `telefono` = wa_id · `ultimo_mensaje` = `{{now}}` · `ultimo_seguimiento` = `{{now}}` · `seguimientos` = `0`

### Paso 3 — Crear el escenario de seguimiento
**Create a new scenario** → menú `…` → **Import Blueprint** → sube `2-Tersil_Seguimiento_23h.blueprint.json`.

Selecciona el data store `TERSIL_Seguimiento` en estos 4 módulos:
- "Clientes con 23 h sin responder" (el primero)
- "Marcar seguimiento 1"
- "Marcar seguimiento 2"
- "Cerrar seguimiento"

(el módulo "¿Bot pausado?" ya apunta solo a `TERSIL_Pausa_Bot`)

### Paso 4 — Programar y activar
En el reloj del primer módulo: **Every 30 minutes** (`Run scenario: at regular intervals → 30 minutes`). Guarda y **activa** el escenario.

---

## Ojo con la ventana de 24 h de WhatsApp

WhatsApp solo deja mandar mensajes libres dentro de las 24 h siguientes al último mensaje **del cliente**.

- **Seguimiento 1 (23 h): siempre entra.** Por eso son 23 h y no 24.
- **Seguimientos 2 y 3:** solo se entregan si el cliente contestó en el intermedio (eso reabre la ventana). Si nunca contestó, WhatsApp los rechaza.
- El escenario ya está preparado para eso: marca el registro **antes** de enviar y el envío tiene manejo de errores "Ignore", así que un rechazo no repite el intento ni apaga el escenario.
- Si quieres que los seguimientos 2 y 3 lleguen siempre, hay que cambiar esos dos módulos por **plantillas (templates) aprobadas** de WhatsApp.

## Para cambiar los textos de seguimiento
Están en los 3 módulos de WhatsApp del escenario de seguimiento (rutas 1, 2 y 3). Se editan directo ahí.

## Para cambiar el intervalo
Está en el módulo "Clientes con 23 h sin responder", en las dos condiciones `{{addHours(now; -23)}}`. Cambia el `-23` en ambas.

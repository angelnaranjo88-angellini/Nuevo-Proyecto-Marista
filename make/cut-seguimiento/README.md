# CUT - Seguimiento Prospectos (Make, id 6055110)

Escenario de seguimiento: cada 30 minutos busca en Airtable prospectos que no
han recibido seguimiento y les manda un WhatsApp para reactivar la conversación.

Flujo: Airtable *Search Records* (1) → WhatsApp *sendMessage* (2) → Airtable
*Update Records* (3, marca `Seguimiento enviado`).

## El escenario se desactivaba solo

Las tres ejecuciones del 26/08 fallaron con el mismo error:

```
[400] [100] The parameter to is required.
Módulo: whatsapp-business-cloud → sendMessage
```

WhatsApp rechazaba el envío porque `to` llegaba vacío. Con `maxErrors: 3` en el
escenario, tres fallos seguidos bastan para que Make lo apague.

**Causa.** El filtro de Airtable usaba `{Telefono}!=""` para excluir registros sin
teléfono. En Airtable esa comparación no descarta las celdas vacías de forma
confiable, así que la búsqueda devolvía registros sin número y el primero de
ellos tumbaba la corrida completa (2 operaciones: búsqueda + intento de envío).

## Arreglo

1. **Fórmula de búsqueda**: `{Telefono}!=""` → `LEN({Telefono}&"")>=10`. El `&""`
   fuerza el valor a texto (funciona igual si el campo es número o teléfono) y el
   `>=10` descarta además números incompletos que WhatsApp rechazaría.
2. **Filtro en el módulo 2** ("Tiene telefono"): el envío solo corre si
   `{{1.Telefono}}` existe y no está vacío. Red de seguridad por si algún registro
   se cuela.
3. **Manejador de error `Skip`** en el módulo 2: si un envío falla (número dado de
   baja, ventana de 24 h de WhatsApp vencida), se descarta ese registro y el
   escenario sigue con los demás en vez de morir y desactivarse.

## Qué vigilar

WhatsApp solo permite mensajes de texto libre dentro de las **24 horas** desde el
último mensaje del cliente; fuera de esa ventana hay que usar una plantilla
aprobada. La fórmula ya acota el seguimiento a registros de entre 3 y 20 horas,
que cae dentro de la ventana. Si en el futuro se amplía ese rango, los envíos
empezarán a fallar con el error 131047.

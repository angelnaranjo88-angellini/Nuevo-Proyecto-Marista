# Simplificación del proceso de compra — 17 nov 2026

Los clientes se quejaron de que comprar es tedioso. Se revisó el prompt del
módulo 12 y el flujo completo de cierre de pedido.

## Dónde se iba el tiempo

Contando los mensajes que el CLIENTE tenía que escribir para una compra nueva
con envío a domicilio:

| # | El cliente escribe | Por qué |
|---|---|---|
| 1 | "hola" | |
| 2 | "personal" | DETECCIÓN DE INTENCIÓN era paso obligatorio *antes* de contestar nada |
| 3 | qué productos quiere | |
| 4 | "sí" | acepta la cotización |
| 5 | "envío" | FORMA DE ENTREGA |
| 6 | nombre | ← |
| 7 | calle y número | ← |
| 8 | colonia y C.P. | ← **seis mensajes solo de datos** |
| 9 | ciudad y estado | ← |
| 10 | referencias | ← |
| 11 | correo electrónico | ← |
| 12 | "sí" | confirmación previa a la ficha |
| 13 | "sí" | confirmación *después* de la ficha |

Trece mensajes. Y eso en el mejor caso, sin dudas ni correcciones.

### Las cinco causas concretas

**1. La regla de estilo convertía el checkout en un interrogatorio.**
El prompt decía: *"Si necesitas varios datos, pide uno o dos a la vez, de forma
conversacional"*. Para conversar está bien. Para cobrar es fatal: son 6-7 datos,
o sea 4-6 mensajes del cliente después de que ya dijo que sí.

**2. Doble confirmación.** `DATOS QUE DEBES RECOPILAR` punto 6 pedía confirmar
el total *antes* de armar la ficha, y la sección `FICHA DE COMPRA` volvía a
preguntar *"¿Confirma que toda la información es correcta...?"* después. El
cliente decía que sí dos veces para lo mismo.

**3. El correo electrónico se pedía en un mensaje aparte.** El dato sí se
necesita (el dueño manda por ahí el rastreo del paquete), pero preguntarlo solo
costaba una ida y vuelta más. Ahora va dentro de la misma plantilla.

**4. Se respondía una pregunta con otra pregunta.** `DETECCIÓN DE INTENCIÓN`
era *"paso obligatorio al iniciar una venta"*. Si alguien escribía "¿cuánto
cuesta la crema limpiadora?", lo primero que recibía era *"¿es para uso personal
o busca precio de distribuidora?"*.

**5. La dirección no se guardaba.** La base de datos
(`LEFRANM_Cosmeticos_Clientes`, estructura 544490) tenía 9 campos —tier, nombre,
teléfono, montos y fechas— y **ninguno de dirección**. Un cliente que ya había
comprado tres veces dictaba su dirección completa las tres veces.

## Qué se cambió

### En el prompt (9 ediciones quirúrgicas)

| # | Edición | Efecto |
|---|---|---|
| 1 | Excepción de checkout en ESTILO DE MENSAJE | los datos de envío se piden en **un solo mensaje** |
| 2 | DETECCIÓN DE INTENCIÓN | si ya preguntaron un precio, **se contesta primero** |
| 3 | FORMA DE ENTREGA | plantilla para copiar y llenar de un jalón |
| 4 | DATOS QUE DEBES RECOPILAR | sin teléfono, **sin doble confirmación** |
| 5 | FICHA DE COMPRA | dirección en una línea en vez de siete campos |
| 6 | Nota de omisión de la ficha | coherente con lo anterior |
| 7 | Buen Fin regla 4 | los dos totales **una vez**, no en cada cotización |
| 8 | Formato del CONTEXTO_INTERNO | agrega `direccion_guardada=` |
| 9 | CONTEXTO INTERNO DEL CLIENTE | **reutiliza la dirección** de quien ya compró |

La plantilla que ahora ve el cliente:

```
¡Perfecto! 😊 Para mandárselo, ¿me copia y llena estos datos en un solo mensaje?

Nombre completo:
Calle y número:
Colonia:
C.P.:
Ciudad y estado:
Correo electrónico:
Referencias (opcional):
```

### En el escenario

| Módulo | Cambio |
|---|---|
| 41 | extrae `direccion_envio` y `correo_cliente` de la ficha |
| 106 | los guarda al cerrar la compra, con `ifempty` para no pisar una dirección buena cuando la compra fue recolección en sucursal |
| **101** | **arrastra ambos campos** |
| 12 | pasa `direccion_guardada=` al agente |

### En la base de datos

Estructura 544490 ampliada de 9 a 11 campos: `direccion_envio` y `correo`
(ambos `text`). Los 9 originales quedaron idénticos. Aplicado por API.

> ⚠️ **El módulo 101 tiene `overwrite: true`** y reescribe el registro completo
> en cada mensaje entrante. Si se agregan campos a la estructura y no se
> incluyen también en el 101, se borran solos en el siguiente mensaje del
> cliente. Por eso el 101 los arrastra con `{{2.direccion_envio}}` y
> `{{2.correo}}`.

## Cómo queda

Compra nueva con envío: **de 13 mensajes a 7**.

Cliente que ya compró antes: alrededor de **4**, porque el bot ya sabe su tier
(no pregunta personal/distribuidora) y ya tiene su dirección — solo la confirma
en una línea y pasa directo a la ficha.

## Verificación

Nueve bloques de cambio en el diff del prompt, uno por edición. Nada más se
movió:

| | antes | después |
|---|---:|---:|
| Referencias al catálogo (`LF-0`) | 93 | 93 |
| CLABE | 1 | 1 |
| Kit de Distribuidor | 3 | 3 |
| Bloque Buen Fin | 3 | 3 |
| Tabla de tarifas de envío | 1 | 1 |
| `[AVISAR_HUMANO:]` | 2 | 2 |
| `[ENVIAR_ARCHIVO:]` | 7 | 7 |
| `[ENVIAR_IMAGEN:]` | 1 | 1 |
| Modo cotizador | 2 | 2 |
| Regla de cabina | 1 | 1 |
| Devoluciones | 1 | 1 |

Módulos modificados: 12, 41, 101, 106 — ninguno más, ninguno nuevo, ninguno
eliminado. Webhook `2547718`, conexiones, `scheduling: immediately` y los 17
manejadores de error, sin cambio. `systemPrompt`: 41,211 → 43,282 chars.

## Decisiones que conviene revisar

**El correo electrónico se conserva.** El dueño lo usa para mandarle al cliente
los datos de rastreo del paquete. Se quitó de donde costaba un mensaje aparte y
se metió DENTRO de la plantilla, así que no cuesta ninguna ida y vuelta extra:
el cliente lo escribe junto con lo demás. En la Ficha de Compra tiene su propia
línea (`📧 Correo electrónico:`) para que el equipo lo copie de un jalón.

En recolección en sucursal sigue sin pedirse, porque no hay nada que rastrear.
Si el dueño lo quiere también ahí, es una línea.

**Las referencias pasaron a opcionales.** Siguen en la plantilla marcadas como
tales y, si el cliente las escribe, aparecen en la ficha.

**El bloque del Buen Fin sigue vigente.** Termina en noviembre; su propia
cabecera dice que se borre completo al terminar.

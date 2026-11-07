# Promociones del Buen Fin — 7 nov 2026

Cinco creatividades: una de productos (cosméticos) y cuatro de servicios (citas).

## Las imágenes

No se pudieron subir a Drive desde la sesión: `create_file` del conector exige
el contenido en base64 dentro de la llamada, y cada imagen son ~106,000
caracteres en una sola línea. El entorno trunca salidas de ese tamaño, y
transcribir ~650,000 caracteres de base64 sin un error no es garantizable —
un carácter mal y la imagen queda corrupta. Se entregaron convertidas y
optimizadas, y las subió el usuario.

Convertidas de `webp` a JPEG porque **WhatsApp Cloud API no acepta webp** para
mensajes de tipo `image` (solo JPEG y PNG); webp solo vale para stickers.
Redimensionadas a 800 px de ancho, calidad 80.

Verificadas tras la subida: las cinco públicas, `image/jpeg`, y con
**SHA-256 idéntico** al archivo local.

| Archivo | ID de Drive | Bytes |
|---|---|---:|
| BuenFin-Productos-Descuentos.jpg | `1Vw19055kS4GUC6TG4Gd-E8jmeh3f0yyw` | 79,940 |
| BuenFin-Conoterapia-2x1.jpg | `1Y0lxQ4orjCrvMd4VsGmqo-Y4bmd2-mWc` | 101,120 |
| BuenFin-Masaje-Espalda-Ventosas.jpg | `1zlmRp8j7eYl6Xqifb2oEYyayjqTZL26o` | 121,147 |
| BuenFin-Masaje-Piernas-Cansadas.jpg | `1If5XkHcpBSkN7TNSggQgaytE7SIqiaCV` | 98,353 |
| BuenFin-Dermapen.jpg | `1bAV-UwxqtOmJbiMOw740avYQSBxTsUYK` | 85,946 |

Se usa el formato `https://lh3.googleusercontent.com/d/<ID>=w1000`, el mismo que
ya usaban las promos de octubre. No se pudo verificar desde la sesión (el proxy
bloquea `lh3.googleusercontent.com`), pero está en producción hoy.

## Por qué el asistente de citas dejó de mandar imágenes

El mecanismo **ya existía y nunca se rompió**:

```
3 (agente) → 30 (quita [AVISAR_HUMANO]) → 17 (detecta link lh3) → router 18
    R1: 4  → texto,  filtro: 17.link_imagen = ''
    R2: 19 → imagen, filtro: 17.link_imagen ≠ ''
```

`executions_list` con `status=3` sobre 5645150 no muestra **ni un solo error en
el módulo 19**. Los errores que hay son otros: un
`[400] The parameter text.body is required` del 1 de noviembre, 28
`[429] You have no credits remaining` de OpenAI el 26 de octubre, un 500 del AI
Agent el 22 y dos `(#2) Service temporarily unavailable` el 15.

O sea: las URLs no fallan, el agente simplemente no las estaba emitiendo — muy
probablemente porque las promos que los clientes preguntan ahora son las del
Buen Fin, que no estaban en el prompt.

**Además, el diseño era excluyente**: el filtro del módulo 4 es
`link_imagen = ''`, así que cuando sí había imagen el cliente recibía **solo la
imagen, sin una palabra de texto**. Nunca las dos cosas.

## Cambios en CITAS (`5645150_citas_BUENFIN.json`)

| Módulo | Cambio |
|---|---|
| 3 | bloque Buen Fin con las 4 promos de servicio |
| 17 | prompt corregido y ampliado |
| 4 | manda el texto **además** de la imagen, y nunca con cuerpo vacío |
| 9 módulos | manejadores `onerror` nuevos (de 2 a 11) |

**Módulo 17** tenía un bug: el prompt decía *"en el campo `texto`"* pero el campo
declarado se llama `Text`. Ahora reconoce dos formatos —la marca
`[ENVIAR_IMAGEN: URL]` y un link `lh3` suelto— y devuelve en `Text` el mensaje
**sin** el link, que antes no hacía.

**Módulo 4**, cuerpo nuevo:

```
{{ifempty(17.Text; ifempty(if(17.link_imagen = ""; 30.mensaje_limpio; ""); if(17.link_imagen = ""; 3.response; "")))}}
```

y el filtro pasa de `17.link_imagen = ''` a *"hay texto que enviar"* sobre esa
misma expresión. Resultado:

- Promo del Buen Fin → el agente manda texto + marca → **llegan los dos**.
- Promo de octubre → el agente manda solo el link → `Text` queda vacío → el
  filtro bloquea el texto → **solo la imagen**, igual que hoy.
- Sin imagen → texto normal, con dos respaldos antes de quedarse vacío.

> El bloque de octubre sigue diciendo *"responde ÚNICAMENTE con el link de
> imagen, sin una sola palabra de texto"*. No se tocó porque no se pidió. Si se
> quiere que esas también manden texto + imagen, es cambiar ese párrafo.

## Cambios en COSMÉTICOS (`5587862_cosmeticos_BUENFIN.json`)

Cosméticos **no tenía forma de mandar imágenes** (solo texto y dos módulos de
documento), así que se le agregó siguiendo el mismo patrón que citas:

| Módulo | Cambio |
|---|---|
| 12 | bloque Buen Fin con el descuento de productos |
| 60 | nuevo parámetro `promo_img_url` + reconoce `[ENVIAR_IMAGEN: URL]` |
| **62** (nuevo) | `sendMessage` tipo `image`, ruta 5 del router 90 |
| **321** (nuevo) | `builtin:Resume` sobre el 62 |

El 62 usa la conexión `9795431` y el `fromId` `587701384435147`, los mismos que
el módulo 38. Filtro: `{{60.promo_img_url}}` distinto de vacío.

## Verificación de los dos archivos

| | CITAS | COSMÉTICOS |
|---|---|---|
| Webhook | `2574977` sin cambio | `2547718` sin cambio |
| Conexiones | sin cambio | sin cambio |
| Scheduling | `immediately` sin cambio | `immediately` sin cambio |
| Módulos modificados | 3, 4, 17 | 12, 60 |
| Módulos nuevos | 9 manejadores de error | 62 y 321 |
| `onerror` | 2 → 11 | 16 → 17 |
| systemPrompt | 26,766 → 30,570 | 38,954 → 41,211 |
| Prompt original | intacto | intacto |
| Marcadores sin reemplazar | 0 | 0 |

Al quitar el bloque insertado, el prompt original vuelve a quedar carácter por
carácter igual salvo **una línea en blanco** de separación. Los módulos que no
debían cambiar (19 en citas; 38 y 61 en cosméticos) quedaron idénticos, y la
configuración del módulo 61 de cosméticos no se tocó.

## Cómo regenerar

`buenfin/aplicar.py` toma los cinco IDs de Drive y reconstruye ambos archivos
desde los blueprints vivos:

```
python3 -I buenfin/aplicar.py ID_PRODUCTOS ID_CONOTERAPIA ID_VENTOSAS ID_PIERNAS ID_DERMAPEN
```

Los textos de los bloques están en `buenfin/bloque_citas.txt` y
`buenfin/bloque_cosmeticos.txt`, con marcadores `PLACEHOLDER_*` para las URLs.

---

## Verificación post-import — 7 nov 2026

Ambos escenarios importados por el usuario y contrastados contra lo enviado.

| | CITAS 5645150 | COSMÉTICOS 5587862 |
|---|---|---|
| Módulos | 24 = 24 | 36 = 36 |
| Faltantes / extra | ninguno | ninguno |
| Módulos distintos | solo el 3, en `metadata` | **ninguno** |
| Webhook | `2574977` ✓ | `2547718` ✓ |
| Conexiones | sin cambio ✓ | sin cambio ✓ |
| `onerror` | 11 = 11 ✓ | 17 = 17 ✓ |
| `systemPrompt` | `sha b782113f` idéntico ✓ | bloque presente ✓ |
| Marcadores sin reemplazar | 0 | 0 |

La diferencia del módulo 3 es solo `metadata` (2410 → 2297 chars), el
descriptor de interfaz que Make regenera al importar. El `systemPrompt` tiene
el mismo `sha256` en ambos lados, así que el comportamiento no cambia.

### Make volvió a reiniciar el scheduling

Los dos quedaron en `{"type":"indefinitely","interval":900}` tras el import —
sondeo cada 15 minutos en vez de responder al instante. Es la tercera vez que
pasa en este proyecto. Corregido por API en los dos:

```
scenarios_update(5645150, scheduling={"type":"immediately"})
scenarios_update(5587862, scheduling={"type":"immediately"})
```

Confirmado `"scheduling": {"type": "immediately"}` y `"isActive": true` en los
dos. **Revisar esto siempre después de cada import.**

### Contenido vivo confirmado

**Citas**: los dos bloques de promociones conviven; 10 URLs `lh3` en el prompt
(6 de octubre + 4 del Buen Fin); módulo 17 con los campos `link_imagen` y
`Text` y reconociendo `[ENVIAR_IMAGEN:]`; módulo 4 con el filtro *"Hay texto
que enviar"*; módulo 19 intacto y ya con manejador de error. Once módulos con
`onerror`: 3, 4, 17, 19, 30, 31, 32, 34, 40, 50, 51.

**Cosméticos**: bloque del Buen Fin con el 15% y el 10%; módulo 60 con el
cuarto parámetro `promo_img_url`; módulo 62 nuevo (`type: image`, conexión
`9795431`, filtro sobre `promo_img_url`, con `onerror`); router 90 con 5 rutas.

### Errores

- **Cosméticos**: el más reciente es del **20 de octubre** (Airtable 429), y
  Airtable ya no está en el escenario. Cero errores desde entonces.
- **Citas**: el más reciente seguía siendo el `text.body is required` del
  1 de noviembre, que es justo lo que corrige la cascada `ifempty` del
  módulo 4.

Ninguno nuevo después del import.

### Lo que no se pudo verificar desde la sesión

Que las URLs `lh3.googleusercontent.com` resuelvan: el proxy del entorno
bloquea ese host. Lo que sí está comprobado es que los cinco archivos son
públicos y devuelven `image/jpeg` por la API de Drive, que es la misma
condición que cumplen las seis imágenes de octubre que ya funcionan.

# Cadena de pago · SP09 → SP10 → SP10-B → SP11

> Construido el 5-ago, todo en **draft** con los triggers **inactivos**.
> **Pendiente: corregir la tarjeta de ClickUp `wdx6zequuc`**, que describe un diseño distinto
> al que conviene construir (ver "Lo que la tarjeta pedía y por qué se cambió").

## Cómo quedó

```
SP09 · Envío de datos de pago            23059046…  8 nodos
  trigger: pipeline_stage_updated → etapa "Datos de pago enviados"
  ├─ Pack x2 = Sí  → WhatsApp datos de pago (pack)     → tag `pago-datos-enviados`
  └─ None          → WhatsApp datos de pago (estándar) → notif → tag `pago-datos-enviados`
        ↓
        (el lead responde mencionando un pago)
        ↓
SP10 · Validación de pago                0b0ff827…  4 nodos
  trigger: customer_reply
     message.body  string-contains-any-of  [yape, plin, voucher, boleta, comprobante,
                                            pagué, pague, deposité, transferí, constancia,
                                            captura, pago]
     contact.tags  index-of-true  `pago-datos-enviados`
  ├─ Comprobante recibido = Sí
  ├─ Oportunidad → etapa "Pago en validación"
  ├─ TAREA para Lucía · vence en 1 día
  └─ Notificación a Lucía
        ↓
        (Lucía marca el campo "Comprobante validado")
        ↓
SP10-B · Pago validado                   231be518…  5 nodos
  trigger: contact_changed sobre "Comprobante validado"
  └─ IF "Comprobante validado" = Sí
       ├─ Validado por = {{user.name}} · Fecha de validación
       └─ tag `pago-validado`
     (rama None = rechazó el comprobante → no hace nada, a propósito)
        ↓
SP11 · Cierre ganado                     2a7a0689…  2 nodos
  trigger: tag `pago-validado`
  ├─ Oportunidad → etapa "Matriculado" · status **won**
  └─ tags `matriculado` + `alumno-activo`
```

## Qué estaba mal

1. **Nadie disparaba nada.** SP10, SP10-B y SP11 tenían **0 triggers**. La cadena existía
   en nodos pero no se ejecutaba nunca.

2. **SP10-B y SP11 movían los dos a Matriculado.** SP10-B con `status=open`, SP11 con
   `status=won`. Como nada disparaba SP11, la oportunidad terminaba en Matriculado **pero
   abierta** — exactamente el problema que este proyecto vino a resolver (2.370 oportunidades
   al 100% abiertas). Ahora SP10-B no toca la etapa: solo valida y pone el tag. El cierre en
   `won` ocurre en un solo sitio, SP11.

3. **Faltaba el nodo de tarea** que la tarjeta sí pedía. Agregado, asignado a Lucía, con
   vencimiento a 1 día, y el cuerpo le dice explícitamente qué campo marcar para que siga
   la cadena.

4. **El rechazo no estaba contemplado.** `Comprobante validado` es un desplegable Sí/No, y
   `has-changed` dispara también cuando Lucía lo pone en **No**. Sin el if/else, rechazar un
   comprobante falso habría matriculado al lead igual. Ahora la rama None no hace nada.

## Lo que la tarjeta pedía y por qué se cambió

La tarjeta proponía disparar SP10 con *"Customer Replied con adjunto en etapa Datos de pago
enviados (aproximación: Customer Replied + filtro etapa)"*, y daba dos opciones para el adjunto:
aceptar falsos positivos (A) o mandar un webhook a n8n (B).

**Ese trigger no es construible.** `customer_reply` solo admite tres filtros en esta subcuenta:
`contact.tags`, `message.body` y `message.type` — y `message.type` es el **canal** de respuesta
(LS01 lo usa con valor 19), no el tipo de adjunto. No hay filtro por etapa del pipeline.

**Opción C, la que se implementó:** el tag `pago-datos-enviados` que pone SP09 hace de filtro de
etapa (y sí es filtrable), y las keywords detectan que el mensaje habla de un pago. El truco de
las keywords no es invento: sale del workflow **vivo** de Francisco `ALERTA - Pago por verificar`,
que ya lo usa con esa misma lista.

Queda mejor que la A —muchos menos falsos positivos— y no necesita n8n como la B.

**Lo único que no cubre:** la foto muda, sin una palabra de texto. Si en la práctica pasa seguido,
las salidas son un segundo trigger `customer_reply` filtrado solo por el tag (vuelve el falso
positivo, pero acotado a quien ya está en pago) o la opción B con n8n.

## Tags nuevos

`pago-datos-enviados` y `pago-validado`. Verificados contra los workflows **publicados** de
Francisco: cero colisiones.

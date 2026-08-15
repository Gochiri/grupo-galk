# Proyecto Grupo GALK — contexto para Claude Code

> **Lee `HANDOFF-SESION-2026-07-23.md` antes de tocar nada.** Ahí está el estado completo:
> qué ya existe en la subcuenta GHL (con todos los IDs), qué falta, los descubrimientos de API
> y los bloqueantes. Evita reconstruir cosas que ya están hechas.

## 1. Arranque de sesión (3 pasos)

```bash
./arranque.sh          # instala .venv y verifica conexión con GHL
```

Antes de correrlo necesitas el archivo `.env` en la raíz (NO está en git, contiene secretos):

```
GHL_API_KEY=pit-...                  # Private Integration Token
GHL_LOCATION_ID=YN2uRSDcNeBdTWm3UPCU
GHL_FIREBASE_REFRESH_TOKEN=AMf-...   # token interno; si da 401, pedir uno nuevo
```

Los valores los tiene el usuario. Pídeselos si falta el `.env`.

## 2. Ramas

- `main` = rama integradora (default del repo).
- `german` / `oliver` / `henry` = una por persona. **Trabaja en la que te indiquen**, no crees ramas nuevas.

```bash
git checkout <persona> && git pull --rebase origin main     # al empezar
git push -u origin <persona>                                # al terminar
git checkout main && git pull origin main && git merge <persona> && git push origin main
```

## 3. Reglas al escribir en GHL (subcuenta EN PRODUCCIÓN)

La subcuenta tiene ~10.900 contactos y ~2.370 oportunidades **reales**. Cuidado.

- **Política §3 — reconstrucción total:** nada de lo heredado (los 40 workflows de Francisco, el
  pipeline `[GALK] Cursos y Capacitaciones`, los 14 campos UPPERCASE, los 41 tags) se edita ni se
  reutiliza. Todo lo nuevo es **aditivo**; lo viejo se archiva en la limpieza (SETUP-01).
- **Idempotencia obligatoria:** todo script que cree algo debe verificar antes si ya existe y
  saltar. Los de `scripts_ghl/` ya lo hacen — sigue ese patrón.
- **Workflows siempre como DRAFT.** Nunca publicar sin que un humano lo revise en la UI.
- **Prohibido hardcodear URLs de fichas** en workflows: usar `{{custom_values.ficha_...}}`.
- Antes de crear algo, consulta los IDs ya existentes en el handoff (§1).
- **Todo PUT de `workflowData` rompe el trigger.** El trigger guarda `targetActionId` (el nodo por
  el que entra el contacto) y vive en otro endpoint, así que al regenerar nodos queda apuntando a
  uno que ya no existe: el workflow **no se ejecuta y no avisa**. Correr después
  `scripts_ghl/reparar_targetaction.py --aplicar`.
- **Triggers `contact_changed`: usar `wf_lib.cond_trigger_campo()`, nunca armar la condición a
  mano.** El campo va como `contact.<ID>` **y** repetido en la clave `id`. Con el ID pelado el
  trigger se guarda, pero en la UI el desplegable queda en "Seleccionar" y **no dispara**.
  Auditor: `scripts_ghl/reparar_condiciones_trigger.py --aplicar`.
- **Un workflow publicado con el trigger inactivo no hace nada.** Al terminar, verificar
  `status == published` **y** `active == True` en cada trigger.
- **`allowMultiple` (Reingreso) viene apagado y con eso el contacto entra UNA vez en su vida.**
  Cualquier workflow que dependa de reintentar —guardas que cortan si faltan datos,
  normalizadores que recalculan— lo necesita en `true`. No activarlo en los que hacen algo hacia
  afuera al entrar (recordatorios, cierres, matrícula): ahí hay que poner un marcador de "ya
  hecho" primero. Auditor: `scripts_ghl/permitir_reingreso.py`.

### ⚠️ Límite de 500 caracteres en los campos de texto de los bots

**Cada vez que escribas texto para pegar en la UI de un bot, cuéntalo antes de entregarlo.**
No hay que recordárselo a nadie: si el texto pasa de 500, GHL lo rechaza al guardar.

| Campo | Límite |
|---|---|
| Transfer Bot → *Condición de activación* | **10–500** |
| Contact Info → *Qué actualizar en el campo* | **500** |
| Otros campos de texto de acciones de bot | asumir **500** mientras no se compruebe otra cosa |

No aplica al **prompt** del bot (Personality / Goal / Instructions), que admite mucho más, ni a
las Knowledge Base.

Si no cabe: la casuística larga va en *Frases de Ejemplo* (Transfer Bot) o en el prompt; en el
campo corto se deja solo la regla. **Entrega siempre el conteo junto al texto**, y si andas cerca
del tope, una versión corta de respaldo.

## 4. Qué se puede hacer por API y qué no

| Vía | Sirve para |
|---|---|
| **API pública** (PIT) | pipelines, campos custom, custom values, usuarios, contactos |
| **API interna** (token Firebase, `backend.leadconnectorhq.com`) | **workflows** (CRUD completo) |
| **Solo UI / Playwright** | **bots de Conversation AI**, carpetas de campos custom |

Detalle de endpoints, límites y gotchas del esquema de nodos: ver §2 del handoff.

## 5. Gestión de tareas

El proyecto se lleva en **ClickUp** (carpeta `$$ Grupo Galk`, 8 listas por módulo). Los IDs de
todas las tareas están en §4 del handoff. Al completar algo en GHL, **actualiza la tarjeta
correspondiente** (estado + comentario con los IDs creados).

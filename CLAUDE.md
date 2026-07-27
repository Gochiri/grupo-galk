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

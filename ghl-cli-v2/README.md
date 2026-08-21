# GHL CLI v2 — toolkit de implementación GoHighLevel por API

Versión 2 del CLI original, actualizada con TODO lo aprendido en la implementación de
Grupo GALK (jul-ago 2026): formas de nodos validadas en producción, convenciones del
canvas, auditores, y el playbook completo de gotchas.

## Qué trae

| Pieza | Qué es |
|---|---|
| `PLAYBOOK-GHL.md` | **Léelo primero.** La biblia de gotchas: las 2 APIs, los 6 errores mortales de workflows, formas de nodo con trampa, leyes de Conversation AI, el patrón "secuencia de ficha", protocolo de pruebas |
| `gohighlevel/utils/wf_toolkit.py` | **La pieza nueva clave.** Formas de nodos validadas (WhatsApp texto/media/PDF, SMS, waits en segundos, notificaciones, clear de campos, AI status), convención if/else que el canvas sí renderiza, `put_workflow()` seguro, `verificar_triggers()` |
| `gohighlevel/utils/ghl_client.py` | Cliente API pública (PIT) — igual que v1 |
| `gohighlevel/utils/ghl_internal_client.py` | Cliente API interna (token Firebase) para workflows/triggers — igual que v1 |
| `gohighlevel/utils/workflow_builder.py` | Builder v1 (legado — para construcciones nuevas usa `wf_toolkit`) |
| `ejemplos/` | Scripts reales del proyecto GALK como referencia: la secuencia de ficha completa (`ejemplo_secuencia_de_ficha.py`), los auditores (`reparar_targetaction`, `reparar_condiciones_trigger`, `permitir_reingreso`) y el subidor de PDFs al media store |
| `CLAUDE-PLANTILLA.md` | CLAUDE.md inicial para el proyecto del cliente nuevo (renombrar a `CLAUDE.md`) |
| `.env.example` | Variables necesarias |

## Instalación en un proyecto nuevo

```bash
# 1. Copia esta carpeta al repo del proyecto nuevo
cp -r ghl-cli-v2/gohighlevel  <proyecto>/cli_anything/gohighlevel   # o donde prefieras
cp ghl-cli-v2/PLAYBOOK-GHL.md <proyecto>/
cp ghl-cli-v2/CLAUDE-PLANTILLA.md <proyecto>/CLAUDE.md              # y edítalo
cp ghl-cli-v2/.env.example    <proyecto>/.env                       # y rellénalo

# 2. Dependencias (solo requests)
python3 -m venv .venv && .venv/bin/pip install requests

# 3. Prueba de conexión
.venv/bin/python -c "
from gohighlevel.utils.wf_toolkit import cargar_env; cargar_env()
import os, requests
r = requests.get(f'https://services.leadconnectorhq.com/locations/{os.environ[\"GHL_LOCATION_ID\"]}/customFields',
    headers={'Authorization': f'Bearer {os.environ[\"GHL_API_KEY\"]}', 'Version': '2021-07-28'})
print('conexión:', r.status_code)"
```

## Los 3 hábitos que hacen que esto funcione

1. **Playbook primero.** Cada regla costó un bug en producción real.
2. **Molde antes que invento.** Nodo nuevo = créalo en la UI una vez, léelo por API, clona.
3. **Dry-run, idempotencia y verificación post-PUT** (`verificar_triggers()`) en todo script.

## Ajustes por proyecto (no hay hardcode, pero sí contexto)

- Los IDs (location, pipeline, campos, bots) van en `.env` / constantes del proyecto —
  los ejemplos de `ejemplos/` muestran el patrón.
- El `from_phone_number` de WhatsApp se saca del primer nodo molde hecho en la UI.
- Los bots de Conversation AI no tienen API: prompts y acciones se entregan como textos
  contados (≤500 caracteres los campos de acciones) para pegar en la UI.

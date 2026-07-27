#!/usr/bin/env bash
# Arranque de sesión: instala el entorno y verifica la conexión con GHL.
# Uso:  ./arranque.sh
set -e
cd "$(dirname "$0")"

echo "→ 1/3 Verificando .env ..."
if [ ! -f .env ] || grep -q "pit-xxxxxxxx" .env 2>/dev/null; then
  echo
  echo "  ✗ Falta el .env (o tiene los valores de ejemplo)."
  echo "    Créalo en la raíz con:"
  echo
  echo "      GHL_API_KEY=pit-..."
  echo "      GHL_LOCATION_ID=YN2uRSDcNeBdTWm3UPCU"
  echo "      GHL_FIREBASE_REFRESH_TOKEN=AMf-..."
  echo
  echo "    (los valores los tiene el usuario — NO están en git a propósito)"
  exit 1
fi
echo "  ✓ .env presente"

echo "→ 2/3 Instalando entorno (.venv) ..."
if [ ! -d .venv ]; then
  ./install.sh >/dev/null 2>&1 || { echo "  ✗ falló install.sh"; exit 1; }
fi
chmod +x ghl 2>/dev/null || true
echo "  ✓ .venv listo"

echo "→ 3/3 Verificando conexión con GHL ..."
.venv/bin/python - <<'EOF'
import os, sys, pathlib
ROOT = pathlib.Path(__file__).parent if "__file__" in dir() else pathlib.Path(".")
for line in open(".env"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, ".")
from cli_anything.gohighlevel.utils import ghl_client as api
LOC = os.environ["GHL_LOCATION_ID"]

# API pública (PIT)
try:
    pls = api.get("/opportunities/pipelines", params={"locationId": LOC}).get("pipelines", [])
    print(f"  ✓ API pública OK — pipelines: {[p['name'] for p in pls]}")
except Exception as e:
    print(f"  ✗ API pública FALLA (¿PIT revocado?): {str(e)[:120]}")

# API interna (Firebase)
try:
    from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
    c = InternalGHLClient(TokenManager(), LOC)
    wfs = c.request("GET", f"/workflow/{LOC}")
    n = len([w for w in wfs if w.get("type") == "workflow"]) if isinstance(wfs, list) else "?"
    print(f"  ✓ API interna OK — workflows: {n}")
except Exception as e:
    print(f"  ✗ API interna FALLA (token Firebase caducado → pedir uno nuevo): {str(e)[:120]}")
EOF

echo
echo "✓ Listo. Lee HANDOFF-SESION-2026-07-23.md para el estado del proyecto."

#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3.12}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "No se encontró $PYTHON_BIN. Instala Python 3.12 o define PYTHON_BIN." >&2
  exit 1
fi

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 12):
    raise SystemExit("CYBER_AI requiere Python 3.12 o superior.")
print(f"Python {sys.version.split()[0]} detectado.")
PY

if [[ ! -d .venv ]]; then
  "$PYTHON_BIN" -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo
echo "Entorno preparado."
echo "Actívalo con: source .venv/bin/activate"
echo "Pruebas: python -m unittest discover -s tests -v"

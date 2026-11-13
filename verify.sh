#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ -x .venv/bin/python ]]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1 && [[ ! -x "$PYTHON_BIN" ]]; then
  echo "No se encontró Python. Ejecuta bash setup.sh o define PYTHON_BIN." >&2
  exit 1
fi

echo "== Preflight local =="
"$PYTHON_BIN" preflight.py

echo
echo "== Sintaxis Python =="
"$PYTHON_BIN" -m compileall -q .

echo
echo "== Autoprueba del núcleo =="
"$PYTHON_BIN" cyber_ai.py --self-test

echo
echo "== Suite automatizada =="
"$PYTHON_BIN" -m unittest discover -s tests -v

echo
echo "CYBER_AI superó las comprobaciones locales."
echo "Esto no sustituye pruebas con Ollama, modelos, Docker ni proveedores reales."

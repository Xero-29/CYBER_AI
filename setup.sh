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
import platform
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit("El lock SHA-256 actual requiere CPython 3.12.x.")
if sys.platform != "linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
    raise SystemExit("El lock SHA-256 actual solo soporta Linux x86_64.")
libc_name, libc_version = platform.libc_ver()
try:
    libc_parts = tuple(int(part) for part in libc_version.split(".")[:2])
except ValueError:
    libc_parts = ()
if libc_name.lower() != "glibc" or len(libc_parts) < 2 or libc_parts < (2, 26):
    raise SystemExit("El lock SHA-256 actual requiere glibc >= 2.26.")
print(f"Python {sys.version.split()[0]} en Linux x86_64/{libc_name} {libc_version}.")
PY

if [[ ! -d .venv ]]; then
  "$PYTHON_BIN" -m venv .venv
fi

.venv/bin/python -m pip install --require-hashes -r requirements.lock

# Runtime data can contain memory, execution history and local credentials.
# Do not follow a symlinked data root; preflight will reject it.
if [[ -d data && ! -L data ]]; then
  find data -type d -exec chmod 700 {} +
fi

echo
echo "Entorno preparado."
echo "Actívalo con: source .venv/bin/activate"
echo "Pruebas: python -m unittest discover -s tests -v"

#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"
IMAGE="${CYBER_AI_RUST_LAB_IMAGE:-cyber-ai-rust-skill-lab:local}"
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Construyendo sandbox Rust aislado..."
  sh "$ROOT/build-rust-skill-lab.sh"
fi
exec python3 autonomous_skill_lab.py \
  --planner-model "${CYBER_AI_PLANNER_MODEL:-qwen3.5:9b}" \
  --executor-model "${CYBER_AI_EXECUTOR_MODEL:-qwen3.5:2b-q4_K_M}" \
  --image "$IMAGE" "$@"

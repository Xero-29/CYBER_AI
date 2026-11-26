#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
IMAGE="${CYBER_AI_RUST_LAB_IMAGE:-cyber-ai-rust-skill-lab:local}"
docker build --pull -f "$ROOT/sandbox/skill-lab.Dockerfile" -t "$IMAGE" "$ROOT"
docker image inspect --format '{{.Id}}' "$IMAGE"
docker run --rm --network=none "$IMAGE" --version
docker run --rm --network=none "$IMAGE" --list

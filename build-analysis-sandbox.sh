#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
docker build --pull -f "$ROOT/Dockerfile.analysis-sandbox" -t "${CYBER_AI_ANALYSIS_SANDBOX_IMAGE:-cyber-ai-analysis-sandbox:1.0}" "$ROOT"
docker image inspect --format '{{.Id}}' "${CYBER_AI_ANALYSIS_SANDBOX_IMAGE:-cyber-ai-analysis-sandbox:1.0}"

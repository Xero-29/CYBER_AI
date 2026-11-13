#!/usr/bin/env python3
"""Interfaz CLI explícita para los adaptadores locales de CYBER_AI."""
import argparse
import json
import os
import sys

from tool_adapters import TOOL_SPECS, ToolExecutionError, run_local_tool, write_evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=sorted(TOOL_SPECS))
    parser.add_argument("--target", required=True, help="Ruta relativa dentro del repositorio")
    parser.add_argument("--config", help="Configuración local para Semgrep")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--execute", action="store_true", help="Confirma la ejecución local")
    args = parser.parse_args(argv)

    if not args.execute:
        print(json.dumps({
            "status": "dry_run",
            "tool": args.tool,
            "target": args.target,
            "execution_started": False,
            "message": "Añade --execute para iniciar el adaptador local.",
        }, ensure_ascii=False, indent=2))
        return 0

    try:
        evidence = run_local_tool(
            args.tool, args.target, config_path=args.config, timeout=args.timeout
        )
        evidence_path = write_evidence(evidence, output_dir=os.environ.get("CYBER_AI_EVIDENCE_DIR", "reports/tool_evidence"))
    except ToolExecutionError as exc:
        print(json.dumps({"status": "denied", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    evidence["evidence_file"] = str(evidence_path)
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

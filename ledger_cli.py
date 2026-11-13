#!/usr/bin/env python3
"""Consulta la integridad y el historial del ledger de ejecuciones."""

import argparse
import json

from execution_ledger import ExecutionLedger


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify", help="Verificar la cadena hash completa")
    commands.add_parser("namespaces", help="Listar namespaces con eventos")
    history = commands.add_parser("history", help="Consultar eventos de un namespace")
    history.add_argument("--namespace", required=True)
    history.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)

    ledger = ExecutionLedger()
    if args.command == "verify":
        result = ledger.verify()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid") else 1
    if args.command == "namespaces":
        print(json.dumps(ledger.namespaces(), ensure_ascii=False, indent=2))
        return 0
    result = ledger.history(namespace=args.namespace, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

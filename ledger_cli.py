#!/usr/bin/env python3
"""Consulta la integridad y el historial del ledger de ejecuciones."""

import argparse
import json

from execution_ledger import ExecutionLedger


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify", help="Verificar la cadena hash completa")
    reconcile = commands.add_parser("reconcile", help="Marcar inicios huérfanos como interrumpidos")
    reconcile.add_argument("--namespace", help="Limitar la reconciliación a un namespace")
    reconcile.add_argument("--older-than-seconds", type=float, default=300,
                           help="Edad mínima de un inicio sin cierre (predeterminado: 300)")
    reconcile.add_argument("--confirm-no-active-runs", action="store_true",
                           help="Confirmar que no hay trabajadores ejecutando tareas")
    commands.add_parser("namespaces", help="Listar namespaces con eventos")
    history = commands.add_parser("history", help="Consultar eventos de un namespace")
    history.add_argument("--namespace", required=True)
    history.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)

    ledger = ExecutionLedger()
    if args.command == "reconcile":
        if not args.confirm_no_active_runs:
            parser.error("reconcile requiere --confirm-no-active-runs; detén los trabajadores primero")
        result = ledger.reconcile_interrupted(
            namespace=args.namespace, stale_after_seconds=args.older_than_seconds)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
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

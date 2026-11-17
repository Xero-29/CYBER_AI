#!/usr/bin/env python3
"""CLI sin red para proponer, aprobar y revertir Skills verificadas."""
import argparse
import json
import sys
from pathlib import Path

import skillbook


MANIFEST_FIELDS = {
    "name", "task_pattern", "description", "prerequisites", "methodology",
    "validation", "tools", "tags", "source_urls", "namespace", "event_ids",
}


def _load_manifest(path):
    file_path = Path(path)
    if file_path.is_symlink() or not file_path.is_file():
        raise ValueError("El manifiesto debe ser un archivo regular, no un symlink.")
    if file_path.stat().st_size > 128 * 1024:
        raise ValueError("El manifiesto supera 128 KiB.")
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("El manifiesto debe contener un objeto JSON.")
    unknown = set(data) - MANIFEST_FIELDS
    missing = MANIFEST_FIELDS - set(data)
    if unknown or missing:
        raise ValueError(
            f"Campos inválidos. Faltan: {sorted(missing)}; sobran: {sorted(unknown)}"
        )
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("propose", "approval-payload", "promote"):
        item = sub.add_parser(command)
        item.add_argument("--manifest", required=True)
    promote = sub.choices["promote"]
    signature = promote.add_mutually_exclusive_group(required=True)
    signature.add_argument("--signature")
    signature.add_argument("--signature-file")

    rollback_payload = sub.add_parser("rollback-payload")
    rollback_payload.add_argument("--skill-id", required=True)
    rollback_payload.add_argument("--target-version", type=int, required=True)
    rollback = sub.add_parser("rollback")
    rollback.add_argument("--skill-id", required=True)
    rollback.add_argument("--target-version", type=int, required=True)
    rollback.add_argument("--signature", required=True)

    verify_history = sub.add_parser("verify-history")
    verify_history.add_argument("--skill-id", required=True)

    review_due = sub.add_parser("review-due")
    review_due.add_argument("--max-age-days", type=int, default=180)

    deprecate_payload = sub.add_parser("deprecate-payload")
    deprecate_payload.add_argument("--skill-id", required=True)
    deprecate_payload.add_argument("--reason", required=True)
    deprecate = sub.add_parser("deprecate")
    deprecate.add_argument("--skill-id", required=True)
    deprecate.add_argument("--reason", required=True)
    deprecate_signature = deprecate.add_mutually_exclusive_group(required=True)
    deprecate_signature.add_argument("--signature")
    deprecate_signature.add_argument("--signature-file")

    args = parser.parse_args(argv)
    try:
        if args.command in {"propose", "approval-payload", "promote"}:
            data = _load_manifest(args.manifest)
            if args.command == "propose":
                result = skillbook.propose_skill_from_ledger(**data)
            elif args.command == "approval-payload":
                result = {"approval_payload": skillbook.skill_approval_payload(**data)}
            else:
                signed = (
                    Path(args.signature_file).read_text(encoding="ascii").strip()
                    if args.signature_file else args.signature
                )
                result = skillbook.register_skill_from_ledger(
                    **data, approval_signature=signed
                )
        elif args.command == "rollback-payload":
            result = {"rollback_payload": skillbook.skill_rollback_payload(
                args.skill_id, args.target_version
            )}
        elif args.command == "rollback":
            result = skillbook.rollback_skill_version(
                args.skill_id, args.target_version, args.signature
            )
        elif args.command == "verify-history":
            result = skillbook.verify_skill_history(args.skill_id)
            if not result["valid"]:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 1
        elif args.command == "review-due":
            result = {"skills_due_for_review": skillbook.list_skills_due_for_review(
                args.max_age_days
            )}
        elif args.command == "deprecate-payload":
            result = {"deprecation_payload": skillbook.skill_deprecation_payload(
                args.skill_id, args.reason
            )}
        else:
            signed = (
                Path(args.signature_file).read_text(encoding="ascii").strip()
                if args.signature_file else args.signature
            )
            result = skillbook.deprecate_skill(args.skill_id, args.reason, signed)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

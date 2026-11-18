# Execution evidence ledger

execution_ledger.py adds a transactional SQLite event log for observed task runs.

## Guarantees
- BEGIN IMMEDIATE, WAL and synchronous=FULL for writes.
- Eventos de ciclo de vida `started` y estados terminales, enlazados mediante `metadata.start_event_id`.
- Migración automática de bases existentes al esquema que admite `started`, conservando filas y hashes.
- Namespace, task fingerprint, status, tool/version, model, environment, duration,
  optional cost, validator outcomes and evidence SHA-256 digest.
- Hash chaining detects modified, missing, reordered or broken-chain rows.
- SQLite triggers block ordinary UPDATE/DELETE operations.
- Secret-like metadata keys are redacted before persistence.
- The database path and DB/WAL/SHM companions are revalidated against symlinks and non-regular files before each connection; POSIX requires a private parent directory and restricts database files to `0600`.
- SQLite integer fields are bounded to the signed 64-bit range before insertion; unrepresentable recovery thresholds fail closed.
- History queries are namespace-scoped.

## Signed external checkpoints

`ledger_checkpoint.py` creates a canonical HMAC-SHA256 anchor containing the ledger sequence and event hash. Verification checks the signature, full local hash chain, and that the current ledger still contains the anchored row. Store checkpoint files outside the ledger host/volume and keep `CYBER_AI_LEDGER_CHECKPOINT_KEY` in an external secret manager. This detects rollback/replacement only when the checkpoint and key remain independently protected; it is not WORM storage or operator identity proof.

## Limitations
Tamper-evident is not tamper-proof. A privileged actor can replace the database
and recompute the chain. Production requires signed checkpoints exported to
independently controlled immutable storage, KMS/HSM-backed keys, OS permissions
and tested restore procedures. The ledger stores an evidence digest, not the
artifact itself. A successful process exit is not proof of correctness;
independent validators must establish outcomes. The team orchestrator records objective reviews as independent validators only when a separate reviewer (VERITAS/FILTRO) returns a grounded compliant verdict. Agent self-completion is explicitly non-independent. The ledger does not itself promote Skills; signed approval is required. Lifecycle `started` rows are ignored when checking whether all actual task outcomes completed successfully. The CLI executors `tool_executor.py` and `task_runner.py` require ledger recording by default and only permit unlogged execution with the explicit `--allow-unlogged-execution` flag; `agent_runner.py` also requires ledger recording by default and only permits unlogged execution when `CYBER_AI_ALLOW_UNLOGGED_EXECUTION=1` is explicitly set (the stricter `CYBER_AI_LEDGER_REQUIRED=1` overrides that exception); `nuclei_scanner.scan_target` accepts `require_ledger=True`; and `team_orchestrator.py` requires start and terminal events. Unexpected exceptions can still leave unmatched start events because a universal exception-finalization wrapper is not yet implemented.

## Use
from execution_ledger import ExecutionLedger
ledger = ExecutionLedger()
ledger.append(namespace="workspace-a", task="run unit tests",
              status="completed", tool="pytest", duration_ms=1200,
              evidence={"artifact": "reports/test-result.json"},
              validator_results=[{"name": "exit_code", "passed": True, "independent": False}])
assert ledger.verify()["valid"]

Run: python -m unittest tests.test_execution_ledger -v

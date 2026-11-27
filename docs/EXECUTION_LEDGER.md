# Execution evidence ledger

execution_ledger.py adds a transactional SQLite event log for observed task runs.

## Guarantees
- BEGIN IMMEDIATE, WAL and synchronous=FULL for writes; every connection also sets `trusted_schema=OFF`, `secure_delete=ON` and `foreign_keys=ON`.
- Eventos de ciclo de vida `started` y estados terminales, enlazados mediante `metadata.start_event_id`.
- Migración automática de bases existentes al esquema que admite `started`, conservando filas y hashes.
- Namespace, task fingerprint, status, tool/version, model, environment, duration,
  optional cost, validator outcomes and evidence SHA-256 digest.
- Hash chaining detects modified, missing, reordered or broken-chain rows.
- SQLite triggers block ordinary UPDATE/DELETE operations.
- Sensitive field-name keys redact their values, and token-like material embedded in mapping keys is redacted before persistence without collapsing colliding entries.
- Process output is considered complete only when both stdout/stderr readers reach EOF; read failures or readers that remain blocked fail the adapter instead of yielding partial evidence.
- History queries are namespace-scoped.
- Database, WAL and SHM paths reject symlinks/non-regular files; on POSIX the parent directory must be private (0700) and database/sidecar files are restricted to 0600.

## Signed external checkpoints

`ledger_checkpoint.py` creates a canonical HMAC-SHA256 anchor containing the ledger sequence and event hash. Verification checks the signature, full local hash chain, and that the current ledger still contains the anchored row. Store checkpoint files outside the ledger host/volume and keep `CYBER_AI_LEDGER_CHECKPOINT_KEY` in an external secret manager. This detects rollback/replacement only when the checkpoint and key remain independently protected; it is not WORM storage or operator identity proof.

## Limitations
Tamper-evident is not tamper-proof. A privileged actor can replace the database
and recompute the chain. Production requires signed checkpoints exported to
independently controlled immutable storage, KMS/HSM-backed keys, OS permissions
and tested restore procedures. POSIX directory/file modes are checked and tightened; Windows ACLs are not inspected by this code and must be provisioned and verified by deployment automation. The ledger stores an evidence digest, not the
artifact itself. A successful process exit is not proof of correctness;
independent validators must establish outcomes. The team orchestrator records objective reviews as independent validators only when a separate reviewer (VERITAS/FILTRO) returns a grounded compliant verdict. Agent self-completion is explicitly non-independent. The ledger does not itself promote Skills; signed approval is required. Lifecycle `started` rows are ignored when checking whether all actual task outcomes completed successfully. `tool_executor.py` and `task_runner.py` now require a ledger by default; `--allow-unlogged-execution` is an explicit troubleshooting override and is not recommended. `--require-ledger` remains accepted for clarity. `agent_runner.py` also requires the ledger by default; `CYBER_AI_ALLOW_UNLOGGED_EXECUTION=1` is the explicit override, while `CYBER_AI_LEDGER_REQUIRED=1` forces the requirement, `nuclei_scanner.scan_target` accepts `require_ledger=True`, and `team_orchestrator.py` requires start and terminal events. Handled exceptions close the lifecycle where the wrapper can observe them. Abrupt process termination or host loss can still leave unmatched starts; the reconciler marks them `interrupted` with unknown outcome and never infers success.

## Use
from execution_ledger import ExecutionLedger
ledger = ExecutionLedger()
ledger.append(namespace="workspace-a", task="run unit tests",
              status="completed", tool="pytest", duration_ms=1200,
              evidence={"artifact": "reports/test-result.json"},
              validator_results=[{"name": "exit_code", "passed": True, "independent": False}])
assert ledger.verify()["valid"]

Run: python -m unittest tests.test_execution_ledger -v

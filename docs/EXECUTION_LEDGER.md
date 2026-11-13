# Execution evidence ledger

execution_ledger.py adds a transactional SQLite event log for observed task runs.

## Guarantees
- BEGIN IMMEDIATE, WAL and synchronous=FULL for writes.
- Namespace, task fingerprint, status, tool/version, model, environment, duration,
  optional cost, validator outcomes and evidence SHA-256 digest.
- Hash chaining detects modified, missing, reordered or broken-chain rows.
- SQLite triggers block ordinary UPDATE/DELETE operations.
- Secret-like metadata keys are redacted before persistence.
- History queries are namespace-scoped.

## Limitations
Tamper-evident is not tamper-proof. A privileged actor can replace the database
and recompute the chain. Production requires signed checkpoints exported to
independently controlled immutable storage, KMS/HSM-backed keys, OS permissions
and tested restore procedures. The ledger stores an evidence digest, not the
artifact itself. A successful process exit is not proof of correctness;
independent validators must establish outcomes. The team orchestrator records objective reviews as independent validators only when a separate reviewer (VERITAS/FILTRO) returns a grounded compliant verdict. Agent self-completion is explicitly non-independent. The ledger does not itself promote Skills; signed approval is required.

## Use
from execution_ledger import ExecutionLedger
ledger = ExecutionLedger()
ledger.append(namespace="workspace-a", task="run unit tests",
              status="completed", tool="pytest", duration_ms=1200,
              evidence={"artifact": "reports/test-result.json"},
              validator_results=[{"name": "exit_code", "passed": True, "independent": False}])
assert ledger.verify()["valid"]

Run: python -m unittest tests.test_execution_ledger -v

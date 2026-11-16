# Release gates

This document defines what must be true before CYBER_AI can move from repository
testing to a controlled pilot or production. A green unit-test workflow alone
does not satisfy these gates.

## Gate A — reproducible repository build

- [ ] Clean checkout on a supported OS and Python version.
- [ ] Dependency lock includes exact versions and verified artifact hashes.
- [ ] SBOM generated from the same resolved dependency set.
- [ ] CI runs syntax checks, complete tests, security/static checks and sandbox tests.
- [ ] CI artifacts are retained with commit-SHA provenance.
- [ ] Dependency update proposals are reviewed and tested before merge.

## Gate B — security controls

- [ ] Secret manager integrated; no long-lived secrets in files, logs, prompts or CI output.
- [ ] Key ownership, rotation, revocation, recovery and separation of duties documented.
- [ ] Backup encryption enabled and keys stored independently.
- [ ] Ledger checkpoints exported to independently administered immutable storage.
- [ ] RBAC, least privilege, tenant isolation and audit access tested.
- [ ] Threat model reviewed by someone other than the implementer.
- [ ] Sandbox boundary tested against hostile workloads; Docker-only isolation is insufficient
      where untrusted code can reach the host kernel.

## Gate C — knowledge and AI quality

- [ ] External sources reviewed individually for provenance, license, accuracy and freshness.
- [ ] Retrieval benchmark run with the actual embedding provider and expert-reviewed queries.
- [ ] Citations, tenant isolation, poisoning resistance and stale/contradictory content tested.
- [ ] Each production provider tested for timeout, rate limits, outage, malformed responses,
      credential handling, cost limits and fallback behavior.
- [ ] Skills require independent approval, regression evidence, versioning and rollback.

## Gate D — operational resilience

- [ ] Load, soak, concurrency and resource-limit tests completed on target infrastructure.
- [ ] RPO/RTO approved by the system owner.
- [ ] Encrypted off-host backups and restore drills demonstrated.
- [ ] Host loss, database corruption, key loss and provider outage exercises completed.
- [ ] Monitoring, alerting, incident response and retention policies operational.

## Gate E — release authorization

- [ ] All prior gates have named owners and attached evidence.
- [ ] No unresolved critical/high findings without a formally accepted risk.
- [ ] Branch protection and required status checks enabled on the release branch.
- [ ] License and third-party notices reviewed and approved by the repository owner.
- [ ] Release tag points to the exact tested commit; rollback procedure is rehearsed.

## Current interpretation

The repository currently has automated Python and Docker CI, offline knowledge
packages, provider adapters, a local execution ledger and local backup integrity
checks. Those are implementation capabilities, not proof that Gates B–E pass.
Items requiring external services, owner decisions or real infrastructure remain
open until evidence is attached. Never mark a gate complete based only on a
configuration file or a simulated test.

# Security Policy

## Supported branch

Security fixes are developed against the active integration branch:
`codex/security-integrity-audit`. The default branch may not yet contain
those changes. Do not assume that an open pull request is a production release.

## Reporting a vulnerability

Do not publish exploitable details, credentials, personal data, or weaponized
proofs in public issues. Use GitHub's private vulnerability reporting feature
for this repository when it is enabled. If private reporting is unavailable,
contact the repository maintainer through a private channel before disclosure.

Include:
- affected commit or release;
- affected component and configuration;
- impact and realistic attack prerequisites;
- minimal, non-destructive reproduction;
- suggested mitigation, if known.

Do not test against systems without explicit authorization.

## Response expectations

This repository does not currently promise a contractual response or remediation
time. Reports should be triaged for severity, reproducibility, affected versions,
and whether credentials or user data may be exposed. A fix is not considered
verified until regression tests and CI pass on the fixing commit.

## Release and deployment warning

CYBER_AI is not certified for production or institutional deployment. Consult
`PROJECT_STATUS.md` and `docs/RELEASE_GATES.md`. In particular, local hash
chains and optional HMAC signatures are not substitutes for independently
managed keys, external immutable storage, encryption, or an independently
reviewed deployment.

<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Security Policy

## Supported versions

Security fixes land on the latest published release. Older 0.0.x
releases do not receive them; upgrade to the latest release, which
ships in lockstep with the core
[`pain001`](https://github.com/sebastienrousseau/pain001) library.
Plugins already generated from an older release are their authors'
code; compare them with a fresh render to pick up a fix.

## Reporting a vulnerability

**Do not open a public issue for security reports.**

Use one of the following private channels, in this order of
preference:

1. **GitHub Private Vulnerability Reporting**
   <https://github.com/sebastienrousseau/pain001-plugin-template/security/advisories/new>
   (the maintainers are notified automatically; do this first)
2. **Email**: `security@pain001.com`
3. **Direct message** to a maintainer listed in
   [MAINTAINERS.md](MAINTAINERS.md)

Please include a description and its impact, steps to reproduce
(preferably a failing test), the scaffold version, and a suggested fix
if you have one. Do not include real payment data or credentials.

These are goals, not guarantees: the pain001 suite is maintained in a
personal capacity, with no SLA and no out-of-hours cover.

**Acknowledgement**: the goal is within 5 working days.
**Triage**: a severity assessment and remediation plan after
acknowledgement.
**Fix windows** (best effort): critical 7 days, high 30 days, medium 60
days, low best-effort. The clock starts at triage, not at report.

## Threat model

This scaffold generates plugin source; it is not a sandbox. An
installed plugin is imported by the host process through the
`pain001.loaders` entry point and runs with that process's permissions.
Review the templates, and any plugin built from them, before execution.

- **Generated code**: the example loader reads tab-separated text,
  keeps every value as a string (no inferred numbers, so leading zeroes
  and decimal scale survive) and refuses malformed headers and record
  widths. It does not infer missing identifiers or amounts.
- **Supply chain**: dependencies are locked in `poetry.lock`, audited
  with pip-audit in CI, and GitHub Actions are pinned by commit.
  Releases carry build provenance and SHA-256 checksums.
- **Data**: fixtures are synthetic; real account data never belongs in
  the repository, an issue or a generated plugin's tests.

No independent security audit has been carried out.

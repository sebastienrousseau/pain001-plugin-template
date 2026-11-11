<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# pain001-plugin-template Governance

This document describes how pain001-plugin-template is run, how decisions
are made, and how to take on responsibility for it. It exists to make the
project legible and sustainable, and to reduce its dependence on any
single person.

## Mission and scope

pain001-plugin-template is a Cookiecutter scaffold for the
[`pain001`](https://github.com/sebastienrousseau/pain001) ISO 20022
library. It generates an installable loader plugin, registered under the
`pain001.loaders` entry point, with tests, lint and CI already in place,
so a third party can add an input format without changing the core.

Changes are weighed against that scope: a correct, small starting point
over a feature-rich one. Anything that belongs to the core's plugin
contract is proposed there, not here.

## Roles

| Role | Who | Can |
| :--- | :--- | :--- |
| **Maintainer** | Listed in [`MAINTAINERS.md`](MAINTAINERS.md) | Merge PRs, cut releases, triage, set direction |
| **Contributor** | Anyone with a merged PR | Propose changes, review, discuss |
| **User** | Everyone | File issues, ask questions, request features |

## Decision making

- **Day-to-day changes** (fixes, docs, tests, template improvements
  within scope) proceed by **lazy consensus**: open a PR; if no
  maintainer objects and CI is green, a maintainer merges it.
- **Significant changes** (a new Cookiecutter prompt, a change to the
  files every generated plugin receives, a new dependency, a raised
  `pain001` floor) need explicit approval from a maintainer in the PR,
  and should start as an issue.
- **Disagreement** is resolved by discussion aiming for consensus; if
  none is reached, the lead maintainer decides and records the
  rationale.

Every change must pass the full gate (100% line and branch coverage of
the scaffold's scripts and of every rendered plugin, the complexity
ceilings, ruff, the release-metadata check) before merge, enforced in
CI, not by trust. Commits carry a Developer Certificate of Origin
sign-off (`git commit -s`; see [`DCO.txt`](DCO.txt)).

## Releases

Releases follow the release model in [`DEVELOPMENT.md`](DEVELOPMENT.md).
Every member of the pain001 suite ships the same version number as the
core; generated third-party plugins keep their own version, starting at
0.0.1. Only maintainers tag releases.

## Becoming a maintainer

More maintainers is the single biggest thing that would de-risk the
project.

1. Contribute a few reviewed PRs ([`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
   is the map; good first areas: a test for a generated-plugin edge
   case, clearer generated documentation).
2. Help triage issues and review others' PRs.
3. Open an issue or email the lead maintainer expressing interest.

A maintainer proposes you; with no objection from existing maintainers
within a week, you are added to `MAINTAINERS.md`.

## Sustainability (bus factor)

pain001-plugin-template has **one** maintainer today. The mitigations in
place:

- **The work is legible:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
  maps the repository and [`DEVELOPMENT.md`](DEVELOPMENT.md) reproduces
  every CI gate and the release model.
- **Quality is enforced by CI,** not by one person's memory.
- **The goal is two or more maintainers** with independent release
  authority.

## Code of conduct and security

Participation follows [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
Security issues follow the private disclosure process in
[`SECURITY.md`](SECURITY.md); please do not open public issues for
vulnerabilities.

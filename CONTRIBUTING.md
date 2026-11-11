<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Contributing

Read [DEVELOPMENT.md](DEVELOPMENT.md) for the toolchain and the local
command behind every CI gate, then run `make check`, `make sec` and
`make docs-lint`, and include tests with every behaviour change.
Change sources, not generated files: the README comes from `docs/`
through `scripts/render_readme.py`, and a generated plugin comes from
`{{cookiecutter.project_name}}/`.

Use conventional, SSH-signed commits with a `Signed-off-by` trailer
(`git commit -s`), which certifies the [Developer Certificate of
Origin](DCO.txt). Do not modify version numbers or publish tags without
a maintainer decision; [GOVERNANCE.md](GOVERNANCE.md) says how
decisions are made. Contributions use Apache-2.0 OR MIT. Never commit
real payment data or keys.

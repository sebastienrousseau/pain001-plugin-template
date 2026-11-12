<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Development

The single entry point for working on `pain001-plugin-template`:
toolchain, how to reproduce every CI gate locally, where tests live,
and how a release happens. [CONTRIBUTING.md](CONTRIBUTING.md) covers the
etiquette (DCO, commit format, review); this file covers the mechanics,
and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) the design.

## Toolchain

| Tool | Version | Where it is pinned |
| :--- | :--- | :--- |
| Python | 3.11 is the floor; CI tests 3.11 and 3.14 | `pyproject.toml`, the `ci.yml` matrix, [toolchain policy](docs/POLICIES.md) |
| Poetry | 2.4.1 in CI | `ci.yml`, `release.yml`, the devcontainer |
| Python packages | exact versions with hashes | `poetry.lock` |
| Node | any current LTS | only for `markdownlint-cli2` in the docs-lint job |
| pre-commit | any | optional; hooks pinned by commit SHA in `.pre-commit-config.yaml` |

```bash
git clone https://github.com/sebastienrousseau/pain001-plugin-template
cd pain001-plugin-template
poetry install --all-extras
pre-commit install        # optional: ruff, codespell and hygiene hooks
make check
make sec
```

The [devcontainer](.devcontainer/devcontainer.json) does the same in a
Codespace or VS Code container and finishes by running `make check`.

## Reproducing every CI gate

| Gate | Local command | CI workflow and job |
| :--- | :--- | :--- |
| Lint and format (ruff, including C901 at 10, and D1: a docstring on every public module, class and function in `scripts/` and the generated plugin) | `make lint` | `ci.yml` check |
| Complexity (cyclomatic 10, cognitive 15, Halstead 30, 60 lines per function, 500 per file) against `complexity-baseline.json`, which only shrinks | `make complexity` | `ci.yml` check |
| Tests with the 100% line and branch coverage floor on `scripts/` | `make test` | `ci.yml` check |
| Render the template, install the plugin, run its tests (100% coverage), ruff and core discovery | `make test` (`tests/test_template.py`) | `ci.yml` check |
| README Quick Start run verbatim | `make test` (`tests/test_readme.py`) | `ci.yml` check |
| README rendered from its sources, canonical sections, links | `make docs` and `make test` | `ci.yml` check |
| Repository-relative links in every Markdown file resolve; suite links name `main` | `make test` (`tests/test_docs_links.py`) | `ci.yml` check |
| Release metadata agrees on one version; release note present | `make versions` | `ci.yml` check, `release.yml` |
| Advisory audit of the locked environment | `make sec` | `ci.yml` check |
| Atheris fuzzing of the example loader against its contract | `python fuzz/fuzz_example_loader.py fuzz/corpus` (Linux x86_64, needs `requirements/fuzz.txt`) | `fuzz.yml` |
| Docs lint (codespell, markdownlint) | `make docs-lint` | `docs-lint.yml` |
| Signed-off-by on every commit | `git commit -s` | `dco.yml` |
| Suite publications agree | none locally (network) | `suite-consistency.yml` (daily) |
| All of the above that run offline | `make check` | |

The coverage floor is 100% line and branch, stated in `pyproject.toml`
`[tool.coverage.report]` for the scaffold and again in the generated
`pyproject.toml` for each plugin. Both code bases are small, and the
branches a lower floor would leave untested are the refusal paths a
plugin author most needs to see working.

## Test layout

```text
tests/
  test_template.py           render, install into a target directory, run
                             the plugin's tests and ruff, check discovery
  test_readme.py             README layout, tokens, links; Quick Start run
  test_docs_links.py         relative links in every Markdown file resolve
  test_scripts.py            scripts/check_release.py, scripts/render_readme.py
  test_check_complexity.py   the complexity gate and its baseline ratchet
  test_fuzz_harness.py       the fuzz harness's contract checks, and a
                             replay of fuzz/corpus/, without Atheris
  test_release_notes.py      vendored with scripts/release_notes.py; do not edit
fuzz/
  fuzz_example_loader.py     Atheris harness for the example loader
  corpus/                    synthetic seed files (first byte: chunk size)
{{cookiecutter.project_name}}/tests/
  test_loader.py             the generated plugin's own tests
```

No test modifies the development environment: plugins are installed
into a temporary target directory or a throwaway virtual environment.
Fixtures are synthetic.

## README

`README.md` is generated. Edit `docs/readme-template.md` (a copy of the
portfolio's canonical layout) or `docs/readme-values.json`, then run
`poetry run python scripts/render_readme.py`. CI fails when the
committed README differs from the rendered one.

## Documentation

`docs/` is the only documentation root: the authoring guide
(`docs/usage.md`), the architecture page, the toolchain policy, and the
README's sources. There is no rendered manual, so there is no docs
build to run with warnings denied; the scaffold's public surface is
four scripts, documented by their docstrings (ruff D1) and by this
file. The plugin contract itself is documented in the core.

## Release model

The version is `0.0.x`, moves in `0.0.1` steps, and ships in lockstep
with the other `pain001` suite members; the 0.0.82 release recorded the
maintainer-authorised adoption of the suite version. Generated plugins
keep their own version, starting at 0.0.1. Work for the next version
happens on `feat/v<next-version>`, the only pull request into `main`.

When the maintainer opens a release, the version moves in
`pyproject.toml` (with the `pain001` floor), the generated
`pyproject.toml` floor, `CITATION.cff`, `SUPPORT.md`, the stability
statement in `docs/readme-values.json` (then re-render the README) and a
new `## [0.0.N]` heading in `CHANGELOG.md`, with a `releases/v0.0.N.md`
note. `make versions` checks they agree. Pushing the signed tag runs
`release.yml`: it repeats the gate, builds the source archive with
SHA-256 sums and build provenance, and publishes the GitHub release with
notes composed by `scripts/release_notes.py`.

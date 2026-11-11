<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

## [Unreleased]

### Added

- Add issue forms, a pull request template, CITATION.cff and a
  markdownlint CI job (`docs-lint.yml`, configured in
  `.markdownlint-cli2.jsonc`).
- Hold the scaffold's scripts to 100% line and branch coverage
  (`tests/test_scripts.py`, pytest-cov, floor in `pyproject.toml`), and
  generated plugins to the same floor: their tests now cover every
  refusal path of the example loader, and `make check` fails if a
  rendered plugin drops below 100%.
- Run the README Quick Start verbatim in `tests/test_readme.py`, offline,
  in a throwaway virtual environment.

### Fixed

- The Quick Start's last step, `pain001 plugins show example`, ran
  whichever `pain001` console script came first on `PATH`, which need
  not belong to the environment the plugin was installed in. It is now
  `python -m pain001 plugins show example`.

## [0.0.85] - 2026-11-10

### Changed

- Release 0.0.85 in lockstep with the pain001 suite and require core
  pain001 0.0.85; the locks resolve its published artifacts. The generated plugin requires it too.

### Fixed

- Generated plugins' CI ran its matrix on Python 3.10, which their
  `requires-python = ">=3.11"` refuses, so the first push of every new
  plugin failed to install it. The matrix is now 3.11 and 3.14, and
  `actions/setup-python` is pinned to the commit the scaffold's own CI
  uses (v7.1.0, was v7.0.0); tests hold both in place.

## [0.0.84] - 2026-11-09

### Added

- Audit all nine suite repositories and their publication channels daily and after publishing workflows, using the shared checker pinned to a core commit.

### Changed

- Release 0.0.84 with the suite and require core pain001 0.0.84. Regenerate dependency locks from the published core artifacts.

## [0.0.83] - 2026-11-09

- Require core pain001 0.0.83 in the scaffold and in generated plugins
  (`pain001>=0.0.83,<1`); `poetry.lock` moves only pain001. Nothing in
  the plugin contract changed: the core's 0.0.83 work is XML signing
  and signature verification.

## [0.0.82] - 2026-11-09

- Require core pain001 0.0.82 and Python 3.11 in the scaffold and generated
  plugins; verify generated dependency metadata against the suite version.
- Publish a signed source release with build provenance and complete asset
  checksums. Refresh pending pytest, hatchling and filelock updates.
- Scaffold an external loader with Cookiecutter, entry-point packaging,
  bounded streaming, text-preservation checks and generated tests.
- Verify real package installation and core plugin discovery in CI.
- Floor `certifi >= 2026.10.19` (PYSEC-2026-4320, GHSA-6q48-6c7w-9gw2)
  and, for the dev group, `filelock >= 4.2.1` (GHSA-9vhv-jxww-xfm5,
  GHSA-567q-5qvw-pf92, GHSA-v4x8-3wr5-3wq8). the scaffold now requires
  Python 3.11 and runs pip-audit on every CI leg.
- Move ruff to 0.17.3.

This first tagged release adopts the pain001 suite version by maintainer
decision. Generated third-party plugins retain their own initial version.

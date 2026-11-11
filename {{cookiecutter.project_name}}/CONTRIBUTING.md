<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Contributing

Thank you for helping. Before opening a pull request:

1. Install with `python -m pip install -e '.[dev]'`.
2. Add or update tests with every behaviour change; `python -m pytest`
   must keep 100% line and branch coverage.
3. Run `ruff check .` and `ruff format --check .`.
4. Record the change under `## [Unreleased]` in `CHANGELOG.md`.

Use synthetic data only: no real account numbers, personal data or
bank-restricted material in code, tests or issues. Contributions are
accepted under Apache-2.0 OR MIT.

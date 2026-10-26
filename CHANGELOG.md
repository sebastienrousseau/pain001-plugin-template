<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

## [0.0.1] - Unreleased

- Scaffold an external loader with Cookiecutter, entry-point packaging,
  bounded streaming, text-preservation checks and generated tests.
- Verify real package installation and core plugin discovery in CI.
- Floor `certifi >= 2026.10.19` (PYSEC-2026-4320, GHSA-6q48-6c7w-9gw2)
  and, for the dev group, `filelock >= 4.2.1` (GHSA-9vhv-jxww-xfm5,
  GHSA-567q-5qvw-pf92, GHSA-v4x8-3wr5-3wq8). filelock 4.2.1 needs
  Python 3.11, so pip-audit installs only there and `make sec` skips it
  on 3.10; the 3.14 job audits.
- Move ruff to 0.17.1.

This initial development iteration is not a tagged release.

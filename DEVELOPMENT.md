<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Development

Run `poetry install`, `poetry run make check` and `poetry run make sec`.
Integration tests render the template, install the generated package into an
isolated target directory, run its tests, and check core entry-point discovery.
No global environment is modified.

Only files under the Cookiecutter project directory become generated plugin
files. Use synthetic fixtures and preserve the core plugin contract.
The contract remains pre-1.0; an independent external author must validate
the design before it is locked. Our generated tests are not that endorsement.

README evidence is in `docs/readme-values.json`; regenerate with
`poetry run python scripts/render_readme.py`. Its layout is the unchanged
portfolio template vendored under `docs/`.

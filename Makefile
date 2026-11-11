# SPDX-License-Identifier: Apache-2.0 OR MIT
# Developer targets; CI runs the same ones. DEVELOPMENT.md maps each to
# its workflow job.
.PHONY: check lint complexity test sec docs docs-lint versions demo
check: lint complexity test docs versions
lint:
	poetry run ruff check tests scripts
	poetry run ruff format --check tests scripts
complexity:
	poetry run python scripts/check_complexity.py
	poetry run complexipy scripts tests '{{cookiecutter.project_name}}/{{cookiecutter.module_name}}' --max-complexity-allowed 15 --quiet
test:
	poetry run pytest
sec:
	poetry run pip-audit --progress-spinner off
docs:
	poetry run python scripts/render_readme.py --check
docs-lint:
	poetry run codespell
	npx --yes markdownlint-cli2@0.23.3 "**/*.md"
versions:
	poetry run python scripts/check_release.py
	poetry run python scripts/release_notes.py check

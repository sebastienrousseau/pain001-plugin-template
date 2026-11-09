# SPDX-License-Identifier: Apache-2.0 OR MIT
.PHONY: check lint test sec docs versions
check: lint test docs versions
lint:
	poetry run ruff check tests scripts
	poetry run ruff format --check tests scripts
test:
	poetry run pytest
sec:
	poetry run pip-audit --progress-spinner off
docs:
	poetry run python scripts/render_readme.py --check
versions:
	poetry run python scripts/check_release.py
	poetry run python scripts/release_notes.py check

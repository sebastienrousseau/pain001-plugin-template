# SPDX-License-Identifier: Apache-2.0 OR MIT
.PHONY: check lint test sec docs
check: lint test docs
lint:
	poetry run ruff check tests scripts
	poetry run ruff format --check tests scripts
test:
	poetry run pytest
sec:
	poetry run pip-audit --progress-spinner off
docs:
	poetry run python scripts/render_readme.py --check

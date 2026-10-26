# SPDX-License-Identifier: Apache-2.0 OR MIT
.PHONY: check lint test sec docs
check: lint test docs
lint:
	poetry run ruff check tests scripts
	poetry run ruff format --check tests scripts
test:
	poetry run pytest
sec:
	@# pip-audit installs only on Python 3.11+ (its filelock fix needs 3.11).
	@if poetry run python -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then \
		poetry run pip-audit --progress-spinner off; \
	else \
		echo "pip-audit skipped: it needs Python 3.11+; the 3.14 job audits"; \
	fi
docs:
	poetry run python scripts/render_readme.py --check

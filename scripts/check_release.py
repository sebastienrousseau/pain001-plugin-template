# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Check the scaffold release and the generated plugin's core requirement."""

import os
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scaffold_version() -> str:
    """Return the scaffold's version after checking its own floors."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"][
        "poetry"
    ]
    version = project["version"]
    assert project["dependencies"]["pain001"] == f">={version},<1"
    assert project["dependencies"]["python"] == ">=3.11,<4"
    return version


def check_generated(version: str) -> None:
    """Refuse a generated plugin that does not require this core."""
    template = ROOT / "{{cookiecutter.project_name}}" / "pyproject.toml"
    generated = tomllib.loads(template.read_text())["project"]
    assert generated["dependencies"] == [f"pain001>={version},<1"]
    assert generated["requires-python"] == ">=3.11"
    assert generated["version"] == "0.0.1"


def check_documents(version: str) -> None:
    """Refuse a changelog, README or release note that names another."""
    assert f"## [{version}] - " in (ROOT / "CHANGELOG.md").read_text()
    readme = (ROOT / "README.md").read_text()
    assert f"Version {version}, in lockstep" in readme
    assert not re.search(r"\{\{[A-Z_]+\}\}", readme)
    assert (ROOT / "releases" / f"v{version}.md").is_file()


def main() -> None:
    """Refuse inconsistent scaffold and generated-plugin release metadata."""
    version = scaffold_version()
    check_generated(version)
    check_documents(version)
    if os.environ.get("GITHUB_REF_TYPE") == "tag":
        assert os.environ["GITHUB_REF_NAME"] == f"v{version}"
    print(f"scaffold and generated core requirement agree on {version}")


if __name__ == "__main__":
    main()

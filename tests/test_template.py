# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Render, install and discover a real third-party entry-point plugin."""

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from cookiecutter.main import cookiecutter
from packaging.specifiers import SpecifierSet


@pytest.mark.parametrize(
    "name", ["pain001-loader-example", "pain001-loader-custom"]
)
def test_render_install_discover(tmp_path, name):
    """The scaffold installs and is discovered without editing core."""
    root = Path(__file__).resolve().parents[1]
    project = cookiecutter(
        str(root),
        no_input=True,
        default_config={"replay_dir": str(tmp_path / "replay")},
        output_dir=str(tmp_path),
        extra_context={"project_name": name},
    )
    target = tmp_path / "installed"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-build-isolation",
            "--target",
            str(target),
            project,
        ],
        check=True,
    )
    environment = dict(os.environ, PYTHONPATH=str(target))
    subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider"],
        cwd=project,
        env=environment,
        check=True,
    )
    code = (
        "from pain001.plugins.registry import registry; "
        "loader=registry.get_loader('example'); "
        "assert loader is not None; "
        f"assert loader.meta.source.startswith('{name}=='); "
        "print(loader.meta.source)"
    )
    subprocess.run([sys.executable, "-c", code], env=environment, check=True)
    subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."], cwd=project, check=True
    )
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        cwd=project,
        check=True,
    )


def test_generated_plugin_requires_the_current_suite(tmp_path):
    """A new plugin declares the core release used to validate the scaffold."""
    root = Path(__file__).resolve().parents[1]
    version = tomllib.loads((root / "pyproject.toml").read_text())["tool"][
        "poetry"
    ]["version"]
    project = Path(
        cookiecutter(
            str(root),
            no_input=True,
            output_dir=str(tmp_path),
            default_config={"replay_dir": str(tmp_path / "replay")},
        )
    )
    metadata = tomllib.loads((project / "pyproject.toml").read_text())[
        "project"
    ]
    assert metadata["dependencies"] == [f"pain001>={version},<1"]
    assert metadata["requires-python"] == ">=3.11"


def _render(tmp_path):
    """Render the scaffold with its defaults and return the project path."""
    root = Path(__file__).resolve().parents[1]
    return Path(
        cookiecutter(
            str(root),
            no_input=True,
            output_dir=str(tmp_path),
            default_config={"replay_dir": str(tmp_path / "replay")},
        )
    )


def _actions(workflow):
    """Map each action a workflow uses to the commit it is pinned to."""
    steps = [
        step
        for job in yaml.safe_load(workflow.read_text())["jobs"].values()
        for step in job["steps"]
        if "uses" in step
    ]
    return dict(step["uses"].split("@", 1) for step in steps)


def test_generated_ci_tests_only_supported_pythons(tmp_path):
    """Every Python the generated CI runs on can install the plugin."""
    project = _render(tmp_path)
    requires = tomllib.loads((project / "pyproject.toml").read_text())[
        "project"
    ]["requires-python"]
    workflow = yaml.safe_load(
        (project / ".github" / "workflows" / "ci.yml").read_text()
    )
    pythons = workflow["jobs"]["test"]["strategy"]["matrix"]["python"]
    unsupported = [v for v in pythons if v not in SpecifierSet(requires)]
    assert not unsupported, f"{unsupported} do not satisfy {requires}"


def test_generated_ci_pins_the_scaffold_actions(tmp_path):
    """Dependabot moves the scaffold's pins; generated plugins follow."""
    root = Path(__file__).resolve().parents[1]
    project = _render(tmp_path)
    ours = _actions(root / ".github" / "workflows" / "ci.yml")
    generated = _actions(project / ".github" / "workflows" / "ci.yml")
    assert generated == {action: ours[action] for action in generated}


# Jinja that survived rendering; GitHub's own ${{ }} expressions are fine.
JINJA = re.compile(r"\{\{\s*cookiecutter|\{%")

GENERATED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "LICENSE-APACHE",
    "LICENSE-MIT",
    ".editorconfig",
    ".gitignore",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    "pyproject.toml",
]


def _unrendered(project):
    """Return the text files in ``project`` that still hold Jinja."""
    return [
        path.relative_to(project).as_posix()
        for path in project.rglob("*")
        if path.suffix in {".md", ".py", ".toml", ".yml"}
        and JINJA.search(path.read_text())
    ]


def test_generated_project_is_a_complete_repository(tmp_path):
    """A new plugin starts with its community files and no template left."""
    project = _render(tmp_path)
    missing = [
        name for name in GENERATED_FILES if not (project / name).is_file()
    ]
    assert not missing, missing
    leftovers = _unrendered(project)
    assert not leftovers, leftovers
    readme = (project / "README.md").read_text()
    assert readme.startswith("<!-- SPDX-License-Identifier:")
    assert "# pain001-loader-example\n" in readme
    assert "python -m pain001 plugins show example" in readme

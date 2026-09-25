# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Render, install and discover a real third-party entry-point plugin."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


@pytest.mark.parametrize(
    "name", ["pain001-loader-example", "pain001-loader-custom"]
)
def test_render_install_discover(tmp_path, name):
    """The scaffold installs and is discovered without editing core."""
    root = Path(__file__).resolve().parents[1]
    project = cookiecutter(
        str(root),
        no_input=True,
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
        [sys.executable, "-m", "pytest", str(Path(project) / "tests"), "-q"],
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

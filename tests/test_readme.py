# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Run the README Quick Start as written.

The commands are taken from the rendered README and run in one bash
session, so a change to the scaffold, to cookiecutter or to the core
CLI fails here rather than in a reader's terminal. Two things differ
from a reader's machine, neither in the commands themselves: the
output directory is a temporary one, and ``python`` is a fresh virtual
environment that sees this checkout's locked packages through a
``.pth`` file, so ``pip install`` runs offline and leaves the
development environment untouched.
"""

from __future__ import annotations

import os
import re
import subprocess
import sysconfig
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
OUTPUT_DIR = "/tmp/pain001-plugins"


def _section(title: str) -> str:
    """Return the body of the ``## title`` section of the README."""
    return README.split(f"\n## {title}\n", 1)[1].split("\n---", 1)[0]


def _quick_start() -> str:
    """Return the Quick Start shell block."""
    block = re.search(r"```sh\n(.*?)\n```", _section("Quick Start"), re.S)
    assert block is not None, "Quick Start has no sh block"
    return block[1]


def _isolated_python(tmp_path: Path) -> Path:
    """Create a virtual environment that can import the locked packages."""
    home = tmp_path / "venv"
    venv.EnvBuilder(with_pip=False).create(home)
    purelib = subprocess.run(
        [
            str(home / "bin" / "python"),
            "-c",
            "import sysconfig; print(sysconfig.get_paths()['purelib'])",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    ours = sysconfig.get_paths()["purelib"]
    (Path(purelib) / "locked.pth").write_text(ours + "\n", encoding="utf-8")
    return home / "bin"


def test_quick_start_runs_verbatim(tmp_path: Path) -> None:
    """Render, install, test and discover a plugin with the README steps."""
    script = _quick_start()
    assert OUTPUT_DIR in script
    output = tmp_path / "plugins"
    bindir = _isolated_python(tmp_path)
    environment = dict(
        os.environ,
        PATH=f"{bindir}{os.pathsep}{os.environ['PATH']}",
        PIP_NO_INDEX="1",
        PIP_NO_BUILD_ISOLATION="0",
        PIP_DISABLE_PIP_VERSION_CHECK="1",
    )
    result = subprocess.run(
        [
            "bash",
            "-euo",
            "pipefail",
            "-c",
            script.replace(OUTPUT_DIR, str(output)),
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "pain001-loader-example==0.0.1" in result.stdout

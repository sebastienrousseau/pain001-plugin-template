# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Keep the README canonical and run its Quick Start as written.

The README is rendered from ``docs/readme-template.md`` (a byte-identical
copy of the portfolio's canonical layout) and ``docs/readme-values.json``.
These tests hold the result to the canonical section order and refuse
unresolved ``{{TOKEN}}`` placeholders and dangling repository links.

The Quick Start commands are taken from the rendered README and run in one bash
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

# The second-level headings of ~/Code/README-TEMPLATE.md, in order.
CANONICAL_SECTIONS = [
    "Contents",
    "Install",
    "Requirements",
    "Quick Start",
    "The pain001-plugin-template ecosystem",
    "Capabilities at a glance",
    "Ecosystem comparison",
    "Benchmarks",
    "Features",
    "Configuration",
    "Examples",
    "When not to use pain001-plugin-template",
    "Development",
    "Security",
    "Documentation",
    "Stability guarantees",
    "License",
]


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


def test_readme_has_no_unresolved_tokens() -> None:
    """Every template placeholder was filled from readme-values.json."""
    assert not re.findall(r"\{\{[A-Z_]+\}\}", README)


def test_readme_sections_follow_the_canonical_order() -> None:
    """The README keeps the canonical headings, in order, and no others."""
    assert re.findall(r"^## (.+)$", README, re.M) == CANONICAL_SECTIONS


def test_readme_template_keeps_the_canonical_layout() -> None:
    """The vendored template has exactly the canonical sections."""
    template = (ROOT / "docs" / "readme-template.md").read_text()
    headings = re.findall(r"^## (.+)$", template, re.M)
    expected = [
        h.replace("pain001-plugin-template", "{{PROJECT_NAME}}")
        for h in CANONICAL_SECTIONS
    ]
    assert headings == expected


def test_readme_repository_links_resolve() -> None:
    """Every relative link and image in the README points at a file."""
    targets = re.findall(r"\]\(([^)]+)\)", README)
    targets += re.findall(r'(?:src|href)="([^"]+)"', README)
    local = [t for t in targets if "://" not in t and not t.startswith("#")]
    assert local
    missing = [t for t in local if not (ROOT / t.split("#")[0]).exists()]
    assert not missing, missing


def test_every_readme_image_is_an_absolute_url() -> None:
    """PyPI does not resolve relative paths, so every image is absolute."""
    sources = re.findall(r'(?:src|srcset)="([^"]+)"', README)
    assert sources
    assert all(source.startswith("https://") for source in sources), sources
    prefix = (
        "https://raw.githubusercontent.com/sebastienrousseau/"
        "pain001-plugin-template/main/"
    )
    tree = [s.removeprefix(prefix) for s in sources if s.startswith(prefix)]
    assert {"docs/logo.svg", ".github/demo.gif"} <= set(tree)
    assert all((ROOT / path).is_file() for path in tree), tree

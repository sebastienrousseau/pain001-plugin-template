# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Every repository-relative link in the Markdown docs resolves.

This walks the Markdown sources, including the files a generated plugin
receives (their links are relative to the template directory, which is
where they will sit once rendered), offline, and fails on any link or
image whose target file is gone. Links into the suite's own GitHub
repositories must name ``main``: a link to a release branch breaks when
the branch is deleted after its merge.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
# Generated, cached or third-party trees, and the README template, whose
# links are written relative to the README it renders.
SKIP_DIRS = {"node_modules", "mutants", "_build", "htmlcov"}
SKIP_FILES = {ROOT / "docs" / "readme-template.md"}
LINK = re.compile(r"\]\(([^)\s]+)\)|(?:src|href)=\"([^\"]+)\"")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
SUITE_FILE = re.compile(
    r"https://github\.com/sebastienrousseau/pain001[\w.-]*/((?:blob|tree)/[^)\s\"]+)"
)


def _markdown_files() -> list[Path]:
    """Return every Markdown source in the repository."""
    found = []
    for path in sorted(ROOT.rglob("*.md")):
        parts = path.relative_to(ROOT).parts
        hidden = any(p.startswith(".") and p != ".github" for p in parts)
        if hidden or SKIP_DIRS.intersection(parts) or path in SKIP_FILES:
            continue
        found.append(path)
    return found


def _local_targets(text: str) -> list[str]:
    """Return the repository-relative link targets outside code spans."""
    targets = [a or b for a, b in LINK.findall(CODE.sub("", text))]
    return [
        t
        for t in targets
        if "://" not in t and not t.startswith(("#", "mailto:"))
    ]


MARKDOWN = _markdown_files()


def test_markdown_sources_are_found() -> None:
    """The walk sees the README, the guides and the generated README."""
    names = {p.relative_to(ROOT).as_posix() for p in MARKDOWN}
    expected = {
        "README.md",
        "docs/usage.md",
        "docs/ARCHITECTURE.md",
        "{{cookiecutter.project_name}}/README.md",
    }
    assert expected <= names


@pytest.mark.parametrize(
    "path", MARKDOWN, ids=lambda p: p.relative_to(ROOT).as_posix()
)
def test_relative_links_resolve(path: Path) -> None:
    """Each relative link in ``path`` names a file that exists."""
    text = path.read_text(encoding="utf-8")
    missing = [
        target
        for target in _local_targets(text)
        if not (path.parent / target.split("#")[0]).exists()
    ]
    assert not missing, missing


@pytest.mark.parametrize(
    "path", MARKDOWN, ids=lambda p: p.relative_to(ROOT).as_posix()
)
def test_suite_links_name_the_default_branch(path: Path) -> None:
    """A link to a file in a suite repository points at ``main``."""
    text = path.read_text(encoding="utf-8")
    stale = [
        link
        for link in SUITE_FILE.findall(text)
        if not link.startswith(("blob/main/", "tree/main/"))
    ]
    assert not stale, stale

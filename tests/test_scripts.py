# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Tests for the release gate and the README renderer under scripts/."""

from __future__ import annotations

import importlib.util
import re
import runpy
import shutil
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> ModuleType:
    """Import ``scripts/<name>.py`` as a module without touching sys.path."""
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_release = _load("check_release")
render_readme = _load("render_readme")


def _copy_tree(tmp_path: Path) -> Path:
    """Copy what the two scripts read into ``tmp_path`` and return it."""
    for name in ("pyproject.toml", "CHANGELOG.md", "README.md"):
        shutil.copy(ROOT / name, tmp_path / name)
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    shutil.copytree(ROOT / "releases", tmp_path / "releases")
    template = "{{cookiecutter.project_name}}"
    (tmp_path / template).mkdir()
    shutil.copy(
        ROOT / template / "pyproject.toml",
        tmp_path / template / "pyproject.toml",
    )
    return tmp_path


def test_release_gate_accepts_the_repository(capsys, monkeypatch):
    """The committed metadata agrees on one version."""
    monkeypatch.delenv("GITHUB_REF_TYPE", raising=False)
    check_release.main()
    assert "agree on" in capsys.readouterr().out


def test_release_gate_accepts_the_matching_tag(monkeypatch):
    """On a tag build the tag must name the manifest version."""
    version = check_release.tomllib.loads(
        (ROOT / "pyproject.toml").read_text()
    )["tool"]["poetry"]["version"]
    monkeypatch.setenv("GITHUB_REF_TYPE", "tag")
    monkeypatch.setenv("GITHUB_REF_NAME", f"v{version}")
    check_release.main()


def test_release_gate_refuses_another_tag(monkeypatch):
    """A tag that names another version stops the release."""
    monkeypatch.setenv("GITHUB_REF_TYPE", "tag")
    monkeypatch.setenv("GITHUB_REF_NAME", "v0.0.0")
    with pytest.raises(AssertionError):
        check_release.main()


def test_release_gate_refuses_a_stale_generated_floor(tmp_path, monkeypatch):
    """A generated plugin that requires an older core is refused."""
    root = _copy_tree(tmp_path)
    manifest = root / "{{cookiecutter.project_name}}" / "pyproject.toml"
    text = manifest.read_text()
    floor = re.search(r'"pain001>=([0-9.]+),<1"', text)[1]
    manifest.write_text(text.replace(f"pain001>={floor}", "pain001>=0.0.1"))
    monkeypatch.setattr(check_release, "ROOT", root)
    with pytest.raises(AssertionError):
        check_release.main()


def test_release_gate_runs_as_a_script(capsys, monkeypatch):
    """``python scripts/check_release.py`` runs the gate."""
    monkeypatch.delenv("GITHUB_REF_TYPE", raising=False)
    runpy.run_path(
        str(ROOT / "scripts" / "check_release.py"), run_name="__main__"
    )
    assert "agree on" in capsys.readouterr().out


def test_render_check_accepts_the_committed_readme(monkeypatch):
    """``--check`` passes when README.md matches its sources."""
    monkeypatch.setattr("sys.argv", ["render_readme.py", "--check"])
    render_readme.main()


@pytest.mark.parametrize("readme", ["stale\n", None])
def test_render_check_refuses_drift(tmp_path, monkeypatch, readme):
    """``--check`` fails on a stale or missing README.md."""
    root = _copy_tree(tmp_path)
    if readme is None:
        (root / "README.md").unlink()
    else:
        (root / "README.md").write_text(readme)
    monkeypatch.setattr(render_readme, "ROOT", root)
    monkeypatch.setattr("sys.argv", ["render_readme.py", "--check"])
    with pytest.raises(SystemExit, match="stale"):
        render_readme.main()


def test_render_writes_the_readme(tmp_path, monkeypatch):
    """Without ``--check`` the renderer rewrites README.md."""
    root = _copy_tree(tmp_path)
    (root / "README.md").write_text("old\n")
    monkeypatch.setattr(render_readme, "ROOT", root)
    monkeypatch.setattr("sys.argv", ["render_readme.py"])
    render_readme.main()
    assert (root / "README.md").read_text() == (ROOT / "README.md").read_text()


def test_render_runs_as_a_script(monkeypatch):
    """``python scripts/render_readme.py --check`` runs the check."""
    monkeypatch.setattr("sys.argv", ["render_readme.py", "--check"])
    runpy.run_path(
        str(ROOT / "scripts" / "render_readme.py"), run_name="__main__"
    )

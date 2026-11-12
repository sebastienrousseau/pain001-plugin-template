# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Run the Atheris harness's contract without Atheris.

Atheris ships Linux x86_64 wheels only, so the fuzz job runs it there;
these tests stand in a recording stub for it, replay the seed corpus and
show that each contract check fails on a loader that breaks it.
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "fuzz" / "fuzz_example_loader.py"
CORPUS = sorted((ROOT / "fuzz" / "corpus").iterdir())


@pytest.fixture
def harness(monkeypatch):
    """Import the harness with a stub ``atheris`` that records calls."""
    calls = []
    stub = types.ModuleType("atheris")
    stub.instrument_func = lambda function: calls.append(function)
    stub.Setup = lambda argv, target: calls.append(("Setup", target))
    stub.Fuzz = lambda: calls.append("Fuzz")
    monkeypatch.setitem(sys.modules, "atheris", stub)
    spec = importlib.util.spec_from_file_location("fuzz_harness", HARNESS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.calls = calls
    return module


def test_instruments_the_loader(harness):
    names = [function.__name__ for function in harness.calls]
    assert names == [
        "_check_headers",
        "_check_width",
        "load",
        "load_streaming",
    ]


@pytest.mark.parametrize("seed", CORPUS, ids=[path.name for path in CORPUS])
def test_corpus_holds_the_contract(harness, seed):
    harness.test_one_input(seed.read_bytes())


def test_seeds_reach_rows_and_refusals(harness):
    harness.test_one_input((ROOT / "fuzz/corpus/valid.tsv").read_bytes())
    assert len(harness.LOADER.load(str(harness.INPUT)).rows) == 2
    harness.test_one_input((ROOT / "fuzz/corpus/too-wide.tsv").read_bytes())
    with pytest.raises(ValueError, match="width"):
        harness.LOADER.load(str(harness.INPUT))


def _rows(*rows):
    return types.SimpleNamespace(rows=list(rows))


def test_flags_a_row_whose_keys_differ(harness, monkeypatch):
    monkeypatch.setattr(
        harness.LOADER, "load", lambda path: _rows({"a": "1"}, {"b": "2"})
    )
    with pytest.raises(AssertionError, match="row keys differ"):
        harness.test_one_input(b"1a\n1\n")


def test_flags_a_value_that_is_not_text(harness, monkeypatch):
    monkeypatch.setattr(harness.LOADER, "load", lambda path: _rows({"a": 1}))
    with pytest.raises(AssertionError, match="non-text value"):
        harness.test_one_input(b"1a\n1\n")


def test_flags_an_oversized_chunk(harness, monkeypatch):
    monkeypatch.setattr(
        harness.LOADER,
        "load_streaming",
        lambda path, size: [_rows({"a": "1"}, {"a": "2"})],
    )
    with pytest.raises(AssertionError, match="chunk outside 1..1 rows"):
        harness.test_one_input(b"\x00a\n1\n2\n")


def test_flags_streaming_that_differs_from_load(harness, monkeypatch):
    # load reads through load_streaming, so the stub goes on load: it
    # reports a row the file (and so the real streaming path) lacks.
    monkeypatch.setattr(
        harness.LOADER, "load", lambda path: _rows({"a": "1"}, {"a": "2"})
    )
    with pytest.raises(AssertionError, match="differs from load"):
        harness.test_one_input(b"1a\n1\n")


def test_main_hands_the_target_to_libfuzzer(harness):
    harness.main()
    assert harness.calls[-2:] == [("Setup", harness.test_one_input), "Fuzz"]

# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Coverage-guided fuzzing of the scaffold's example loader with Atheris.

Every generated plugin starts from the loader in
``{{cookiecutter.project_name}}/{{cookiecutter.module_name}}``. Its Jinja
placeholders sit inside string literals, so the file is valid Python
before rendering and is loaded here by path.

The contract: on any file the loader either raises ``ValueError`` (a
decoding error is one) or returns rows whose keys are the header and
whose values are all text, and ``load_streaming`` yields the same rows as
``load`` in non-empty chunks no larger than the chunk size. Any other
exception, or a broken row, is a crash that libFuzzer reports.

The first byte of an input picks the chunk size (1 to 8); the rest is the
file. The files in ``fuzz/corpus/`` are seeds in that shape.

Run (Linux x86_64, Python 3.12)::

    pip install --require-hashes -r requirements/fuzz.txt
    python fuzz/fuzz_example_loader.py fuzz/corpus -max_total_time=60
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

import atheris

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (
    ROOT
    / "{{cookiecutter.project_name}}"
    / "{{cookiecutter.module_name}}"
    / "__init__.py"
)
INPUT = Path(tempfile.mkdtemp(prefix="fuzz-loader-")) / "input.tsv"


def _load_module():
    """Import the scaffold's loader module from its template path."""
    spec = importlib.util.spec_from_file_location("example_loader", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for function in (
        module._check_headers,
        module._check_width,
        module.ExampleLoader.load,
        module.ExampleLoader.load_streaming,
    ):
        atheris.instrument_func(function)
    return module


LOADER = _load_module().ExampleLoader()


def _check_rows(rows: list) -> None:
    """Every row has the header's keys and a text value for each."""
    header = list(rows[0]) if rows else []
    for row in rows:
        if list(row) != header:
            raise AssertionError(f"row keys differ from header: {row!r}")
        if not all(isinstance(value, str) for value in row.values()):
            raise AssertionError(f"non-text value in row: {row!r}")


def _check_chunks(chunks: list, size: int, rows: list) -> None:
    """Chunks are non-empty, bounded, and add up to ``load``'s rows."""
    if any(not chunk.rows or len(chunk.rows) > size for chunk in chunks):
        raise AssertionError(f"chunk outside 1..{size} rows")
    streamed = [row for chunk in chunks for row in chunk.rows]
    if streamed != rows:
        raise AssertionError("load_streaming differs from load")


def test_one_input(data: bytes) -> None:
    """Load one input both ways and hold the result to the contract."""
    size = 1 + data[0] % 8 if data else 1
    INPUT.write_bytes(data[1:])
    try:
        rows = LOADER.load(str(INPUT)).rows
    except ValueError:
        return
    _check_rows(rows)
    _check_chunks(list(LOADER.load_streaming(str(INPUT), size)), size, rows)


def main() -> None:
    """Hand the harness to libFuzzer."""
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":  # pragma: no cover - the libFuzzer entry point
    main()

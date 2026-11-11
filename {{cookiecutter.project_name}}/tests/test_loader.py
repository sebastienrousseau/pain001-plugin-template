# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Generated tests exercise the same protocol used by core dispatch."""

import pytest
from pain001.plugins import PAIN001_API_VERSION, AbstractLoader

from {{ cookiecutter.module_name }} import ExampleLoader, __version__

HEADER = "id\tpayment_amount\n"


def _write(tmp_path, text):
    """Write ``text`` to a payments file and return its path as a string."""
    path = tmp_path / "payments{{ cookiecutter.file_extension }}"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_protocol_and_text_preservation(tmp_path):
    """Text must retain leading zeroes and decimal scale."""
    path = _write(tmp_path, HEADER + "001\t12.30\n")
    loader = ExampleLoader()
    assert isinstance(loader, AbstractLoader)
    expected = [{"id": "001", "payment_amount": "12.30"}]
    assert loader.load(path).rows == expected
    assert loader.load(path).source_hint == path
    assert next(iter(loader.load_streaming(path, 1))).rows == expected


def test_metadata_matches_the_package():
    """Discovery reads the name, version and contract version from meta."""
    meta = ExampleLoader.meta
    assert meta.name == "{{ cookiecutter.plugin_name }}"
    assert meta.version == __version__
    assert meta.api_version == PAIN001_API_VERSION
    assert ExampleLoader.extensions == ("{{ cookiecutter.file_extension }}",)


def test_streaming_respects_the_chunk_size(tmp_path):
    """Full chunks are yielded as they fill; the remainder comes last."""
    rows = "".join(f"{n:03}\t{n}.00\n" for n in range(5))
    chunks = list(
        ExampleLoader().load_streaming(_write(tmp_path, HEADER + rows), 2)
    )
    assert [len(chunk.rows) for chunk in chunks] == [2, 2, 1]
    assert chunks[-1].rows == [{"id": "004", "payment_amount": "4.00"}]


def test_exact_multiple_yields_no_empty_chunk(tmp_path):
    """A record count divisible by the chunk size ends on a full chunk."""
    path = _write(tmp_path, HEADER + "001\t1.00\n002\t2.00\n")
    chunks = list(ExampleLoader().load_streaming(path, 2))
    assert [len(chunk.rows) for chunk in chunks] == [2]


def test_header_only_file_has_no_records(tmp_path):
    """A header with no records loads as an empty result."""
    assert ExampleLoader().load(_write(tmp_path, HEADER)).rows == []


@pytest.mark.parametrize("size", [0, -1])
def test_chunk_size_must_be_positive(tmp_path, size):
    """A non-positive chunk size is refused before the file is read."""
    with pytest.raises(ValueError, match="chunk_size"):
        list(ExampleLoader().load_streaming(_write(tmp_path, HEADER), size))


@pytest.mark.parametrize(
    "text",
    ["", "id\t\n", "id\tid\n"],
    ids=["no-header", "empty-name", "duplicate-name"],
)
def test_malformed_headers_are_refused(tmp_path, text):
    """Column names must be present, non-empty and unique."""
    with pytest.raises(ValueError, match="column names"):
        ExampleLoader().load(_write(tmp_path, text))


@pytest.mark.parametrize(
    "row", ["001\t12.30\textra\n", "001\n"], ids=["too-wide", "too-narrow"]
)
def test_record_width_must_match_the_header(tmp_path, row):
    """A record with more or fewer fields than the header is refused."""
    with pytest.raises(ValueError, match="width"):
        ExampleLoader().load(_write(tmp_path, HEADER + row))

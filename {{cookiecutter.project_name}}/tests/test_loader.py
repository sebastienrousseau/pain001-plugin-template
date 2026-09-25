# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Generated tests exercise the same protocol used by core dispatch."""

from pain001.plugins import AbstractLoader

from {{ cookiecutter.module_name }} import ExampleLoader


def test_protocol_and_text_preservation(tmp_path):
    """Text must retain leading zeroes and decimal scale."""
    path = tmp_path / "payments{{ cookiecutter.file_extension }}"
    path.write_text("id\tpayment_amount\n001\t12.30\n", encoding="utf-8")
    loader = ExampleLoader()
    assert isinstance(loader, AbstractLoader)
    expected = [{"id": "001", "payment_amount": "12.30"}]
    assert loader.load(str(path)).rows == expected
    assert next(iter(loader.load_streaming(str(path), 1))).rows == expected

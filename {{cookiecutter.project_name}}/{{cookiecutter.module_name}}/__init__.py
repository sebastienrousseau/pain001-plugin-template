# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Example external loader; replace the parser with your format's reader."""

import csv
from collections.abc import Iterable

from pain001.plugins import PAIN001_API_VERSION, LoaderResult, PluginMeta

__version__ = "0.0.1"


class ExampleLoader:
    """Read tab-separated records with a header and preserve text values."""

    meta = PluginMeta(
        name="{{ cookiecutter.plugin_name }}",
        version=__version__,
        description="Read tab-separated flat payment records.",
        api_version=PAIN001_API_VERSION,
    )
    extensions = ("{{ cookiecutter.file_extension }}",)

    def load(self, path: str) -> LoaderResult:
        """Materialize the same records as the streaming path."""
        rows = [
            row
            for chunk in self.load_streaming(path, 1000)
            for row in chunk.rows
        ]
        return LoaderResult(rows=rows, source_hint=path)

    def load_streaming(
        self, path: str, chunk_size: int
    ) -> Iterable[LoaderResult]:
        """Read bounded chunks; reject malformed headers and row widths."""
        if chunk_size < 1:
            raise ValueError("chunk_size must be positive")
        with open(path, newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            headers = reader.fieldnames
            if (
                not headers
                or any(not name for name in headers)
                or len(set(headers)) != len(headers)
            ):
                raise ValueError("Expected unique, non-empty column names")
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Record width differs from the header")
                rows.append(row)
                if len(rows) == chunk_size:
                    yield LoaderResult(rows=rows, source_hint=path)
                    rows = []
            if rows:
                yield LoaderResult(rows=rows, source_hint=path)

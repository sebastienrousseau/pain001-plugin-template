<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Author a loader plugin

Run `poetry run cookiecutter .` and choose an unused package and plugin name.
Install the generated project using `python -m pip install -e '.[dev]'`.
`pain001 plugins show example` then reports the installed distribution as
the source. Files with the selected extension are automatically dispatched.

The example is a tab-separated parser with a header row. It preserves every
value as text, checks row widths, and yields bounded streaming batches.
Replace its parser, not the four required members: `meta`, `extensions`,
`load(path)` and `load_streaming(path, chunk_size)`. Return `LoaderResult`
with flat payment rows. Let schema validation and scheme checks run afterward.

Package entry points are the discovery mechanism. The four groups are
`pain001.loaders`, `pain001.validators`, `pain001.schemes` and `pain001.writers`.
Their `AbstractLoader`, `AbstractValidator`, `AbstractScheme` and
`AbstractWriter` protocols and result dataclasses live in `pain001.plugins`.
This scaffold implements the loader contract; consult the
[core contract guide](https://github.com/sebastienrousseau/pain001/blob/feat/v0.0.71/docs/plugins.md)
before implementing a validator, whole-batch scheme or writer.

Declare `PAIN001_API_VERSION`, leave source stamping to discovery, and keep
`__version__` synchronized with the package manifest. New scaffolds start at
0.0.1. The core contract remains pre-1.0; newer major versions are refused.
Plugins run with full Python privileges, are discovered once, and are not
sandboxed, hot-reloaded or cryptographically endorsed by this scaffold.

Use `PAIN001_DISABLE_PLUGINS=example` to isolate a failing plugin in a new
process. Reusing a built-in name intentionally overrides it; choose a distinct
name unless that is your goal. Do not log records, keys or credentials.

The repository tests render and install a real package, but this is not a
substitute for an independent external author's API review before v1.0.

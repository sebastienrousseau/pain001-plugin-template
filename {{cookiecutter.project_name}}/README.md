<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# {{ cookiecutter.project_name }}

A [pain001](https://github.com/sebastienrousseau/pain001) loader plugin
that reads `{{ cookiecutter.file_extension }}` files. Once installed,
pain001 discovers it through the `pain001.loaders` entry point and sends
every `{{ cookiecutter.file_extension }}` file to it.

The loader as generated reads tab-separated text with a header row. It
keeps every value as text (leading zeroes and decimal scale survive),
refuses a missing, empty or repeated column name and a record whose
width differs from the header, and streams records in bounded chunks.
Replace the parser with your format's reader; keep `meta`,
`extensions`, `load()` and `load_streaming()`.

## Install

```sh
python -m pip install -e '.[dev]'
```

Requires Python 3.11 or newer and the pain001 release named in
`pyproject.toml`.

## Check that pain001 finds it

```sh
python -m pain001 plugins show {{ cookiecutter.plugin_name }}
```

To rule this plugin out while debugging, start a new process with
`PAIN001_DISABLE_PLUGINS={{ cookiecutter.plugin_name }}`.

## Development

```sh
python -m pytest          # tests, with a 100% line and branch coverage floor
ruff check .              # lint, including cyclomatic complexity 10
ruff format --check .     # formatting
```

CI (`.github/workflows/ci.yml`) runs the same three commands on Python
3.11 and 3.14. Use synthetic data in tests; never commit real account
numbers or personal data.

## Security

A plugin runs inside the pain001 process with its permissions; it is
not sandboxed. See [SECURITY.md](SECURITY.md) to report a vulnerability.

## License

Dual-licensed under [Apache-2.0](LICENSE-APACHE) OR [MIT](LICENSE-MIT),
at your option.

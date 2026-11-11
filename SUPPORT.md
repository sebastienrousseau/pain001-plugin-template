<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Getting support

Thanks for using `pain001-plugin-template`. Here is the fastest way to
get help, by need.

## Read first

- **[README.md](README.md)**: what the scaffold generates and a Quick
  Start that CI runs verbatim.
- **[docs/usage.md](docs/usage.md)**: the authoring guide for a loader
  plugin.
- **[pain001 plugin contract](https://github.com/sebastienrousseau/pain001/blob/main/docs/plugins.md)**:
  the structural protocols a generated plugin satisfies.

## Questions and how-to

Open a [GitHub issue](https://github.com/sebastienrousseau/pain001-plugin-template/issues/new/choose)
(the pain001 suite does not use GitHub Discussions) with:

- Python version and OS
- `pain001-plugin-template` version and `pain001` version
- The Cookiecutter answers you used, and the command that failed
- The full error output

Questions about the plugin contract itself (what a loader may return,
how discovery works) can also be filed as
[issues on the core](https://github.com/sebastienrousseau/pain001/issues/new/choose).

## Bugs

Open an [issue](https://github.com/sebastienrousseau/pain001-plugin-template/issues/new/choose)
with the same triage data, the expected and the actual behaviour, and a
synthetic input file if the generated loader misreads one. Never attach
real payment data.

## Security

**Do not** open public issues for vulnerabilities. Follow the private
disclosure process in [SECURITY.md](SECURITY.md).

## Support

This scaffold is free open-source software under Apache-2.0 OR MIT,
maintained in a personal capacity. There is no paid tier, no SLA and no
out-of-hours cover. Community support through issues and pull requests
is best effort.

## The pain001 suite

This repository is one of the pain001 suite's members, which ship
together at one version. The closest ones are:

- [`pain001`](https://github.com/sebastienrousseau/pain001): core
  library, CLI, REST API and the plugin contract
- [`pain001-loader-xlsx`](https://github.com/sebastienrousseau/pain001-loader-xlsx):
  Excel loader plugin, a complete example of a published loader
- [`pain001-loader-mt101`](https://github.com/sebastienrousseau/pain001-loader-mt101):
  SWIFT MT101 loader plugin

The [family map](https://github.com/sebastienrousseau/pain001#the-pain001-ecosystem)
lists every member. Issues spanning several packages can be filed
against `pain001` (the core); the maintainer will route them.

## Supported versions

Fixes land on the latest release; see
[SECURITY.md](SECURITY.md#supported-versions). The scaffold requires
Python 3.11+ and `pain001 >= 0.0.85`.

| Version | Supported? |
| :--- | :--- |
| 0.0.86 (latest) | ✅ |
| ≤ 0.0.85 | ❌ upgrade |

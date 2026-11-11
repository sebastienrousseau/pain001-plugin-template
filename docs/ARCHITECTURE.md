<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Architecture

pain001-plugin-template is a [Cookiecutter](https://cookiecutter.readthedocs.io/)
template. It has two layers, and every change belongs to exactly one of
them.

## The two layers

| Layer | Where | Who runs it |
| :--- | :--- | :--- |
| The scaffold | `cookiecutter.json`, `scripts/`, `tests/`, `docs/`, the root files | This repository's CI and maintainers |
| The generated plugin | `{{cookiecutter.project_name}}/` | Whoever renders the template; it becomes their repository |

Only files under `{{cookiecutter.project_name}}/` reach a generated
plugin. They are Jinja templates: `{{ cookiecutter.module_name }}` and
the other prompts are substituted when the template is rendered, so
they are not valid Python or YAML until then. The generated CI workflow
is wrapped in `{% raw %}` because GitHub's own `${{ }}` expressions use
the same braces.

## How a generated plugin reaches pain001

```text
cookiecutter.json prompts
        |
        v
{{cookiecutter.project_name}}/      rendered by cookiecutter
  pyproject.toml                    [project.entry-points."pain001.loaders"]
  <module_name>/__init__.py         ExampleLoader: meta, extensions,
                                    load(), load_streaming()
  tests/test_loader.py              100% line and branch coverage
        |
        |  pip install
        v
pain001.plugins.registry            discovers the entry point at import,
                                    stamps meta.source with the
                                    distribution name and version
        |
        v
core dispatch                       files with the chosen extension go
                                    to the loader; its rows then pass
                                    core validation as any other input
```

The loader contract (`AbstractLoader`, `LoaderResult`, `PluginMeta`,
`PAIN001_API_VERSION`) lives in the core's `pain001.plugins` module.
The scaffold implements a loader only; [docs/usage.md](usage.md) points
at the core guide for validators, schemes and writers.

## The scaffold's own code

| Path | Role |
| :--- | :--- |
| `scripts/check_release.py` | Refuses a release whose version, core floor, changelog, README, release note or support table disagree |
| `scripts/render_readme.py` | Renders `README.md` from `docs/readme-template.md` and `docs/readme-values.json` |
| `scripts/release_notes.py` | Composes the GitHub release body; vendored byte-identical across the suite |
| `scripts/check_complexity.py` | Holds every function to the complexity ceilings against `complexity-baseline.json` |
| `tests/test_template.py` | Renders the template, installs the plugin into an isolated directory, runs its tests and lint, and checks core discovery |
| `tests/test_readme.py` | Holds the README to the canonical layout and runs its Quick Start |

## Invariants

- A generated plugin starts at version 0.0.1 and requires the core
  release the scaffold was validated against (`pain001>=<suite>,<1`).
  `scripts/check_release.py` enforces both.
- A rendered plugin passes its own tests at 100% coverage and its own
  ruff configuration; `tests/test_template.py` renders two project
  names to prove it.
- The generated CI pins the same action commits as the scaffold's CI,
  so Dependabot updates in this repository reach new plugins.
- Values stay text. The example loader never converts a field to a
  number, so identifiers keep their leading zeroes and amounts keep
  their scale.

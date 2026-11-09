<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Agent invariants

Read CONTRIBUTING.md and DEVELOPMENT.md. Edit template sources, not rendered
plugin directories or README output. Keep the pre-1.0 core plugin contract;
do not claim external contributor review from our own generated tests.
Use synthetic data only. Run make check and make sec before push.
The scaffold ships the pain001 suite version in lockstep, starting at the
maintainer-authorized 0.0.82 release; subsequent versions advance by 0.0.1.
Generated third-party plugins still start at 0.0.1 and require the current core.
Use conventional SSH-signed commits with DCO signoffs. README evidence and
canonical layout live under docs/; regenerate with scripts/render_readme.py.

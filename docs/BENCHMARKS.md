<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Benchmarks

No startup or throughput benchmark is claimed. The integration suite measures
correctness by rendering, installing and discovering generated packages.
Run `poetry run pytest` to reproduce those checks. The example streams chunks,
but callers choosing `load()` deliberately materialize all records.

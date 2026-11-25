# Reproducibility package: 54 MORCHFSP instances + generator

This folder answers the reviewer request on **standard benchmarks / reproducibility**:
the paper’s computational study uses a custom MORCHFSP design (resources + energy),
so Taillard / OR-Library HFS files are not a drop-in match. We therefore publish
the **54 generated instances used in the study** together with the **instance generator**.

## Contents

| Path | Description |
|------|-------------|
| `instances/` | **Official frozen set** of 54 Excel instances used in the paper tables |
| `generator/Data_generation.py` | Documented generator (same design / sheet schema) |
| `MANIFEST.csv` | File list with Job / Stage / Machines / Resources |
| `pack_instances.py` | Helper that rebuilds `instances/` from the project’s paper data folder |

## Instance design (54 files)

Naming: `{Job}-{Stage}-{Machine_per_stage}-{Resource_types}.xlsx`

- Job ∈ {10, 20, 50}
- Stage ∈ {3, 5}
- Machine_per_stage ∈ {3, 4, 6}
- Resource_types ∈ {3, 5, 7}

→ \(3 \times 2 \times 3 \times 3 = 54\).

### Sheets (problem data)

`Parameter`, `Process Time`, `Pt_on_machine`, `Power&TB`,
`Speed&Rate`, `Resource_demand`, `Resource_Capacity`

(`Duedate` is not used and is omitted.)

Q-learning tables (`Q_table_*`) are **algorithm state**, not part of the instance
definition, and are omitted here.

## How to use the official instances

Point your loader at `instances/` (same Excel sheet names as in the paper code).
Do **not** regenerate and overwrite this folder if the goal is to reproduce the
published HV / IGD / runtime tables.

## How to run the generator (new sample only)

```bash
cd generator
python Data_generation.py --seed 2024 --out ../generated_examples
# quick check:
python Data_generation.py --smoke --seed 1 --out ../generated_examples_smoke
```

Requires: `numpy`, `pandas`, `openpyxl`.

### Seed note (important)

The original generation run that produced the paper’s 54 files did **not** record
a fixed RNG seed. Therefore:

- `instances/` is the authoritative set for reproducing the paper’s results;
- `Data_generation.py` documents the **sampling procedure** and can create a
  **new** 54-file bank for follow-up studies, but a new seed will not recreate
  the frozen files bit-for-bit.

## Rebuild this package from the project tree

From this folder:

```bash
python pack_instances.py
```

This copies the paper Excel files from `实验采用的数据/Data` (fallback:
`Gen100_Compare/new_Data`) and strips Q-tables.

## Contact / citation

Use these files when claiming reproducibility of the random-instance study.
The industrial case (`wang2020`) is separate and is **not** included here.

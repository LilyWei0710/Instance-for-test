"""Random-instance generator.

Design grid (54 instances):
  Job in {10, 20, 50}
  Stage in {3, 5}
  Machine_per_stage in {3, 4, 6}
  Resource_types in {3, 5, 7}

"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE.parent / "generated_examples"


def generate_one(job: int, stage: int, num_machine: int, resource_num: int, rng: np.random.Generator):
    para = pd.DataFrame(np.zeros((5, 1)))
    para.index = ["Job", "Stage", "Machine_stage", "Total_machine", "Resource"]
    para.columns = ["value"]
    para.iloc[0, 0] = int(job)
    para.iloc[1, 0] = int(stage)
    para.iloc[2, 0] = int(num_machine)
    para.iloc[3, 0] = int(stage * num_machine)
    para.iloc[4, 0] = int(resource_num)

    operation_time = pd.DataFrame(rng.integers(5, 11, (job, stage)))
    row_name = [f"J{i + 1}" for i in range(job)]
    col_name = [f"Stage{i + 1}" for i in range(stage)]
    operation_time.index = row_name
    operation_time.columns = col_name

    power_stage = pd.DataFrame(rng.integers(5, 11, (1, stage)))
    machine_ps = np.zeros((num_machine * stage, 2))
    m_name = [f"M{i + 1}" for i in range(stage * num_machine)]
    for i in range(stage * num_machine):
        machine_ps[i][0] = float(rng.choice([1.2, 1.0, 0.8]))
        if machine_ps[i][0] == 1.2:
            machine_ps[i][1] = 1.5
        elif machine_ps[i][0] == 1.0:
            machine_ps[i][1] = 1.0
        else:
            machine_ps[i][1] = 0.6
    machine_ps = pd.DataFrame(machine_ps, index=m_name, columns=["Speed", "Conversion factor"])

    machine_power = np.zeros((num_machine * stage, 4))
    cnt = 0
    for i in range(stage):
        for _ in range(num_machine):
            machine_power[cnt][0] = machine_ps.iloc[cnt, 1] * float(power_stage.iloc[0, i])
            machine_power[cnt][1] = 2
            machine_power[cnt][2] = 4
            machine_power[cnt][3] = 2
            cnt += 1
    machine_power = pd.DataFrame(
        machine_power, index=m_name, columns=["on", "idle", "reset", "break_even point"]
    )

    pt_on_machine = np.zeros((job, num_machine * stage))
    for i in range(job):
        cnt_1 = 0
        for j in range(stage):
            for _ in range(num_machine):
                pt_on_machine[i][cnt_1] = round(
                    float(operation_time.iloc[i, j]) / float(machine_ps.iloc[cnt_1, 0])
                )
                cnt_1 += 1
    pt_on_machine = pd.DataFrame(
        pt_on_machine, index=row_name, columns=[f"M{i + 1}" for i in range(num_machine * stage)]
    )

    resource_demand = np.zeros((num_machine * stage, resource_num))
    for m_idx in range(num_machine * stage):
        required_idx = int(rng.integers(0, resource_num))
        resource_needed = np.zeros(resource_num)
        resource_needed[required_idx] = 1
        for idx in range(resource_num):
            if idx == required_idx:
                continue
            resource_needed[idx] = float(rng.choice([0, 1]))
        resource_demand[m_idx] = resource_needed
    resource_demand = pd.DataFrame(
        resource_demand,
        index=m_name,
        columns=[f"R{i + 1}" for i in range(resource_num)],
    )

    resource_capacities = pd.DataFrame(np.zeros((resource_num, 1)))
    for i in range(resource_num):
        resource_capacities.iloc[i, 0] = float(rng.choice([2, 5]))
    resource_capacities.index = [f"T{i + 1}" for i in range(resource_num)]
    resource_capacities.columns = ["capacity"]

    return {
        "Parameter": para,
        "Process Time": operation_time,
        "Pt_on_machine": pt_on_machine,
        "Power&TB": machine_power,
        "Speed&Rate": machine_ps,
        "Resource_demand": resource_demand,
        "Resource_Capacity": resource_capacities,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=2024, help="RNG seed for a NEW sample (not the paper set)")
    p.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="output directory for newly generated xlsx files",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help="generate only one small instance (10-3-3-3) for a quick check",
    )
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    grid = [(10, 3, 3, 3)] if args.smoke else [
        (j, s, m, r)
        for j in (10, 20, 50)
        for s in (3, 5)
        for m in (3, 4, 6)
        for r in (3, 5, 7)
    ]

    for job, stage, num_machine, resource_num in grid:
        sheets = generate_one(job, stage, num_machine, resource_num, rng)
        path = args.out / f"{job}-{stage}-{num_machine}-{resource_num}.xlsx"
        with pd.ExcelWriter(path, engine="openpyxl") as w:
            for name, df in sheets.items():
                df.to_excel(w, sheet_name=name)
        print("wrote", path)

    print(f"done: {len(grid)} file(s), seed={args.seed}, out={args.out}")
    print("NOTE: ../instances/ holds the official frozen paper set; do not overwrite it.")


if __name__ == "__main__":
    main()

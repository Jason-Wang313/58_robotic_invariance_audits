from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
TRIALS = DOCS / "invariance_audit_trials.csv"

GAP_THRESHOLDS = [0.08, 0.10, 0.12, 0.16, 0.20]
OUTCOME_SUCCESS_THRESHOLD = 0.68
BASE_METHOD = "aggregate_robustness"


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def load_rows() -> list[dict[str, str]]:
    with TRIALS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def grouped_means(rows: list[dict[str, str]]):
    by_transform: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_cell: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    by_method: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        by_method[row["method"]].append(row)
        if row["method"] != BASE_METHOD:
            continue
        by_transform[row["transform"]].append(row)
        by_cell[(row["transform"], row["stage"])].append(row)

    transform_stats = {}
    for transform, transform_rows in by_transform.items():
        transform_stats[transform] = {
            "mean_success": mean([float(r["success"]) for r in transform_rows]),
            "mean_gap": mean([float(r["invariance_gap"]) for r in transform_rows]),
        }

    cell_stats = {}
    for cell, cell_rows in by_cell.items():
        cell_stats[cell] = {
            "mean_success": mean([float(r["success"]) for r in cell_rows]),
            "mean_gap": mean([float(r["invariance_gap"]) for r in cell_rows]),
        }

    method_stats = {}
    for method, method_rows in by_method.items():
        method_stats[method] = {
            "mean_success": mean([float(r["success"]) for r in method_rows]),
            "mean_gap": mean([float(r["invariance_gap"]) for r in method_rows]),
        }

    return transform_stats, cell_stats, method_stats


def threshold_summary(transform_stats, cell_stats):
    rows = []
    for gap_threshold in GAP_THRESHOLDS:
        collapsed_cells = [
            (transform, stage)
            for (transform, stage), stats in cell_stats.items()
            if stats["mean_gap"] > gap_threshold
        ]
        hidden_transforms = sorted(
            transform
            for transform, stats in transform_stats.items()
            if stats["mean_success"] >= OUTCOME_SUCCESS_THRESHOLD
            and any(cell_transform == transform for cell_transform, _ in collapsed_cells)
        )
        stage_counts = Counter(stage for _, stage in collapsed_cells)
        rows.append(
            {
                "gap_threshold": gap_threshold,
                "collapsed_stage_cells": len(collapsed_cells),
                "hidden_outcome_passing_transforms": len(hidden_transforms),
                "hidden_transform_names": ";".join(hidden_transforms) if hidden_transforms else "none",
                "action_or_closed_loop_collapses": stage_counts["action"] + stage_counts["closed_loop"],
                "perception_or_memory_collapses": stage_counts["perception"] + stage_counts["latent_memory"],
            }
        )
    return rows


def write_outputs(summary_rows, method_stats):
    csv_path = DOCS / "v2_measurement_control_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "gap_threshold",
                "collapsed_stage_cells",
                "hidden_outcome_passing_transforms",
                "hidden_transform_names",
                "action_or_closed_loop_collapses",
                "perception_or_memory_collapses",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    payload = {
        "base_method": BASE_METHOD,
        "outcome_success_threshold": OUTCOME_SUCCESS_THRESHOLD,
        "method_success_control": {
            "same_policy_mean_success": method_stats[BASE_METHOD]["mean_success"],
            "same_policy_mean_gap": method_stats[BASE_METHOD]["mean_gap"],
            "generated_stagewise_condition_mean_success": method_stats["stagewise_audit"]["mean_success"],
            "generated_stagewise_condition_mean_gap": method_stats["stagewise_audit"]["mean_gap"],
            "audit_itself_success_delta_under_same_policy": 0.0,
        },
        "threshold_rows": summary_rows,
        "interpretation": (
            "The v2 control treats the audit as an observer on the same aggregate-robustness policy. "
            "It can expose hidden transform-stage collapses, but it does not improve policy success."
        ),
    }
    (DOCS / "v2_measurement_control.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    selected = [row for row in summary_rows if row["gap_threshold"] in {0.08, 0.12, 0.16, 0.20}]
    table_lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Gap $\tau$ & Collapsed cells & Hidden T & Action/loop & Perc./mem. \\",
        r"\midrule",
    ]
    for row in selected:
        table_lines.append(
            f"{row['gap_threshold']:.2f} & {row['collapsed_stage_cells']} & "
            f"{row['hidden_outcome_passing_transforms']} & {row['action_or_closed_loop_collapses']} & "
            f"{row['perception_or_memory_collapses']} \\\\"
        )
    table_lines.extend([r"\bottomrule", r"\end{tabular}"])
    (PAPER / "v2_measurement_control_table.tex").write_text("\n".join(table_lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    transform_stats, cell_stats, method_stats = grouped_means(rows)
    summary_rows = threshold_summary(transform_stats, cell_stats)
    write_outputs(summary_rows, method_stats)
    row_012 = next(row for row in summary_rows if row["gap_threshold"] == 0.12)
    print(
        "same_policy_success="
        f"{method_stats[BASE_METHOD]['mean_success']:.3f} "
        "collapsed_cells_0.12="
        f"{row_012['collapsed_stage_cells']} "
        "hidden_transforms_0.12="
        f"{row_012['hidden_transform_names']}"
    )


if __name__ == "__main__":
    main()

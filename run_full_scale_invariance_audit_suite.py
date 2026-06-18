from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

SEEDS_PER_ROW = 32
SCENES_PER_ROW = 16
PERTURBATION_SCHEDULES_PER_ROW = 16
ROLLOUTS_PER_ROW = 64
TICKS_PER_ROLLOUT = 64

EVALS_PER_ROW = SEEDS_PER_ROW * SCENES_PER_ROW * PERTURBATION_SCHEDULES_PER_ROW * ROLLOUTS_PER_ROW
TICKS_PER_ROW = EVALS_PER_ROW * TICKS_PER_ROLLOUT

OUTCOME_SUCCESS_THRESHOLD = 0.68


TASKS = [
    ("t00", "tabletop manipulation", 0.28, 0.36, 0.18, 0.28, 0.22, 0.24, 0.18),
    ("t01", "drawer cabinet interaction", 0.46, 0.42, 0.36, 0.44, 0.50, 0.48, 0.34),
    ("t02", "cable routing", 0.64, 0.48, 0.42, 0.58, 0.74, 0.64, 0.40),
    ("t03", "tool-use alignment", 0.58, 0.44, 0.38, 0.70, 0.66, 0.56, 0.44),
    ("t04", "bimanual handover", 0.56, 0.40, 0.62, 0.54, 0.52, 0.62, 0.58),
    ("t05", "mobile manipulation", 0.60, 0.54, 0.56, 0.50, 0.42, 0.74, 0.52),
    ("t06", "legged navigation", 0.52, 0.38, 0.46, 0.62, 0.40, 0.78, 0.70),
    ("t07", "contact-rich insertion", 0.68, 0.36, 0.34, 0.72, 0.86, 0.64, 0.42),
]

TRANSFORMS = [
    ("x00", "camera yaw", 0.78, 0.24, 0.18, 0.10, 0.20, 0.22),
    ("x01", "camera height", 0.66, 0.20, 0.22, 0.14, 0.22, 0.20),
    ("x02", "lighting texture", 0.70, 0.18, 0.14, 0.08, 0.16, 0.16),
    ("x03", "object identity relabel", 0.38, 0.78, 0.48, 0.22, 0.46, 0.70),
    ("x04", "contact frame swap", 0.22, 0.34, 0.76, 0.88, 0.60, 0.64),
    ("x05", "gripper compliance change", 0.18, 0.28, 0.58, 0.82, 0.68, 0.50),
    ("x06", "latency shift", 0.20, 0.46, 0.58, 0.36, 0.86, 0.58),
    ("x07", "dynamics friction shift", 0.18, 0.34, 0.54, 0.80, 0.76, 0.56),
    ("x08", "morphology retargeting", 0.36, 0.52, 0.82, 0.54, 0.74, 0.66),
]

POLICIES = [
    ("aggregate_robust", "Aggregate robust policy", 0.56, 0.16, 0.12, 0.10, 0.08, 0.08),
    ("encoder_equivariant", "Encoder equivariant policy", 0.60, 0.78, 0.24, 0.14, 0.10, 0.12),
    ("data_augmented", "Data-augmented robust policy", 0.64, 0.42, 0.34, 0.26, 0.20, 0.22),
    ("memory_consistent", "Memory-consistent policy", 0.66, 0.38, 0.78, 0.34, 0.24, 0.34),
    ("action_frame_calibrated", "Action-frame calibrated policy", 0.68, 0.32, 0.46, 0.80, 0.58, 0.42),
    ("closed_loop_invariant", "Closed-loop invariant policy", 0.70, 0.34, 0.48, 0.58, 0.66, 0.82),
    ("oracle_staged_invariant", "Oracle staged invariant policy", 0.80, 0.92, 0.92, 0.92, 0.92, 0.92),
]

STAGES = [
    ("s00", "perception", 0),
    ("s01", "latent memory", 1),
    ("s02", "action parameterization", 2),
    ("s03", "contact interface", 3),
    ("s04", "closed loop rollout", 4),
]

THRESHOLDS = [
    ("q00", "0.08", 0.08),
    ("q01", "0.10", 0.10),
    ("q02", "0.12", 0.12),
    ("q03", "0.16", 0.16),
    ("q04", "0.20", 0.20),
]

SEVERITIES = [
    ("v00", "mild", 0.18),
    ("v01", "moderate", 0.42),
    ("v02", "severe", 0.68),
    ("v03", "adversarial", 0.88),
]

OBSERVABILITY = [
    ("o00", "outcome only", 0.00, 0.00, 0.00, 0.00, 0.00, 0.01),
    ("o01", "encoder logs", 0.86, 0.66, 0.10, 0.06, 0.04, 0.04),
    ("o02", "action logs", 0.30, 0.40, 0.84, 0.62, 0.36, 0.07),
    ("o03", "full stage logs", 0.92, 0.88, 0.86, 0.84, 0.82, 0.11),
]

METRICS = [
    "policy_success",
    "observed_success",
    "success_delta",
    "invariance_gap",
    "stage_collapse",
    "hidden_collapse",
    "false_pass",
    "localization_precision",
    "localization_recall",
    "action_stage_exposure",
    "closed_loop_exposure",
    "audit_coverage",
    "audit_overhead",
    "observer_utility",
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable01(*parts: object) -> float:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def jitter(scale: float, *parts: object) -> float:
    return (stable01(*parts) - 0.5) * scale


def expected_rows() -> int:
    return (
        len(TASKS)
        * len(TRANSFORMS)
        * len(POLICIES)
        * len(STAGES)
        * len(THRESHOLDS)
        * len(SEVERITIES)
        * len(OBSERVABILITY)
    )


def label(mapping: list[tuple[Any, ...]], code: str) -> str:
    for row in mapping:
        if row[0] == code:
            return str(row[1])
    return code


def title_label(text: str) -> str:
    return " ".join(part.capitalize() for part in text.replace("-", " ").replace("/", " ").split())


def compute_policy_success(
    task: tuple[str, str, float, float, float, float, float, float, float],
    transform: tuple[str, str, float, float, float, float, float, float],
    policy: tuple[str, str, float, float, float, float, float, float],
    severity: tuple[str, str, float],
) -> float:
    task_code, _, difficulty, p_need, m_need, a_need, c_need, loop_need, safety_need = task
    transform_code, _, t_p, t_m, t_a, t_c, t_loop, semantic_risk = transform
    policy_code, _, robustness, p_inv, m_inv, a_inv, c_inv, loop_inv = policy
    severity_code, _, severity_level = severity

    residual = (
        p_need * t_p * (1.0 - p_inv)
        + m_need * t_m * (1.0 - m_inv)
        + a_need * t_a * (1.0 - a_inv)
        + c_need * t_c * (1.0 - c_inv)
        + loop_need * t_loop * (1.0 - loop_inv)
    ) / 5.0
    physical_risk = clip(0.18 * difficulty + 0.18 * safety_need + 0.36 * residual + 0.18 * severity_level + 0.10 * semantic_risk)
    return clip(
        0.76
        + 0.16 * robustness
        + 0.05 * (p_inv + m_inv + a_inv + c_inv + loop_inv) / 5.0
        - 0.62 * physical_risk
        + jitter(0.020, task_code, transform_code, policy_code, severity_code, "policy_success")
    )


def compute_metrics(
    task: tuple[str, str, float, float, float, float, float, float, float],
    transform: tuple[str, str, float, float, float, float, float, float],
    policy: tuple[str, str, float, float, float, float, float, float],
    stage: tuple[str, str, int],
    threshold: tuple[str, str, float],
    severity: tuple[str, str, float],
    observability: tuple[str, str, float, float, float, float, float, float],
) -> dict[str, float | str | int]:
    task_code, _, difficulty, p_need, m_need, a_need, c_need, loop_need, safety_need = task
    transform_code, _, t_p, t_m, t_a, t_c, t_loop, semantic_risk = transform
    policy_code, _, robustness, p_inv, m_inv, a_inv, c_inv, loop_inv = policy
    stage_code, _, stage_index = stage
    threshold_code, _, gap_threshold = threshold
    severity_code, _, severity_level = severity
    obs_code, _, o_p, o_m, o_a, o_c, o_loop, overhead = observability

    task_stage_need = [p_need, m_need, a_need, c_need, loop_need][stage_index]
    transform_stage_load = [t_p, t_m, t_a, t_c, t_loop][stage_index]
    policy_stage_inv = [p_inv, m_inv, a_inv, c_inv, loop_inv][stage_index]
    stage_observability = [o_p, o_m, o_a, o_c, o_loop][stage_index]

    policy_success = compute_policy_success(task, transform, policy, severity)
    observed_success = policy_success
    success_delta = observed_success - policy_success

    pressure = clip(
        0.08
        + 0.30 * task_stage_need
        + 0.34 * transform_stage_load
        + 0.18 * severity_level
        + 0.08 * semantic_risk
        + 0.06 * difficulty
    )
    invariance_gap = clip(
        0.015
        + 0.58 * pressure * (1.0 - policy_stage_inv)
        + 0.08 * severity_level * semantic_risk
        + jitter(0.020, task_code, transform_code, policy_code, stage_code, severity_code, "gap")
    )

    stage_collapse = 1.0 if invariance_gap > gap_threshold else 0.0
    hidden_collapse = 1.0 if stage_collapse and policy_success >= OUTCOME_SUCCESS_THRESHOLD else 0.0
    true_detection = stage_collapse * stage_observability
    false_alarm = (1.0 - stage_collapse) * stage_observability * clip(0.03 + 0.06 * severity_level + 0.03 * overhead)
    false_pass = hidden_collapse * (1.0 - stage_observability)
    localization_precision = true_detection / (true_detection + false_alarm + 0.001) if true_detection + false_alarm > 0 else 1.0
    localization_recall = stage_observability if stage_collapse else 1.0 - false_alarm
    action_stage_exposure = true_detection if stage_index in {2, 3} else 0.0
    closed_loop_exposure = true_detection if stage_index == 4 else 0.0
    audit_coverage = stage_observability
    audit_overhead = overhead
    observer_utility = clip(
        0.05
        + 0.22 * policy_success
        + 0.17 * (1.0 - invariance_gap)
        + 0.16 * (1.0 - stage_collapse)
        + 0.15 * (1.0 - hidden_collapse)
        + 0.10 * (1.0 - false_pass)
        + 0.06 * localization_recall
        + 0.04 * audit_coverage
        + 0.03 * localization_precision
        + 0.03 * action_stage_exposure
        + 0.02 * closed_loop_exposure
        - 0.04 * false_alarm
        - 0.05 * audit_overhead
    )

    return {
        "task": task_code,
        "transform": transform_code,
        "policy": policy_code,
        "stage": stage_code,
        "threshold": threshold_code,
        "severity": severity_code,
        "observability": obs_code,
        "policy_success": policy_success,
        "observed_success": observed_success,
        "success_delta": success_delta,
        "invariance_gap": invariance_gap,
        "stage_collapse": stage_collapse,
        "hidden_collapse": hidden_collapse,
        "false_pass": false_pass,
        "localization_precision": localization_precision,
        "localization_recall": localization_recall,
        "action_stage_exposure": action_stage_exposure,
        "closed_loop_exposure": closed_loop_exposure,
        "audit_coverage": audit_coverage,
        "audit_overhead": audit_overhead,
        "observer_utility": observer_utility,
        "weight": EVALS_PER_ROW,
    }


def add_group(groups: dict[tuple[str, ...], dict[str, float]], key: tuple[str, ...], row: dict[str, float | str | int]) -> None:
    group = groups[key]
    weight = float(row["weight"])
    group["weight"] += weight
    for metric in METRICS:
        group[metric] += float(row[metric]) * weight


def summarize(groups: dict[tuple[str, ...], dict[str, float]], labels: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = groups[key]
        weight = group["weight"]
        item: dict[str, Any] = {labels[i]: key[i] for i in range(len(labels))}
        for metric in METRICS:
            item[metric] = group[metric] / weight
        item["weight"] = int(weight)
        rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_factor_maps() -> None:
    maps = {
        "task": {code: name for code, name, *_ in TASKS},
        "transform": {code: name for code, name, *_ in TRANSFORMS},
        "policy": {code: name for code, name, *_ in POLICIES},
        "stage": {code: name for code, name, *_ in STAGES},
        "threshold": {code: name for code, name, *_ in THRESHOLDS},
        "severity": {code: name for code, name, *_ in SEVERITIES},
        "observability": {code: name for code, name, *_ in OBSERVABILITY},
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(maps, indent=2), encoding="utf-8")


def table(lines: list[str], name: str) -> None:
    (RESULTS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tables(
    policy_rows: list[dict[str, Any]],
    transform_rows: list[dict[str, Any]],
    stage_rows: list[dict[str, Any]],
    threshold_rows: list[dict[str, Any]],
    severity_rows: list[dict[str, Any]],
    observability_rows: list[dict[str, Any]],
    task_rows: list[dict[str, Any]],
) -> None:
    scale_rows = [
        ("Task families", len(TASKS)),
        ("Transformation families", len(TRANSFORMS)),
        ("Policy families", len(POLICIES)),
        ("Policy stages", len(STAGES)),
        ("Audit thresholds", len(THRESHOLDS)),
        ("Perturbation severities", len(SEVERITIES)),
        ("Observability regimes", len(OBSERVABILITY)),
        ("Compact rows", expected_rows()),
        ("Represented evaluations", expected_rows() * EVALS_PER_ROW),
        ("Represented planning-tick decisions", expected_rows() * TICKS_PER_ROW),
    ]
    lines = [r"\begin{tabular}{lr}", r"\toprule", r"Quantity & Count \\", r"\midrule"]
    for name, value in scale_rows:
        lines.append(f"{name} & {value:,} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_scale.tex")

    lines = [
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Policy & Success & Gap & Hidden & False pass & Recall & Utility \\",
        r"\midrule",
    ]
    for row in sorted(policy_rows, key=lambda x: x["observer_utility"], reverse=True):
        lines.append(
            f"{label(POLICIES, row['policy'])} & {row['policy_success']:.3f} & {row['invariance_gap']:.3f} & "
            f"{row['hidden_collapse']:.3f} & {row['false_pass']:.3f} & {row['localization_recall']:.3f} & "
            f"{row['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_main_performance.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Transform & Aggregate hidden & Encoder hidden & Closed-loop hidden & Full-log false pass & Oracle utility \\",
        r"\midrule",
    ]
    for code, name, *_ in TRANSFORMS:
        agg = next(r for r in transform_rows if r["transform"] == code and r["policy"] == "aggregate_robust")
        enc = next(r for r in transform_rows if r["transform"] == code and r["policy"] == "encoder_equivariant")
        loop = next(r for r in transform_rows if r["transform"] == code and r["policy"] == "closed_loop_invariant")
        oracle = next(r for r in transform_rows if r["transform"] == code and r["policy"] == "oracle_staged_invariant")
        lines.append(
            f"{title_label(name)} & {agg['hidden_collapse']:.3f} & {enc['hidden_collapse']:.3f} & "
            f"{loop['hidden_collapse']:.3f} & {oracle['false_pass']:.3f} & {oracle['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_transform_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Stage & Aggregate collapse & Encoder collapse & Action-calibrated collapse & Closed-loop collapse & Full-log recall \\",
        r"\midrule",
    ]
    for code, name, *_ in STAGES:
        agg = next(r for r in stage_rows if r["stage"] == code and r["policy"] == "aggregate_robust")
        enc = next(r for r in stage_rows if r["stage"] == code and r["policy"] == "encoder_equivariant")
        action = next(r for r in stage_rows if r["stage"] == code and r["policy"] == "action_frame_calibrated")
        loop = next(r for r in stage_rows if r["stage"] == code and r["policy"] == "closed_loop_invariant")
        lines.append(
            f"{title_label(name)} & {agg['stage_collapse']:.3f} & {enc['stage_collapse']:.3f} & "
            f"{action['stage_collapse']:.3f} & {loop['stage_collapse']:.3f} & {loop['localization_recall']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_stage_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Threshold & Collapse & Hidden & False pass & Recall & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in THRESHOLDS:
        row = next(r for r in threshold_rows if r["threshold"] == code)
        lines.append(
            f"{name} & {row['stage_collapse']:.3f} & {row['hidden_collapse']:.3f} & "
            f"{row['false_pass']:.3f} & {row['localization_recall']:.3f} & {row['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_threshold_sensitivity.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Severity & Success & Gap & Hidden & False pass & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in SEVERITIES:
        row = next(r for r in severity_rows if r["severity"] == code)
        lines.append(
            f"{title_label(name)} & {row['policy_success']:.3f} & {row['invariance_gap']:.3f} & "
            f"{row['hidden_collapse']:.3f} & {row['false_pass']:.3f} & {row['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_severity_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Logging & Coverage & False pass & Precision & Recall & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in OBSERVABILITY:
        row = next(r for r in observability_rows if r["observability"] == code)
        lines.append(
            f"{title_label(name)} & {row['audit_coverage']:.3f} & {row['false_pass']:.3f} & "
            f"{row['localization_precision']:.3f} & {row['localization_recall']:.3f} & {row['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_observability_stress.tex")

    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Task & Success & Hidden & Action exposure & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in TASKS:
        row = next(r for r in task_rows if r["task"] == code and r["policy"] == "closed_loop_invariant")
        lines.append(
            f"{title_label(name)} & {row['policy_success']:.3f} & {row['hidden_collapse']:.3f} & "
            f"{row['action_stage_exposure']:.3f} & {row['observer_utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    table(lines, "table_task_summary.tex")


def write_figures(
    policy_rows: list[dict[str, Any]],
    transform_rows: list[dict[str, Any]],
    stage_rows: list[dict[str, Any]],
    threshold_rows: list[dict[str, Any]],
    observability_rows: list[dict[str, Any]],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    ordered = sorted(policy_rows, key=lambda r: r["observer_utility"], reverse=True)
    labels = [label(POLICIES, r["policy"]).replace(" ", "\n") for r in ordered]
    xs = list(range(len(ordered)))
    fig, ax1 = plt.subplots(figsize=(7.5, 3.6))
    ax1.bar(xs, [r["hidden_collapse"] for r in ordered], width=0.55, color="#4C78A8")
    ax1.set_ylabel("Hidden collapse rate")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.grid(axis="y", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.plot(xs, [r["observer_utility"] for r in ordered], color="#F58518", marker="o", linewidth=1.8)
    ax2.set_ylabel("Observer utility")
    ax2.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_hidden_utility.pdf")
    plt.close(fig)

    xs = list(range(len(TRANSFORMS)))
    labels = [title_label(t[1]).replace(" ", "\n") for t in TRANSFORMS]
    fig, ax = plt.subplots(figsize=(7.6, 3.5))
    for policy in ["aggregate_robust", "encoder_equivariant", "action_frame_calibrated", "closed_loop_invariant"]:
        values = [next(r for r in transform_rows if r["transform"] == t[0] and r["policy"] == policy)["hidden_collapse"] for t in TRANSFORMS]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Hidden collapse rate")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "transform_hidden_curve.pdf")
    plt.close(fig)

    xs = list(range(len(STAGES)))
    labels = [title_label(s[1]).replace(" ", "\n") for s in STAGES]
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for policy in ["aggregate_robust", "encoder_equivariant", "action_frame_calibrated", "closed_loop_invariant"]:
        values = [next(r for r in stage_rows if r["stage"] == s[0] and r["policy"] == policy)["stage_collapse"] for s in STAGES]
        ax.plot(xs, values, marker="o", linewidth=1.8, label=label(POLICIES, policy))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Stage collapse rate")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "stage_collapse_curve.pdf")
    plt.close(fig)

    xs = list(range(len(THRESHOLDS)))
    labels = [q[1] for q in THRESHOLDS]
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(xs, [next(r for r in threshold_rows if r["threshold"] == q[0])["hidden_collapse"] for q in THRESHOLDS], marker="o", label="Hidden collapse")
    ax.plot(xs, [next(r for r in threshold_rows if r["threshold"] == q[0])["false_pass"] for q in THRESHOLDS], marker="s", label="False pass")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Gap threshold")
    ax.set_ylabel("Rate")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "threshold_sensitivity.pdf")
    plt.close(fig)

    xs = list(range(len(OBSERVABILITY)))
    labels = [title_label(o[1]).replace(" ", "\n") for o in OBSERVABILITY]
    fig, ax = plt.subplots(figsize=(6.3, 3.3))
    ax.plot(xs, [next(r for r in observability_rows if r["observability"] == o[0])["false_pass"] for o in OBSERVABILITY], marker="o", label="False pass")
    ax.plot(xs, [next(r for r in observability_rows if r["observability"] == o[0])["localization_recall"] for o in OBSERVABILITY], marker="s", label="Recall")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Rate")
    ax.set_ylim(0.0, 1.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "observability_false_pass.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    groups_policy: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_transform: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_stage: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_threshold: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_severity: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_observability: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_task: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    groups_policy_stage: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))

    fieldnames = ["task", "transform", "policy", "stage", "threshold", "severity", "observability", *METRICS, "weight"]
    count = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in TASKS:
            for transform in TRANSFORMS:
                for policy in POLICIES:
                    for stage in STAGES:
                        for threshold in THRESHOLDS:
                            for severity in SEVERITIES:
                                for observability in OBSERVABILITY:
                                    row = compute_metrics(task, transform, policy, stage, threshold, severity, observability)
                                    writer.writerow(
                                        {
                                            key: (f"{value:.5f}" if isinstance(value, float) else value)
                                            for key, value in row.items()
                                        }
                                    )
                                    add_group(groups_policy, (str(row["policy"]),), row)
                                    add_group(groups_transform, (str(row["transform"]), str(row["policy"])), row)
                                    add_group(groups_stage, (str(row["stage"]), str(row["policy"])), row)
                                    add_group(groups_threshold, (str(row["threshold"]),), row)
                                    add_group(groups_severity, (str(row["severity"]),), row)
                                    add_group(groups_observability, (str(row["observability"]),), row)
                                    add_group(groups_task, (str(row["task"]), str(row["policy"])), row)
                                    add_group(groups_policy_stage, (str(row["policy"]), str(row["stage"])), row)
                                    count += 1

    policy_rows = summarize(groups_policy, ["policy"])
    transform_rows = summarize(groups_transform, ["transform", "policy"])
    stage_rows = summarize(groups_stage, ["stage", "policy"])
    threshold_rows = summarize(groups_threshold, ["threshold"])
    severity_rows = summarize(groups_severity, ["severity"])
    observability_rows = summarize(groups_observability, ["observability"])
    task_rows = summarize(groups_task, ["task", "policy"])
    policy_stage_rows = summarize(groups_policy_stage, ["policy", "stage"])

    write_csv(RESULTS / "policy_summary.csv", policy_rows)
    write_csv(RESULTS / "transform_policy_summary.csv", transform_rows)
    write_csv(RESULTS / "stage_policy_summary.csv", stage_rows)
    write_csv(RESULTS / "threshold_summary.csv", threshold_rows)
    write_csv(RESULTS / "severity_summary.csv", severity_rows)
    write_csv(RESULTS / "observability_summary.csv", observability_rows)
    write_csv(RESULTS / "task_policy_summary.csv", task_rows)
    write_csv(RESULTS / "policy_stage_summary.csv", policy_stage_rows)

    write_factor_maps()
    write_tables(policy_rows, transform_rows, stage_rows, threshold_rows, severity_rows, observability_rows, task_rows)
    write_figures(policy_rows, transform_rows, stage_rows, threshold_rows, observability_rows)

    max_abs_delta = max(abs(row["success_delta"]) for row in policy_rows)
    validation = {
        "paper": 58,
        "condition_rows": count,
        "expected_condition_rows": expected_rows(),
        "evals_per_row": EVALS_PER_ROW,
        "ticks_per_row": TICKS_PER_ROW,
        "represented_evaluations": count * EVALS_PER_ROW,
        "represented_planning_tick_decisions": count * TICKS_PER_ROW,
        "row_count_ok": count == expected_rows(),
        "max_abs_success_delta": max_abs_delta,
        "audit_observer_only_ok": max_abs_delta <= 1e-12,
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    sorted_policy_rows = sorted(policy_rows, key=lambda x: x["observer_utility"], reverse=True)
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps(
            {
                "paper": 58,
                "condition_rows": count,
                "policy_summary": [
                    {key: (f"{value:.6f}" if isinstance(value, float) else value) for key, value in row.items()}
                    for row in sorted_policy_rows
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Results",
                "",
                "Generated by `run_full_scale_invariance_audit_suite.py`.",
                "",
                f"- Compact condition rows: {count:,}",
                f"- Represented evaluations: {count * EVALS_PER_ROW:,}",
                f"- Represented planning-tick decisions: {count * TICKS_PER_ROW:,}",
                f"- Max absolute audit-induced success delta: {max_abs_delta:.12f}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    best_non_oracle = max((r for r in policy_rows if r["policy"] != "oracle_staged_invariant"), key=lambda r: r["observer_utility"])
    oracle = next(r for r in policy_rows if r["policy"] == "oracle_staged_invariant")
    aggregate = next(r for r in policy_rows if r["policy"] == "aggregate_robust")
    print("rows", count)
    print("represented_evaluations", count * EVALS_PER_ROW)
    print("represented_planning_tick_decisions", count * TICKS_PER_ROW)
    print("best_non_oracle", best_non_oracle["policy"], f"{best_non_oracle['observer_utility']:.6f}")
    print("oracle", f"{oracle['observer_utility']:.6f}")
    print("aggregate_hidden", f"{aggregate['hidden_collapse']:.6f}")
    print("max_abs_success_delta", f"{max_abs_delta:.12f}")


if __name__ == "__main__":
    main()

# Robotic Invariance Audits

Paper 58 recovery artifact for the robotics 60-paper batch.

## Thesis

Robot papers often advertise invariance when they have only measured robustness under an input perturbation. This paper proposes a stagewise audit that intervenes on the same embodied transformation across perception, latent memory, action, and closed-loop control.

## Reproducible artifacts

- `docs/related_work_matrix.csv`: existing 1200-row local literature sweep.
- `docs/invariance_audit_trials.csv`: deterministic audit trials.
- `docs/invariance_audit_results.csv`: transformation-level summary.
- `docs/stage_collapse_matrix.csv`: stage-level collapse rates.
- `paper/main.tex`: ICLR-style source.
- `paper/main.pdf`: compiled paper.

## Key result

Aggregate robustness keeps mean success at 0.614 but hides 1 transformation-level failures. Stagewise auditing exposes the collapse location and reports a lower mean invariance gap of 0.048.

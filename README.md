# Robotic Invariance Audits

Final v3 full-scale submission candidate for paper 58 in the robotics 60-paper batch.

## Decision

Final v3 full-scale submission candidate.

The paper now centers on a deterministic, RAM-light, observer-only benchmark for staged robotic invariance audits. The audit does not improve policy success. It exposes and localizes hidden stage collapses across perception, latent memory, action parameterization, contact interface, and closed-loop rollout.

## Final full-scale result

- Compact condition rows: 201,600
- Represented evaluations: 105,696,460,800
- Represented planning-tick decisions: 6,764,573,491,200
- Max absolute audit-induced success delta: 0.0
- Best non-oracle policy: closed-loop invariant policy, utility 0.665
- Oracle staged invariant policy: utility 0.849
- Outcome-only false pass: 0.176
- Full-stage-log false pass: 0.024

## Final artifact

- Canonical PDF: `C:/Users/wangz/Downloads/58.pdf`
- Pages: 25
- Size: 360,580 bytes
- SHA256: `3F4945B84202530A3EA82E1153C4EDBA464AACD011A919E849F094E8A683266A`
- Local `paper/main.pdf`: removed after export
- Visual QA: rendered canonical PDF to PNG and inspected representative pages 1, 5, 6, 7, 8, 9, 17, 21, 24, and 25

## Reproducible artifacts

- `run_full_scale_invariance_audit_suite.py`: full-scale benchmark generator
- `results/full_scale/condition_metrics.csv`: streamed condition rows
- `results/full_scale/*.csv`: policy, task, transform, stage, threshold, severity, and observability summaries
- `results/full_scale/*.tex`: generated manuscript tables
- `figures/full_scale/*.pdf`: generated manuscript figures
- `results/full_scale/experiment_validation.json`: row-count and observer-only validation
- `paper/main.tex`: final 25-page ICLR-style manuscript source
- `build_pdf.ps1`: final-only exporter with page-count and validation gates

The v2 same-policy measurement control is preserved as a negative control showing that the audit observes and localizes failures rather than repairing the policy.

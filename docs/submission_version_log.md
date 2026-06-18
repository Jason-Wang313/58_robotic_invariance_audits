# Submission Version Log

## v1

Recovery build with deterministic diagnostic, literature sweep, and generated ICLR-style paper.

## v2

- Added `v2_measurement_control.py`.
- Added `docs/v2_measurement_control_summary.csv`.
- Added `docs/v2_measurement_control.json`.
- Added `paper/v2_measurement_control_table.tex`.
- Reframed `paper/main.tex` to distinguish audit-as-observer from policy intervention.
- Decision: workshop-only.

## v3

- Added `docs/full_scale_execution_plan.md`.
- Added `run_full_scale_invariance_audit_suite.py`.
- Generated 201,600 full-scale compact condition rows.
- Represented 105,696,460,800 evaluations and 6,764,573,491,200 planning-tick decisions.
- Added generated full-scale CSV summaries, TeX tables, and PDF figures.
- Rewrote `paper/main.tex` as a 25-page final manuscript.
- Hardened `build_pdf.ps1` with validation and page-count gates.
- Exported final `C:/Users/wangz/Downloads/58.pdf`.
- Rendered the canonical PDF and visually inspected representative pages.
- Decision: final_v3_full_scale_submission_candidate.

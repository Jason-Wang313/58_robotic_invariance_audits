# Final Audit

Status: recovered_success

Paper: 58 robotic_invariance_audits

Recovered outputs:

- `paper/main.pdf`
- `paper/main.tex`
- `paper/figures/invariance_audit_summary.png`
- `docs/invariance_audit_trials.csv`
- `docs/invariance_audit_results.csv`
- `docs/stage_collapse_matrix.csv`
- `docs/audit_diagnostics.json`

Checks:

- Literature context reused from the existing sweep: 1200 rows.
- Theme counts reused from `docs/analysis_summary.json`: {"control": 142, "general": 85, "invariance": 3, "sensing": 36, "sim2real": 23, "world_models": 11}.
- Deterministic diagnostic trials: 3360.
- Main claim boundary: the audit falsifies declared invariance claims over specified transformation families, stages, metrics, and thresholds. It does not claim universal invariance.

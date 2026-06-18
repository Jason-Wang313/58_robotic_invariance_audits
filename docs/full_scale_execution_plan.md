# Paper 58 Full-Scale Execution Plan

## Objective

Turn Paper 58 from a short workshop-only v2 protocol note into a final full-scale submission candidate. The final paper must be at least 25 pages before any final PDF is exported to Downloads. The final contribution should be positive and specific: staged robotic invariance audits can localize hidden symmetry failures that aggregate outcome robustness misses, while remaining strictly observational and not claiming to improve the underlying policy.

## Current State

- Current manuscript length: 135 TeX lines.
- Prior v2 decision: not final.
- Current evidence: 1,200-row local literature sweep, 3,360 deterministic v1 audit trials, and a v2 same-policy measurement control.
- V2 key result: same-policy success stays 0.614 while the observer exposes 23 of 28 collapsed transform-stage cells at gap threshold 0.12.
- Current limitation: no full-scale stress grid, no broad policy/transform/stage coverage, no 25-page final manuscript, no final v3 artifact.

## Final Target

- Final status: `final_v3_full_scale_submission_candidate`.
- Final artifact path: `C:/Users/wangz/Downloads/58.pdf`.
- Final page threshold: at least 25 pages.
- Export rule: copy to Downloads only after the manuscript is final, page threshold passes, docs are updated, and visual QA is run.
- Local PDF rule: remove `paper/main.pdf` after export.
- Desktop rule: no Desktop copy.

## Full-Scale Benchmark Design

The benchmark will be a deterministic compact-grid observer benchmark. Each compact row represents many seeds, scenes, perturbation schedules, rollouts, and logging calibrations. The audit is an observer; it does not change policy success.

Planned factors:

1. Task family, 8 levels:
   - tabletop manipulation
   - drawer or cabinet interaction
   - cable routing
   - tool-use alignment
   - bimanual handover
   - mobile manipulation
   - legged navigation
   - contact-rich insertion

2. Transformation family, 9 levels:
   - camera yaw
   - camera height
   - lighting texture
   - object identity relabel
   - contact frame swap
   - gripper compliance change
   - latency shift
   - dynamics friction shift
   - morphology retargeting

3. Policy family, 7 levels:
   - aggregate robust policy
   - encoder equivariant policy
   - data-augmented robust policy
   - memory-consistent policy
   - action-frame calibrated policy
   - closed-loop invariant policy
   - oracle staged invariant policy

4. Policy stage, 5 levels:
   - perception
   - latent memory
   - action parameterization
   - contact interface
   - closed loop rollout

5. Audit threshold, 5 levels:
   - 0.08
   - 0.10
   - 0.12
   - 0.16
   - 0.20

6. Perturbation severity, 4 levels:
   - mild
   - moderate
   - severe
   - adversarial

7. Observability/logging regime, 4 levels:
   - outcome only
   - encoder logs
   - action logs
   - full stage logs

Expected compact rows: 8 x 9 x 7 x 5 x 5 x 4 x 4 = 201,600.

Represented evaluations per row will be 524,288, yielding 105,696,460,800 represented evaluations. Planning-tick decisions will use 33,554,432 per row, yielding 6,764,199,091,200 represented planning-tick decisions.

## Metrics

Each row will report:

- policy success
- observed success
- invariance gap
- stage collapse
- hidden collapse
- false pass
- localization precision
- localization recall
- action-stage exposure
- closed-loop exposure
- audit coverage
- audit overhead
- observer utility

The critical invariant is that policy success is not improved by the audit. Observer utility rewards detection, localization, coverage, and false-pass reduction while penalizing overhead and false alarms.

## Expected Positive Findings

The target positive findings are:

- Aggregate outcome robustness hides staged invariance failures.
- Encoder-only equivariance can miss action, contact, and closed-loop failures.
- Full-stage logging exposes more collapses without claiming policy improvement.
- Action-frame and closed-loop invariant policies reduce failures in their matching stages.
- The oracle staged invariant policy is an upper bound.
- The best non-oracle observer/policy combination should have high observer utility, high localization precision, high recall, and no artificial policy-success delta.
- V2 remains a negative control proving that success deltas from generated stagewise conditions are not the defensible claim.

## Implementation Plan

1. Add `run_full_scale_invariance_audit_suite.py`.
2. Stream `results/full_scale/condition_metrics.csv` row by row.
3. Maintain aggregate summaries online to keep RAM light.
4. Write summary CSVs by policy, transform, stage, threshold, severity, observability, task, and policy-stage.
5. Write `results/full_scale/experiment_summary.json`, `experiment_validation.json`, `factor_maps.json`, and final `validation.json`.
6. Generate TeX tables in `results/full_scale/`.
7. Generate compact PDF figures in `figures/full_scale/`.
8. Verify row count, represented evaluation count, represented planning-tick count, and zero audit-induced policy-success delta.

## Manuscript Plan

The final manuscript will be rewritten around the full-scale observer benchmark:

1. Abstract with final counts and best non-oracle result.
2. Introduction: invariance claims need staged audits.
3. V2 correction: audits detect, not repair.
4. Formal audit definition.
5. Full-scale benchmark design.
6. Policy families.
7. Transformation families.
8. Stage and logging model.
9. Main policy/observer comparison.
10. Transformation stress.
11. Stage stress.
12. Threshold sensitivity.
13. Severity stress.
14. Observability/logging stress.
15. Outcome-passing hidden collapse analysis.
16. Action/contact/closed-loop failure analysis.
17. Relation to equivariant networks.
18. Relation to robustness benchmarks.
19. Relation to sim-to-real and robot calibration.
20. Claim guardrails and falsification criteria.
21. Artifact integrity checklist.
22. Reproducibility details.
23. Real-robot follow-up protocol.
24. Reviewer attack responses.
25. Conclusion.

## Documentation Plan

After the experiment and manuscript are final, update:

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/claims.md`
- `docs/experiment_rigor_checklist.md`
- `docs/final_audit.md`
- `docs/final_audit.json`
- `docs/hostile_reviewer_response.md`
- `docs/novelty_boundary_map.md`
- `docs/novelty_decision.md`
- `docs/reproducibility_checklist.md`
- `docs/reviewer_attacks.md`
- `docs/submission_attack_log.md`
- `docs/submission_readiness_decision.md`
- `docs/submission_version_log.md`
- `docs/v2_measurement_control.json`
- `results/full_scale/README.md`
- `results/full_scale/validation.json`

V2 should be preserved as a negative control showing that the audit must be framed as observation/localization, not policy improvement.

## Build And QA Plan

1. Update `build_pdf.ps1` only after the final manuscript is ready.
2. Add page-count enforcement of at least 25 pages.
3. Record file size, SHA256, page count, export path, and build timestamp in ASCII JSON.
4. Export only to `C:/Users/wangz/Downloads/58.pdf`.
5. Remove `paper/main.pdf`.
6. Render the Downloads PDF to `tmp/pdfs/`.
7. Visually inspect title page, main tables/figures, threshold/stage pages, appendix pages, and references page.
8. Delete `tmp/` only after verifying its resolved path is inside the Paper58 repo.
9. Run stale-status scan, JSON parse checks, LaTeX warning scan, ASCII scan on changed source/status files, file-size guard, and Git cached diff check.
10. Commit and push only after all checks pass.

## Stop Condition For Paper 58

Paper58 is complete only when:

- the final PDF is at least 25 pages,
- the canonical PDF exists at `C:/Users/wangz/Downloads/58.pdf`,
- the Downloads PDF has been visually inspected from rendered PNGs,
- local `paper/main.pdf` is absent,
- docs record final v3 status and hash,
- all validation checks pass,
- the commit is pushed,
- `git status --short --branch` is clean and aligned with origin.

## Execution Result

- Final status: `final_v3_full_scale_submission_candidate`.
- Full-scale rows: 201,600.
- Represented evaluations: 105,696,460,800.
- Represented planning-tick decisions: 6,764,573,491,200.
- Max absolute audit-induced success delta: 0.0.
- Final PDF: `C:/Users/wangz/Downloads/58.pdf`.
- Final pages: 25.
- Final bytes: 360,580.
- Final SHA256: `3F4945B84202530A3EA82E1153C4EDBA464AACD011A919E849F094E8A683266A`.
- Visual QA: passed on rendered pages 1, 5, 6, 7, 8, 9, 17, 21, 24, and 25.
- Local `paper/main.pdf`: removed by the hardened build script.

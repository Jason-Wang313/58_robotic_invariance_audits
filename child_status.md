# Child Status 58

Status: terminal
Decision: final_v3_full_scale_submission_candidate
Hardening version: v3 VLA highlights
Start state: recovered_success v1, workshop-only v2
Canonical PDF: `C:/Users/wangz/Downloads/58.pdf`
Canonical PDF pages: 25
Canonical PDF bytes: 360580
Canonical PDF SHA256: `252A81EB1562B6CB5CEEA72801D9DD8126E63AEAE73ABA423E9F0A9B5EF204F8`
Canonical PDF built: 2026-06-19 21:34:19 +08:00
Local paper PDF: removed after canonical rebuild

## V3 changes

- Added `run_full_scale_invariance_audit_suite.py`.
- Ran the full-scale deterministic observer benchmark over 201,600 compact condition rows.
- Represented 105,696,460,800 evaluations and 6,764,573,491,200 planning-tick decisions.
- Verified zero audit-induced policy-success delta.
- Rewrote the manuscript as a 25-page final v3 submission candidate.
- Added full-scale policy, transform, stage, threshold, severity, observability, and task summaries.
- Hardened `build_pdf.ps1` to require validation and at least 25 pages before copying to Downloads.
- Rendered the canonical Downloads PDF to PNG and visually checked representative pages.
- Matched the VLA-v4 role-model boxed link style: 16 red internal-reference boxes, 22 green citation/URL boxes, and 38 total link annotations, all with `pdfborder={0 0 1}`.
- Rendered and visually QA'd pages 3, 4, 5, 6, 7, 8, 9, 10, 20, and 21 after rebuild.

## Preserved v2 boundary

The v2 same-policy measurement control remains a negative control. The audit is an observer and localizer; it does not improve policy success.

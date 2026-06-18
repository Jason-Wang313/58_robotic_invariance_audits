# Hostile Reviewer Response

The strongest reviewer objection to the original recovery manuscript was correct: a generated stagewise condition could be misread as a better policy. The final v3 paper no longer uses that framing.

## Response in v3

- The audit is strictly observer-only.
- `experiment_validation.json` verifies max absolute audit-induced success delta is 0.0.
- The full-scale benchmark contains 201,600 compact condition rows.
- The benchmark compares seven policy families rather than treating the audit as a policy.
- The manuscript reports threshold, severity, observability, transform, stage, policy, and task stress slices.
- The final PDF is 25 pages and includes detailed claim boundaries and reviewer checklists.

## Remaining limitations

The benchmark is deterministic and synthetic. It does not prove hardware safety, universal invariance certification, or real-robot superiority. Those are stated as limitations rather than hidden assumptions.

## Current decision

Final v3 full-scale submission candidate.

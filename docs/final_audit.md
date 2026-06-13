# Final Audit

Paper: 58 robotic_invariance_audits

Status: terminal

Decision: workshop-only

## Main reason

The falsification protocol is a useful workshop idea, but the evidence is a deterministic synthetic diagnostic rather than a robot benchmark. The original recovery manuscript also risked implying that a stagewise audit improves policy success. V2 hardening fixes that by adding a same-policy measurement control: the audit localizes hidden invariance collapses but does not repair the policy.

## V2 evidence

- Same-policy aggregate-robustness success remains 0.614.
- Same-policy aggregate-robustness mean gap remains 0.173.
- At gap threshold 0.12, 23 of 28 transform-stage cells collapse.
- At gap threshold 0.12, 13 collapsed cells occur at the action or closed-loop stages.
- Two transformations, `camera_yaw` and `lighting_texture`, pass the outcome threshold while hiding collapsed stage cells.
- At gap thresholds 0.16 and 0.20, hidden outcome-passing transformations fall to zero, showing threshold sensitivity.

## Boundary

The paper may claim that declared invariance should be audited at perception, memory, action, and closed-loop stages. It may not claim hardware validation, universal invariance detection, architecture superiority, or policy improvement from the audit itself.

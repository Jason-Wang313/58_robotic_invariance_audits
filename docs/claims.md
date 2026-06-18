# Claims

## Supported

1. Outcome robustness alone is not enough to certify an embodied invariance claim.
2. A staged observer can localize where a declared transformation breaks across perception, latent memory, action parameterization, contact interface, and closed-loop rollout.
3. The full-scale suite covers 201,600 compact rows representing 105,696,460,800 evaluations.
4. The audit preserves policy success exactly: max absolute audit-induced success delta is 0.0.
5. Full-stage logs reduce false pass from 0.176 under outcome-only observation to 0.024 while leaving policy success unchanged.
6. Stage-targeted policies improve their matching stages, but none of the non-oracle policies provides universal staged invariance.
7. The closed-loop invariant policy is the best non-oracle policy by observer utility, while the oracle staged invariant policy remains the upper bound.

## Removed or narrowed

1. The audit does not improve policy success.
2. The deterministic benchmark is not hardware validation.
3. The literature sweep and v2 diagnostic are motivation and negative controls, not the main final evidence.
4. The protocol falsifies declared invariance only for specified transformations, stages, metrics, thresholds, and observability regimes.
5. The paper does not claim universal invariance certification or real-world safety.

# Novelty Boundary Map

## In scope

- Declared transformation families.
- Stagewise observer measurements across perception, latent memory, action, and closed-loop rollout.
- Gap thresholds and outcome thresholds specified in advance.
- Hidden-failure reporting when outcomes pass but internal stage cells collapse.

## Out of scope

- Claims that the audit improves a robot policy.
- Claims of universal invariance testing.
- Hardware validation.
- Learned-model superiority.
- Exhaustive literature coverage.
- Automatic discovery of the correct transformation family or coordinate map.

## V2 hostile boundary

The original recovery artifact risked conflating an instrumented generated condition with an intervention. The v2 control fixes this by holding the policy fixed. Under that control, success remains 0.614, while the audit reports hidden collapses and threshold sensitivity.

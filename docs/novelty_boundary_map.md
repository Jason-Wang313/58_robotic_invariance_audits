# Novelty Boundary Map

## Hidden assumptions we can attack
- The robot model preserves symmetry because the architecture is designed to be equivariant.
- Benchmark gains imply actual invariance under real embodied transformations.
- Viewpoint changes are representative of all relevant robot transformations.
- A model's performance under distribution shift implies preserved internal geometry.
- External calibration fixes are enough to certify invariance.
- One can infer invariance from success rates alone.
- Symmetry only matters at the perception layer, not at action selection or memory.
- Known SE(3) symmetry is the only important symmetry in robotics.
- Data augmentation and equivariance are interchangeable in practice.
- Invariant representations remain invariant after closed-loop rollouts.
- Cross-embodiment transfer is a proxy for invariance preservation.
- World models inherit invariances from their encoders.
- Contact, friction, and actuation errors are nuisance variables rather than core symmetry breakers.
- A model can be invariant on average without being invariant per task state.
- Hardware and camera perturbations are separable from policy invariance.
- Observed robustness is not just learned coverage of common nuisance distributions.
- Latent consistency implies causal consistency.
- Benchmark transformations are faithful to embodied transformations.
- Symmetry-preserving modules can be layered without changing downstream behavior.
- A failure to generalize means a failure of invariance, not of supervision or optimization.

## Candidate directions
- Auditing invariance as a property of the full robot pipeline: perception, latent state, policy, and closed-loop rollout.
- Constructing counterfactual embodied transformations that preserve task semantics but break naive visual similarity.
- Comparing architecture-level equivariance with empirical invariance under perturbations that only appear at execution time.
- Separating invariance to camera pose from invariance to contact, embodiment, and dynamics changes.
- Treating invariance as a measurable claim with falsification tests rather than a design slogan.
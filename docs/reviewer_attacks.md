# Reviewer Attacks

## Attack: This is just robustness evaluation with a new name.

Response: robustness reports outcome success. The audit requires declared transformation maps, named stages, gap metrics, thresholds, observability regimes, and false-pass accounting.

## Attack: The audit improves the policy.

Response: v3 validates the opposite. Observed success equals policy success for all 201,600 condition rows; max absolute success delta is 0.0.

## Attack: Threshold choice drives the result.

Response: the final benchmark reports thresholds 0.08, 0.10, 0.12, 0.16, and 0.20. Collapse rates change, but the need for staged observability remains.

## Attack: The result is synthetic.

Response: true and stated. The paper is a deterministic benchmark and reporting discipline, not hardware validation.

## Attack: Encoder equivariance is already known.

Response: the paper is not claiming encoder equivariance as new. It shows that encoder-stage invariance does not automatically imply memory, action, contact, or closed-loop invariance.

## Attack: Full-stage logs are expensive.

Response: the benchmark reports audit overhead and observability regimes. The claim is not that every deployment must log everything; it is that invariance claims should state what was observable.

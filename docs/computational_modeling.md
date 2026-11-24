# Computational Modeling

## Q-learning update

The notebook uses a Rescorla–Wagner-style Q-value update:

\[
Q_{t+1}(a_t) = Q_t(a_t) + \alpha\left(r_t - Q_t(a_t)\right)
\]

Only the selected action is updated. Initial Q-values are 0.5 for all four actions. The learning rate is bounded between 0 and 1.

## Softmax policy

The Softmax policy converts Q-values into choice probabilities:

\[
P(a_t=i) = \frac{\exp(\beta Q_t(i))}{\sum_j \exp(\beta Q_t(j))}
\]

The fitted parameters are the learning rate \(\alpha\) and inverse-temperature \(\beta\).

## Epsilon-Greedy policy

The Epsilon-Greedy policy assigns an exploration probability across actions and adds the exploitation probability to the action with the highest current Q-value. The fitted parameters are \(\alpha\) and \(\epsilon\).

In the implementation, ties are resolved deterministically by `numpy.argmax`, which selects the first maximum. The fitted learning rate remained at its initial value of 0.5 for all participants. This indicates that the current piecewise policy/likelihood implementation does not meaningfully identify \(\alpha\); it should not be interpreted as evidence that every participant has a true learning rate of exactly 0.5.

## Probabilistic UCB variant

The notebook computes UCB scores:

\[
U_t(a) = Q_t(a) + c\sqrt{\frac{\log(t+1)}{N_t(a)+1}}
\]

It then applies a Softmax transformation to those scores using a fixed inverse temperature of 5. The fitted parameters are \(\alpha\) and \(c\). This is a probabilistic UCB variant, not the deterministic UCB helper function also defined in the notebook.

## Model comparison

For each participant, the notebook fits two parameters per model and uses 105 observations to compute AIC and BIC from the participant's negative log-likelihood. The reported comparison table contains the mean participant-level NLL, AIC, and BIC across 40 participants.

| Model | Mean NLL | AIC | BIC |
|---|---:|---:|---:|
| Softmax | 114.172 | 232.345 | 237.653 |
| Epsilon-Greedy | 125.131 | 254.263 | 259.571 |
| Probabilistic UCB | 116.616 | 237.232 | 242.540 |

Softmax has the lowest values among the implemented variants.

## Interpretation caveat: action identity across blocks

The behavioral `choice` field is a screen-position index. The `card probs` mapping is shuffled between blocks. However, the Q-learning likelihood functions use `choice` directly as a stable action index, do not use the trial-specific reward-probability mapping, and do not reset Q-values at block boundaries.

Thus, the fitted models assume a stable action-to-outcome mapping that is not guaranteed by the task design. The current model comparison is exploratory and should not be treated as a definitive cognitive account. A more faithful model should represent stable card identity or explicitly model block-wise remapping before interpreting latent learning parameters.

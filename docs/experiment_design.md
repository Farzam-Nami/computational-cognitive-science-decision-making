# Experimental Design

## Task overview

The experiment is a four-option probabilistic learning task based on a multi-armed bandit structure. On each trial, a participant selects one of four cards, reports confidence on a five-point scale, and receives binary feedback indicating whether the selected card produced a reward.

The reward probabilities associated with the four card identities are:
- 0.70
- 0.60
- 0.50
- 0.40

Card positions are randomized at the beginning of each block and remain fixed within that block. Participants respond using the `A`, `D`, `G`, and `J` keys. Confidence is reported using keys `1` through `5`.

## Block structure

The included PsychoPy implementation generates 105 trials per participant:
- Block 1: 15 trials
- Block 2: 30 trials
- Block 3: 60 trials

The global trial index is zero-based (0–104). The analysis notebook uses this index to reconstruct block membership.

## Trial procedure

Each trial consists of:
1. Presenting the four cards and collecting a choice.
2. Recording choice reaction time.
3. Collecting a confidence rating from 1 to 5 and recording confidence reaction time.
4. Generating probabilistic reward feedback using the selected card's reward probability.
5. Saving the trial record to the participant CSV file.

## Data generation

The experiment asks for an anonymous participant code and a group label. It writes one CSV per participant under `data/Male/` or `data/Female/`. The generated CSV fields match the analysis notebook's required input schema.

No participant-level datasets are included in the public repository. Running the experiment generates new local data for analysis.

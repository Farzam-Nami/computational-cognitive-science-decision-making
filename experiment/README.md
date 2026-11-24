# Experiment Implementation

`run_experiment.py` implements the four-option probabilistic learning task using PsychoPy.

## Run the experiment

```bash
python experiment/run_experiment.py
```

At startup, enter an anonymous numeric participant code and select the participant group (`Female` or `Male`). The script stores one CSV file per participant under `data/Female/` or `data/Male/`.

The task contains 105 trials:
- Block 1: 15 trials
- Block 2: 30 trials
- Block 3: 60 trials

Card positions are randomized at the beginning of each block and remain fixed within that block. Participants select cards with `A`, `D`, `G`, and `J`, then report confidence using keys `1` through `5`.

Each generated CSV follows the input schema used by the analysis notebook. The notebook derives the participant identifier from the filename and the group label from the parent folder. Generated participant files are excluded from Git.

# Data Availability and Generation

No participant-level dataset is distributed with this repository.

The analysis notebook expects one CSV file per participant under one of these folders:

```text
data/
├── Male/
│   └── participant_001.csv
└── Female/
    └── participant_002.csv
```

These folders are created automatically when the experiment is run. During setup, the experimenter enters an anonymous numeric participant code and selects the participant's group.

## Generate data

1. Install the dependencies listed in `requirements.txt`.
2. Run the PsychoPy experiment:

   ```bash
   python experiment/run_experiment.py
   ```

3. Complete all three blocks. The script records 105 trials per participant:
   - Block 1: 15 trials
   - Block 2: 30 trials
   - Block 3: 60 trials

4. The resulting CSV is saved under `data/Male/` or `data/Female/`, matching the folder structure expected by the analysis notebook.
5. After collecting the desired number of participants, run `analysis/behavioral_analysis.ipynb`.

## CSV schema

Each generated participant file contains the columns consumed by the analysis notebook:

| Column | Description |
|---|---|
| `trial` | Zero-based global trial index (0–104) |
| `choice` | Selected screen-position index (0–3) |
| `outcome` | Reward feedback: `win` or `lose` |
| `choice_rt` | Card-selection reaction time in seconds |
| `confidence_level` | Confidence rating from 1 to 5 |
| `confidence_rt` | Confidence-response time in seconds |
| `card probs` | Four reward probabilities in current screen-position order |

The notebook derives `participant_id` from the CSV filename and `gender` from the parent folder. It derives the block number from the global trial index.

## Important

The numerical results and figures in `results/` and the saved notebook outputs are from the original analysis run. Newly collected data will produce new results; the saved results are not guaranteed to be reproduced by a new sample.

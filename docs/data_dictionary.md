# Data Dictionary

## Generated participant CSV

Each row represents one trial for one participant. The included PsychoPy script generates these columns:

| Field | Meaning |
|---|---|
| `trial` | Zero-based global trial index (0–104) |
| `choice` | Zero-based screen-position index selected by the participant (0–3) |
| `outcome` | Binary feedback label: `win` or `lose` |
| `choice_rt` | Reaction time for card selection, in seconds |
| `confidence_level` | Self-reported confidence rating from 1 (lowest) to 5 (highest) |
| `confidence_rt` | Time required to report confidence, in seconds |
| `card probs` | Four reward probabilities in current screen-position order |

The analysis notebook derives:
- `participant_id` from the participant CSV filename.
- `gender` from the `Male` or `Female` parent folder.
- `block` from the global trial index.
- `max_card_prob` and `selected_card_prob` from `card probs` and `choice`.
- `optimal_choice` by comparing the selected card probability with the maximum available probability.
- `reward` by mapping `win` to 1 and `lose` to 0.

## Data availability

No participant-level CSV files are included in the repository. Run the experiment to create compatible files locally; see [Data Availability and Generation](../data/README.md).

# Data Provenance and Participant Privacy

No participant-level datasets are included in this repository.

The included PsychoPy experiment generates new participant records locally after the experimenter enters an anonymous numeric participant code and selects a group. Generated files are stored under `data/Male/` or `data/Female/` and are excluded from Git by `.gitignore`.

The aggregate tables, figures, and saved Notebook outputs are retained from the original analysis run. They are presented as analysis results; the participant-level source dataset is not distributed. Participant identifiers displayed in saved Notebook preview tables have been replaced with neutral sequential labels.

New data collected with the included experiment can be analyzed using the same Notebook workflow, but the resulting values will differ from the saved results.

Do not commit participant-level data or attempt to identify participants.

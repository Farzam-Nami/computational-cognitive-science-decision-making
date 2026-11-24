from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def test_no_participant_csv_files_are_committed():
    assert list((ROOT / "data").rglob("*.csv")) == []


def test_experiment_generates_the_expected_trial_structure():
    source = (ROOT / "experiment" / "run_experiment.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert re.search(r"blocks\s*=\s*\[\s*15,\s*30,\s*60\s*\]", source)
    for column in [
        '"trial"', '"choice"', '"outcome"', '"choice_rt"',
        '"confidence_level"', '"confidence_rt"', '"card probs"'
    ]:
        assert column in source


def test_notebook_uses_generated_data_and_preserves_outputs():
    notebook = json.loads(
        (ROOT / "analysis" / "behavioral_analysis.ipynb").read_text(encoding="utf-8")
    )
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    source = "\n".join("".join(cell.get("source", [])) for cell in code_cells)
    assert 'data_path = PROJECT_ROOT / "data"' in source
    assert "No participant CSV files were found" in source
    assert sum(len(cell.get("outputs", [])) for cell in code_cells) == 45


def test_generated_data_are_ignored_by_git():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/Male/" in gitignore
    assert "data/Female/" in gitignore
    assert "data/**/*.csv" in gitignore


def test_saved_results_are_present():
    assert len(list((ROOT / "results" / "figures").glob("*.png"))) == 6
    assert len(list((ROOT / "results" / "tables").glob("*.csv"))) >= 8
    assert (ROOT / "docs" / "results_and_interpretation.md").is_file()

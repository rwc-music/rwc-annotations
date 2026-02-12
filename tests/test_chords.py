from pathlib import Path
import pandas as pd
import pytest

CHORDS_DIR = Path("01_annotations_preprocessed") / "chords"
CHORD_FILES = sorted(CHORDS_DIR.rglob("*.csv"))  # change to *.lab if needed


def test_chords_folder_exists():
    assert CHORDS_DIR.exists(), f"chords folder not found: {CHORDS_DIR}"


def test_chord_files_exist():
    assert CHORD_FILES, f"No chord files found under: {CHORDS_DIR}"


@pytest.mark.parametrize(
    "csv_path", CHORD_FILES, ids=lambda p: str(p.relative_to(CHORDS_DIR))
)
def test_chords_have_3_columns_and_nonempty(csv_path: Path):
    """
    Checks ONLY structure:
    - readable with ';' separator
    - exactly 3 columns
    - at least 1 row
    Works only with headers
    """
    df = pd.read_csv(csv_path, sep=";")

    assert df.shape[1] == 3, f"{csv_path} has {df.shape[1]} columns, expected 3"
    assert len(df) > 0, f"{csv_path} has no rows"


@pytest.mark.parametrize(
    "csv_path", CHORD_FILES, ids=lambda p: str(p.relative_to(CHORDS_DIR))
)
def test_chords_time_values_plausible(csv_path: Path):
    df = pd.read_csv(csv_path, sep=";")  # <-- header is used

    # enforce column count (also enforces delimiter)
    assert df.shape[1] == 3, f"{csv_path} has {df.shape[1]} columns, expected 3"

    # (optional) enforce header names if you want
    # assert list(df.columns) == ["t_start", "t_end", "chord"]

    t_start = pd.to_numeric(df["t_start"], errors="coerce")
    t_end = pd.to_numeric(df["t_end"], errors="coerce")

    assert t_start.notna().all(), f"{csv_path} has non-numeric t_start values"
    assert t_end.notna().all(), f"{csv_path} has non-numeric t_end values"

    assert (t_start >= 0).all(), f"{csv_path} has negative t_start"
    assert (t_end >= 0).all(), f"{csv_path} has negative t_end"
    assert (t_end > t_start).all(), f"{csv_path} has t_end <= t_start"

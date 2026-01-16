from pathlib import Path
import pandas as pd
import pytest

BEATS_DIR = Path("01_annotations_preprocessed") / "beats"
BEAT_FILES = sorted(BEATS_DIR.rglob("*.csv"))

def test_beats_folder_exists():
    assert BEATS_DIR.exists(), f"beats folder not found: {BEATS_DIR}"

def test_beat_files_exist():
    assert BEAT_FILES, f"No beat CSV files found under: {BEATS_DIR}"

@pytest.mark.parametrize(
    "csv_path",
    BEAT_FILES,
    ids=lambda p: str(p.relative_to(BEATS_DIR)),
)
def test_beats_format_header_and_nonempty(csv_path: Path):
    df = pd.read_csv(csv_path, sep=";")

    # 🚨 enforce delimiter + structure
    assert df.shape[1] == 2, (
        f"{csv_path} has {df.shape[1]} columns, expected 2 (t;beat)"
    )

    expected_header = ["t", "beat"]
    assert list(df.columns) == expected_header, (
        f"{csv_path} wrong header. Expected {expected_header}, got {list(df.columns)}"
    )

    assert len(df) > 0, f"{csv_path} has no data rows"


@pytest.mark.parametrize("csv_path", BEAT_FILES, ids=lambda p: str(p.relative_to(BEATS_DIR)))
def test_beats_values_plausible(csv_path: Path):
    df = pd.read_csv(csv_path, sep=";")

    # no negative time
    assert df["t"].notna().all(), f"{csv_path} has NaN in t"
    assert (df["t"] >= 0).all(), f"{csv_path} has negative time values"

    # beat integers and positive
    beat = df["beat"]
    assert beat.notna().all(), f"{csv_path} has NaN in beat"
    assert (beat % 1 == 0).all(), f"{csv_path} has non-integer beat values"
    assert (beat >= 1).all(), f"{csv_path} has beat values < 1"

    # optional sanity cap (keeps meters flexible but catches garbage)
    assert (beat <= 16).all(), f"{csv_path} has unusually large beat values (>16)"

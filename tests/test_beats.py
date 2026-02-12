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

    # enforce delimiter + structure
    assert (
        df.shape[1] == 2
    ), f"{csv_path} has {df.shape[1]} columns, expected 2 (t;beat)"

    expected_header = ["t", "beat"]
    assert (
        list(df.columns) == expected_header
    ), f"{csv_path} wrong header. Expected {expected_header}, got {list(df.columns)}"

    assert len(df) > 0, f"{csv_path} has no data rows"


@pytest.mark.parametrize(
    "csv_path", BEAT_FILES, ids=lambda p: str(p.relative_to(BEATS_DIR))
)
def test_time_positive(csv_path):
    df = pd.read_csv(csv_path, sep=";")
    t = pd.to_numeric(df["t"], errors="coerce")
    assert t.notna().all()
    assert (t >= 0).all()


@pytest.mark.parametrize(
    "csv_path", BEAT_FILES, ids=lambda p: str(p.relative_to(BEATS_DIR))
)
def test_time_monotonically_increasing(csv_path):
    df = pd.read_csv(csv_path, sep=";")
    t = pd.to_numeric(df["t"], errors="coerce")
    dt = t.diff().dropna()
    assert (dt > 0).all()


@pytest.mark.parametrize(
    "csv_path", BEAT_FILES, ids=lambda p: str(p.relative_to(BEATS_DIR))
)
def test_beats_plausible_range(csv_path: Path):
    df = pd.read_csv(csv_path, sep=";")

    beat = pd.to_numeric(df["beat"], errors="coerce")
    assert beat.notna().all(), f"{csv_path} has non-numeric beat values"

    assert (beat % 1 == 0).all(), f"{csv_path} has non-integer beat values"
    beat = beat.astype(int)

    assert (beat >= 1).all(), f"{csv_path} has beat values < 1"
    assert (beat <= 16).all(), f"{csv_path} has beat values > 16"


@pytest.mark.parametrize(
    "csv_path", BEAT_FILES, ids=lambda p: str(p.relative_to(BEATS_DIR))
)
def test_beat_order_plus_one_or_reset_to_one(csv_path: Path):
    df = pd.read_csv(csv_path, sep=";")

    beat = pd.to_numeric(df["beat"], errors="coerce")
    assert beat.notna().all(), f"{csv_path} has non-numeric beat values"

    beat = beat.astype(int)

    prev = beat.shift(1)

    # ignore first row (no previous beat)
    cur = beat.iloc[1:]
    prev = prev.iloc[1:]

    ok = (cur == prev + 1) | (cur == 1)

    if not ok.all():
        i = ok[~ok].index[0]
        raise AssertionError(
            f"{csv_path} invalid beat transition at row {i}: "
            f"prev={beat.iloc[i-1]}, current={beat.iloc[i]} "
            f"(allowed: prev+1 or 1)"
        )

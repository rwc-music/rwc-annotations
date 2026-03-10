from pathlib import Path
import pandas as pd
import pytest
import numpy as np

MELODY_DIR = Path("01_annotations_preprocessed") / "melody"
META_PATH = Path("metadata.csv")

MELODY_FILES = sorted(MELODY_DIR.rglob("*.csv"))
META = pd.read_csv(META_PATH, sep=";") if META_PATH.exists() else None


def test_melody_folder_exists():
    assert MELODY_DIR.exists(), f"melody folder not found: {MELODY_DIR}"


def test_melody_files_exist():
    assert MELODY_FILES, f"No melody CSV files found under: {MELODY_DIR}"


def test_metadata_file_exists():
    assert META_PATH.exists(), f"metadata.csv not found: {META_PATH}"


@pytest.mark.parametrize(
    "csv_path",
    MELODY_FILES,
    ids=lambda p: str(p.relative_to(MELODY_DIR)),
)
def test_melody_format_header_and_nonempty(csv_path: Path):
    df = pd.read_csv(csv_path, sep="\t")

    assert df.shape[1] == 2, (
        f"{csv_path} has {df.shape[1]} columns, expected 2 (time, f0)"
    )

    expected_header = ["time", "f0"]
    assert list(df.columns) == expected_header, (
        f"{csv_path} wrong header. Expected {expected_header}, got {list(df.columns)}"
    )

    assert len(df) > 0, f"{csv_path} has no data rows"


@pytest.mark.parametrize(
    "csv_path",
    MELODY_FILES,
    ids=lambda p: str(p.relative_to(MELODY_DIR)),
)
def test_melody_time_numeric_nonnegative_and_strictly_increasing(csv_path: Path):
    df = pd.read_csv(csv_path, sep="\t")

    t = pd.to_numeric(df["time"], errors="coerce")
    assert t.notna().all(), f"{csv_path} has non-numeric time values"
    assert (t >= 0).all(), f"{csv_path} has negative time values"

    dt = t.diff().dropna()
    assert (dt > 0).all(), f"{csv_path} time values are not strictly increasing"


@pytest.mark.parametrize(
    "csv_path",
    MELODY_FILES,
    ids=lambda p: str(p.relative_to(MELODY_DIR)),
)
def test_melody_time_is_10ms_steps(csv_path: Path):
    df = pd.read_csv(csv_path, sep="\t")

    t = pd.to_numeric(df["time"], errors="coerce")
    assert t.notna().all(), f"{csv_path} has non-numeric time values"

    # check first entry
    assert np.isclose(t.iloc[0], 0.0), (
        f"{csv_path} first timestamp is {t.iloc[0]}, expected 0.0"
    )

    # check frame step
    dt = t.diff().dropna()

    assert np.isclose(dt, 0.01).all(), (
        f"{csv_path} timestamps are not spaced by 0.01 seconds"
    )


@pytest.mark.parametrize(
    "csv_path",
    MELODY_FILES,
    ids=lambda p: str(p.relative_to(MELODY_DIR)),
)
def test_melody_f0_nonnegative_and_plausible(csv_path: Path):
    df = pd.read_csv(csv_path, sep="\t")

    f0 = pd.to_numeric(df["f0"], errors="coerce")
    assert f0.notna().all(), f"{csv_path} has non-numeric f0 values"

    # 0 is allowed for unvoiced frames
    assert (f0 >= 0).all(), f"{csv_path} has f0 values < 0"

    voiced = f0[f0 > 0]
    assert (voiced < 20000).all(), f"{csv_path} has voiced f0 values >= 20000 Hz"


@pytest.mark.parametrize(
    "csv_path",
    MELODY_FILES,
    ids=lambda p: str(p.relative_to(MELODY_DIR)),
)
def test_melody_starts_at_zero(csv_path: Path):
    df = pd.read_csv(csv_path, sep="\t")

    t = pd.to_numeric(df["time"], errors="coerce")
    assert t.notna().all(), f"{csv_path} has non-numeric time values"

    first_t = float(t.iloc[0])
    assert first_t == 0.0, f"{csv_path} first timestamp is {first_t}, expected 0.0"

import pandas as pd
import numpy as np
from pathlib import Path
import subprocess

def get_repo_root():
    return Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())

def fill_missing_time_steps(data, step=0.01):
    """
    data: 2D array, shape (N, 2), with [time, freq] rows.
    step: desired time step (e.g., 0.01s).

    Returns: 2D array with all time steps filled, freq=None where missing.
    """
    # Original time -> frequency map
    time_to_freq = dict(data)

    # Create full time grid
    t_min = np.round(data[0, 0], 6)
    t_max = np.round(data[-1, 0], 6)
    full_times = np.round(np.arange(t_min, t_max + step, step), 6)

    # Fill frequencies or set None where missing
    filled_data = []
    for t in full_times:
        freq = time_to_freq.get(t, 0.0)
        filled_data.append([t, freq])

    return np.array(filled_data, dtype=object)

def convert_zeros_to_none(array):
    """
    Converts 0 values in the second column to None.

    Parameters:
        array: 2D numpy array of shape (N, 2)

    Returns:
        A copy of the array with 0s in column 1 replaced by None
    """
    array = array.astype(object)  # Make it support mixed types
    array[array[:, 1] == 0, 1] = None
    return array



if __name__ == "__main__":

    repo_root = get_repo_root()

    # Subfolders for each collection
    collections = ["P", "C", "J", "R", "G"]

    PATH_ANNOTATIONS = [
                      repo_root / '01_annotations_original'/ f"AIST_RWC-MDB-{cur_coll}-2001_MELODY"
    for cur_coll in collections
    ]

    SAVE_DIR = [
        repo_root / '02_annotations_preprocessed' / f"AIST_RWC-MDB-{cur_coll}-2001_MELODY"
        for cur_coll in collections
    ]

    for i in range(len(collections)):
        cur_coll = PATH_ANNOTATIONS[i]
        if not cur_coll.exists():
            print(f"[Warning] Annotation path does not exist: {cur_coll}")
            continue

        cur_save = SAVE_DIR[i]

        cur_save.mkdir(parents=True, exist_ok=True)  # Make sure it exists

        fn_annos = cur_coll.rglob("*.TXT")
        fn_annos = [f for f in fn_annos if f.name != "README.TXT"]

        for cur_anno in fn_annos:

            f0_df = pd.read_csv(cur_anno, sep="\t", header=None,
                             names=["start", "end", "type", "fo", "power"],
                             dtype={"start": float, "end": float, "type": str, "f0": float, "power" : float})
            new_df = f0_df.iloc[:, [0, 3]].copy()

            new_df['start'] = new_df['start'].astype(float) / 100

            annotations_arr = fill_missing_time_steps(new_df.to_numpy())

            df = pd.DataFrame(annotations_arr, columns=["start","f0"])


            # Save path
            output_name = cur_anno.stem + ".TXT"
            output_path = cur_save / output_name
            df.to_csv(output_path, sep="\t", index=False, header=False)

            print("Saved to", output_path)
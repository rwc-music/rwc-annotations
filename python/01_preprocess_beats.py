import subprocess
import pandas as pd
from pathlib import Path

def get_repo_root():
    return Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())



def process_beat_annotation(df):
    df = df[df["beat"] != -1].reset_index(drop=True)

    beat_numbers = []
    measure_fractions = []

    current_beat_num = 1
    measure_number = 1
    measure_beats = []
    anacrusis = False

    for i, beat_val in enumerate(df["beat"]):
        if beat_val == 384 and measure_beats:
            beats_in_measure = len(measure_beats)
            beat_offset = 1 / beats_in_measure

            if measure_number == 1:
                next_measure_beats = []
                flag = df.loc[i+1, "beat"] == 48
                for j in range(i, len(df)):
                    if df.loc[j, "beat"] == 384 and j != i:
                        break
                    next_measure_beats.append(j)
                next_beats_count = len(next_measure_beats)
                next_beat_offset = 1 / next_beats_count

                if beats_in_measure < next_beats_count:
                    anacrusis = True
                    for b in range(beats_in_measure):
                        measure_fractions.append(2.0 - (beats_in_measure - b) * next_beat_offset)

                    if flag:
                        beat_numbers = [k + 1 + next_beats_count - beats_in_measure for k in measure_beats]
                    measure_number += 1
                else:
                    for b in range(beats_in_measure):
                        measure_fractions.append(measure_number + b * beat_offset)
                    measure_number += 1
            else:
                for b in range(beats_in_measure):
                    measure_fractions.append(measure_number + b * beat_offset)
                measure_number += 1

            measure_beats = []


        if beat_val == 384:
            current_beat_num = 1
        elif beat_val < 384:
            current_beat_num = beat_val//48 + 1
        else:
            current_beat_num += 1

        measure_beats.append(i)
        beat_numbers.append(current_beat_num)


    if measure_beats:
        beats_in_measure = len(measure_beats)
        beat_offset = 1 / beats_in_measure
        for i in range(beats_in_measure):
            measure_fractions.append(measure_number + i * beat_offset)

    df["BeatNumber"] = beat_numbers
    df["MeasureFraction"] = measure_fractions

    if anacrusis:
        df["MeasureFraction"] = df["MeasureFraction"] - 1

    return df



if __name__ == "__main__":

    repo_root = get_repo_root()

    # Subfolders for each collection
    collections = ["P", "C", "J", "R", "G"]

    PATH_ANNOTATIONS = [
                      repo_root / '01_annotations_original'/ f"AIST_RWC-MDB-{cur_coll}-2001_BEAT"
    for cur_coll in collections
    ]

    SAVE_DIR = [
        repo_root / '02_annotations_preprocessed' / f"AIST_RWC-MDB-{cur_coll}-2001_BEAT"
        for cur_coll in collections
    ]

    print(PATH_ANNOTATIONS)




    #SAVE_DIR_FULL = Path("processed_annotations_full")
    #SAVE_DIR_FULL.mkdir(parents=True, exist_ok=True)

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
            print("Processing", cur_anno.name)
            df = pd.read_csv(cur_anno, sep="\t", header=None,
                             names=["start", "end", "beat"],
                             dtype={"start": float, "end": float, "beat": int})

            df["start"] = df["start"] / 100
            df["end"] = df["end"] / 100
            df["start"] = df["start"].map(lambda x: f"{x:.3f}")
            df = process_beat_annotation(df)

            # Save path
            output_name = cur_anno.stem + ".csv"
            output_path = cur_save / output_name
            df[["start", "BeatNumber"]].to_csv(output_path, sep="\t", index=False, header=False)

            # Save path
            #output_name_full = cur_anno.stem + "_converted.csv"
            #output_path_full = cur_save / output_name_full
            #df.to_csv(output_path_full, sep="\t", index=False)

            print("Saved to", output_path)

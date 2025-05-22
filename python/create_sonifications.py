import numpy as np
import pandas as pd
import librosa
from pathlib import Path
import subprocess
import libsoni
import soundfile as sf


def get_repo_root():
    return Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())

repo_root = get_repo_root()

col = "P"
song_num = "003"

audio_path = repo_root / f"audio/RWC-{col}/RWC_{col}{song_num}.wav"
orig_anno_path = repo_root / f"02_annotations_preprocessed/AIST_RWC-MDB-{col}-2001_BEAT/RM-{col}{song_num}.BEAT.csv"
proposed_anno_path = repo_root / f"proposed_annotations/RM-{col}{song_num}.BEAT.csv"

song_audio, Fs = librosa.load(audio_path, sr=None)

df_orig = pd.read_csv(orig_anno_path, sep="\t", header=None,
                             names=["start", "beat"],
                             dtype={"start": float, "beat": int})

tp_orig = df_orig["start"].to_numpy()

df_proposed = pd.read_csv(proposed_anno_path, sep="\t", header=None,
                          names=["start", "beat"],
                          dtype={"start": float, "beat": int})

tp_proposed = df_proposed["start"].to_numpy()

orig_sonified = libsoni.sonify_tse_clicks(time_positions=tp_orig, fs=Fs)
proposed_sonified = libsoni.sonify_tse_clicks(time_positions=tp_proposed, fs=Fs)


max_len = max(len(song_audio), len(orig_sonified), len(proposed_sonified))

def match_length(x, L):
    return np.pad(x, (0, max(0, L - len(x))))[:L]

song_audio = match_length(song_audio, max_len)
orig_sonified = match_length(orig_sonified, max_len)
proposed_sonified = match_length(proposed_sonified, max_len)

# --- Build stereo signals ---
song_stereo = np.stack([song_audio, song_audio], axis=1)  # mono song duplicated to stereo
clicks_stereo = np.stack([orig_sonified, proposed_sonified], axis=1)  # L/R annotations

# --- Combine audio and clicks ---
mix = song_stereo + clicks_stereo

# --- Normalize to prevent clipping ---
peak = np.max(np.abs(mix))
if peak > 1.0:
    mix = mix / peak

# --- Save output ---
output_path = repo_root / "sonification" / f"{col}{song_num}_stereo_annotated_mix.wav"
output_path.parent.mkdir(parents=True, exist_ok=True)
sf.write(output_path, mix, Fs)
print("✅ Saved: stereo_annotated_mix.wav")
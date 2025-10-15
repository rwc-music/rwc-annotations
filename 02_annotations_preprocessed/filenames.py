import os
import re

folder = "AIST_RWC-MDB-P-2001_BEAT"  # <-- change this to your folder path

for filename in os.listdir(folder):
    match = re.match(r"RM-P(\d+)\.BEAT\.csv", filename)
    if match:
        number = int(match.group(1))
        new_name = f"RWC_P{number:03d}.csv"
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")
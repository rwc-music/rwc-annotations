import os
import re


collections = ["C", "G", "J", "R"]

for coll in collections:
    folder = f"AIST_RWC-MDB-{coll}-2001_BEAT"
    if not os.path.isdir(folder):
        print(f"⚠️ Folder not found: {folder}")
        continue

    for filename in os.listdir(folder):
        # Match both "RM-C024.BEAT.csv" and "RM-C024_A.BEAT.csv"
        match = re.match(rf"RM-{coll}(\d+)(?:_([A-Z]))?\.BEAT\.csv", filename)
        if match:
            number = int(match.group(1))
            letter = match.group(2) or ""   # letter suffix (A/B/...), may be None
            new_name = f"RWC_{coll}{number:03d}{letter}.csv"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {filename} → {new_name}")
        else:
            print(f"⏭ Skipped (no match): {filename}")
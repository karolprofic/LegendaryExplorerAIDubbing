from pathlib import Path
import os
import wave
from collections import defaultdict
from mutagen import File as MutagenFile
from openpyxl import Workbook

"""
This script scans a folder with exported audio files and generates a report.

It extracts actor names from filenames, calculates:
- number of audio files per actor
- total duration of their lines (in minutes)

Finally, it saves the results to an Excel file.
"""

# === SETTINGS (change only this) ===
AUDIO_FOLDER = Path(r"C:\Users\Karol\Desktop\me3_export")
OUTPUT_FILE = Path(r"C:\Users\Karol\Desktop\me3_voices_report.xlsx")
# ==================================

def parse_actor_name(file_path: Path):
    parts = file_path.name.split(",")
    if len(parts) < 2:
        return None
    return parts[1].strip()


def get_duration_seconds(file_path: Path):
    try:
        audio = MutagenFile(file_path)
        if audio and audio.info and hasattr(audio.info, "length"):
            return float(audio.info.length)
    except:
        pass

    # fallback for wav files
    if file_path.suffix.lower() == ".wav":
        try:
            with wave.open(str(file_path), "rb") as w:
                return w.getnframes() / w.getframerate()
        except:
            pass

    return None


def main():
    counts = defaultdict(int)
    durations = defaultdict(float)

    total_files = 0
    skipped = 0

    for root, _, files in os.walk(AUDIO_FOLDER):
        for file in files:
            path = Path(root) / file
            total_files += 1

            if total_files % 100 == 0:
                print(f"Processed: {total_files}")

            actor = parse_actor_name(path)
            if not actor:
                skipped += 1
                continue

            duration = get_duration_seconds(path)
            if duration is None:
                skipped += 1
                continue

            counts[actor] += 1
            durations[actor] += duration

    # === save to Excel ===
    wb = Workbook()
    ws = wb.active
    ws.title = "Voices"

    ws.append(["voice", "file count", "duration (minutes)"])

    for actor in sorted(counts.keys()):
        minutes = round(durations[actor] / 60, 2)
        ws.append([actor, counts[actor], minutes])

    wb.save(OUTPUT_FILE)

    # === log ===
    print("DONE")
    print(f"Files: {total_files}")
    print(f"Skipped: {skipped}")
    print(f"Unique voices: {len(counts)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
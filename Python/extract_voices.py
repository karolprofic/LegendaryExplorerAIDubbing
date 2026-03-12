import os
import glob

"""
This script generates a list of unique voice actors/characters for dubbing from exported .wav files.
"""

input_folder = "C:/Users/Karol/Desktop/me3_en_audio/"
output_file = "voice_list.txt"

voices = set()

# scan all .wav files
for file_path in glob.glob(os.path.join(input_folder, "*.wav")):
    filename = os.path.basename(file_path)
    parts = filename.split(",")
    if len(parts) >= 2:
        voice_name = parts[1]  # second column is the voice_name
        voices.add(voice_name)

# save sorted list
with open(output_file, "w", encoding="utf-8") as f:
    for v in sorted(voices):
        f.write(v + "\n")

print(f"Saved {len(voices)} unique voice names to {output_file}")
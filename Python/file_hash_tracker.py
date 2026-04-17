import os
import hashlib
import json

def file_hash(path, algo="sha256", chunk_size=1024 * 1024):
    h = hashlib.new(algo)

    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)

    return h.hexdigest()


def build_hash_db(folder, output_file):
    db = {}
    count = 0

    for root_dir, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root_dir, name)

            rel_path = os.path.relpath(path, folder)
            db[rel_path] = file_hash(path)
            count += 1
            if count % 10 == 0:
                print(f"\rProcessed: {count}", end="")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"\nSaved hashes for {len(db)} files → {output_file}")


# TODO: Not tested - be careful 
def compare_hashes(folder, hash_file):
    with open(hash_file, "r", encoding="utf-8") as f:
        old_db = json.load(f)

    count = 0
    new_db = {}
    changed = []
    added = []
    removed = set(old_db.keys())

    for root_dir, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root_dir, name)
            rel_path = os.path.relpath(path, folder)

            new_hash = file_hash(path)
            new_db[rel_path] = new_hash

            if rel_path not in old_db:
                added.append(rel_path)
            else:
                if old_db[rel_path] != new_hash:
                    changed.append(rel_path)

            removed.discard(rel_path)

            count += 1
            if count % 10 == 0:
                print(f"\rProcessed: {count}", end="")

    print("\n=== CHANGED FILES ===")
    for f in changed:
        print(f)

    print("\n=== NEW FILES ===")
    for f in added:
        print(f)

    print("\n=== REMOVED FILES ===")
    for f in removed:
        print(f)

    return changed, added, list(removed)

mel_folder = r"E:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition"
me3_folder = r"E:\SteamLibrary\steamapps\common\Mass Effect Legendary Edition\Game\ME3"

# build_hash_db(mel_folder, output_file="mel_hashes.json")
build_hash_db(me3_folder, output_file="me3_hashes.json")
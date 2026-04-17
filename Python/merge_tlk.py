import os
import glob
import xml.etree.ElementTree as ET

# The split must be done manually.
# It should take no more than 10 minutes.
# The XML parser has trouble loading comments.
input_folder_male = "me3_text_m"
input_folder_female = "me3_text_f"
output_file = "merged.xml"

def load_entries(folder, gender):
    entries = []

    for file in glob.glob(os.path.join(folder, "*.xml")):
        tree = ET.parse(file)
        root = tree.getroot()

        for elem in root.iter("String"):
            sid = elem.get("id")
            if sid is None:
                continue

            try:
                sid_int = int(sid)
            except ValueError:
                continue

            if sid_int < 0:
                continue

            entries.append({
                "id": sid,
                "gender": gender,
                "text": elem.text or ""
            })

    return entries


# load both folders
entries = []
entries.extend(load_entries(input_folder_male, "m"))
entries.extend(load_entries(input_folder_female, "f"))
entries.sort(key=lambda e: (int(e["id"]), e["gender"]))

# save in XML
root = ET.Element("tlkFile")
root.set("TLKToolVersion", "4.0.0.0")

for e in entries:
    sid = e["id"]
    gender = e["gender"]
    sound = f"{int(sid):08d}_{gender}_wav"

    elem = ET.SubElement(root, "String")
    elem.set("id", sid)
    elem.set("gender", gender)
    elem.set("idx", sid + "_" + gender)
    elem.set("sound", sound)
    elem.text = e["text"]

tree = ET.ElementTree(root)
ET.indent(tree, space="    ", level=0)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"Saved {len(entries)} entries to {output_file}")

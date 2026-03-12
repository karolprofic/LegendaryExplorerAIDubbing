import os
import glob
import xml.etree.ElementTree as ET

"""
This script merges multiple localization XML files from ME export into one file.
It performs the following operations:
1. Reads all XML files from the input_folder, default me3_text.
2. Extracts <String> entries, preserving Male/Female sections based on comments.
3. Removes duplicate entries by ID (ignores entries with ID < 0).
4. Adds a 'gender' attribute (m/f) depending on the section.
5. Adds a 'sound' attribute in the format 8-digit ID + '_' + gender + '_wav' (e.g., 00594406_m_wav).
6. Outputs a single, properly formatted XML file maintaining the section comments and indentation.
"""

input_folder = "me3_text"
output_file = "merged.xml"

strings = {}

for file in glob.glob(os.path.join(input_folder, "*.xml")):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(file, parser=parser)
    root = tree.getroot()

    gender = None

    for elem in root.iter():
        # komentarze
        if elem.tag is ET.Comment:
            text = elem.text.lower()

            if "male entries section begin" in text:
                gender = "m"
            elif "female entries section begin" in text:
                gender = "f"
            elif "section end" in text:
                gender = None

        elif elem.tag == "String":
            sid = elem.get("id")

            if sid is None:
                continue

            sid_int = int(sid)

            if sid_int < 0:
                continue

            text = elem.text

            if sid not in strings:
                strings[sid] = {
                    "text": text,
                    "gender": gender
                }

root = ET.Element("tlkFile")
root.set("TLKToolVersion", "4.0.0.0")

for sid in sorted(strings, key=lambda x: int(x)):
    s = strings[sid]

    gender = s["gender"] if s["gender"] else "u"
    sound = f"{int(sid):08d}_{gender}_wav"

    elem = ET.SubElement(root, "String")
    elem.set("id", sid)
    elem.set("gender", gender)
    elem.set("sound", sound)
    elem.text = s["text"]

tree = ET.ElementTree(root)
ET.indent(tree, space="    ", level=0)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"Saved {len(strings)} entries")
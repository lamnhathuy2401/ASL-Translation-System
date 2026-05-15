import os
import xml.etree.ElementTree as ET
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RAW_DIR = os.path.join(BASE_DIR, "raw_sigml")
EXTRACTED_DIR = os.path.join(BASE_DIR, "extracted")

os.makedirs(EXTRACTED_DIR, exist_ok=True)

def extract():
    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".sigml"):
            path = os.path.join(RAW_DIR, filename)

            tree = ET.parse(path)
            root = tree.getroot()

            ham = root.find(".//hamnosys")

            if ham is not None:
                data = {
                    "gloss": filename.replace(".sigml", "").upper(),
                    "hamnosys": ham.text.strip(),
                    "sigml_file": filename
                }

                out_file = os.path.join(EXTRACTED_DIR, filename.replace(".sigml", ".json"))

                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Extraction completed. Files saved to {EXTRACTED_DIR}")

extract()
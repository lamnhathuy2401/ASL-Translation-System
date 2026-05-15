import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

EXTRACTED_DIR = os.path.join(BASE_DIR, "extracted")
DICT_DIR = os.path.join(BASE_DIR, "dict")
OUTPUT_FILE = os.path.join(DICT_DIR, "hamnosys_dict.json")

os.makedirs(DICT_DIR, exist_ok=True)

def build_dict():
    dictionary = {}

    if not os.path.exists(EXTRACTED_DIR):
        raise Exception(f"❌ Extracted folder not found: {EXTRACTED_DIR}")

    files = os.listdir(EXTRACTED_DIR)

    if len(files) == 0:
        print("⚠️ No extracted files found!")
        return

    for filename in files:
        if filename.endswith(".json"):
            path = os.path.join(EXTRACTED_DIR, filename)

            with open(path, encoding="utf-8") as f:
                data = json.load(f)

                gloss = data.get("gloss")
                hamnosys = data.get("hamnosys")

                if gloss and hamnosys:
                    dictionary[gloss] = {
                        "hamnosys": hamnosys,
                        "sigml": data.get("sigml_file")
                    }

    if len(dictionary) == 0:
        print("⚠️ No valid entries found!")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"✅ Dictionary created: {OUTPUT_FILE}")
    print(f"📊 Total entries: {len(dictionary)}")


if __name__ == "__main__":
    build_dict()
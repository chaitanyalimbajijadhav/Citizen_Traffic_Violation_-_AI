from pathlib import Path

BASE = Path("dataset/traffic_violation/final")

# Final class mapping
# 0 = no_helmet
# 1 = triple_riding
# 2 = no_seatbelt
# 3 = mobile_phone
# 4 = wrong_side

CLASS_MAP = {
    "no_helmet": 0,
    "triple_riding": 1,
    "no_seatbelt": 2,
    "mobile_phone": 3,
    "wrong_side": 4,
}

# Source dataset folders already copied into final dataset
SOURCE_MARKERS = {
    "no_helmet": "no_helmet",
    "triple_riding": "triple_riding",
    "no_seatbelt": "no_seatbelt",
    "mobile_phone": "mobile_phone",
    "wrong_side": "wrong_side",
}

# This script uses filename patterns to identify the source class.
# Safer approach: process only labels whose filename exists in the
# corresponding source dataset.

DATASET_SOURCES = {
    "no_helmet": Path("dataset/traffic_violation/no_helmet"),
    "triple_riding": Path("dataset/traffic_violation/triple_riding"),
    "no_seatbelt": Path("dataset/traffic_violation/no_seatbelt"),
    "mobile_phone": Path("D:/TrafficDatasets/MobilePhone_Project"),
    "wrong_side": Path("D:/TrafficDatasets/WrongSide_Project"),
}


def get_source_label_names(source_dir):
    names = set()

    for split in ["train", "val", "test"]:
        label_dir = source_dir / split / "labels"

        if label_dir.exists():
            for label_file in label_dir.glob("*.txt"):
                names.add(label_file.name)

    return names


source_files = {}

for class_name, source_dir in DATASET_SOURCES.items():
    source_files[class_name] = get_source_label_names(source_dir)
    print(f"{class_name}: {len(source_files[class_name])} source labels found")


processed = 0
unmatched = 0
invalid = 0

for split in ["train", "val", "test"]:
    label_dir = BASE / split / "labels"

    if not label_dir.exists():
        continue

    for label_file in label_dir.glob("*.txt"):
        filename = label_file.name

        class_name = None

        for name, filenames in source_files.items():
            if filename in filenames:
                class_name = name
                break

        if class_name is None:
            unmatched += 1
            continue

        new_class_id = CLASS_MAP[class_name]

        lines = label_file.read_text(encoding="utf-8").splitlines()
        new_lines = []

        for line in lines:
            parts = line.strip().split()

            if not parts:
                continue

            if len(parts) < 5:
                invalid += 1
                continue

            # Replace original class ID with final unified class ID
            parts[0] = str(new_class_id)
            new_lines.append(" ".join(parts))

        label_file.write_text(
            "\n".join(new_lines) + ("\n" if new_lines else ""),
            encoding="utf-8"
        )

        processed += 1

print()
print("===== FINAL LABEL REMAPPING =====")
print(f"Processed labels : {processed}")
print(f"Unmatched labels : {unmatched}")
print(f"Invalid lines    : {invalid}")
print()
print("Final classes:")
print("0 = no_helmet")
print("1 = triple_riding")
print("2 = no_seatbelt")
print("3 = mobile_phone")
print("4 = wrong_side")
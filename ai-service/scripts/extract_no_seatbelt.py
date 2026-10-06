from pathlib import Path
import shutil

SOURCE = Path(r"D:\TrafficDatasets\Seatbelt detection.v4i.yolov11")
DEST = Path(r"dataset\traffic_violation\no_seatbelt")

SPLITS = {
    "train": "train",
    "valid": "val",
    "test": "test",
}


def extract_split(source_name, dest_name):
    source_images = SOURCE / source_name / "images"
    source_labels = SOURCE / source_name / "labels"

    dest_images = DEST / dest_name / "images"
    dest_labels = DEST / dest_name / "labels"

    dest_images.mkdir(parents=True, exist_ok=True)
    dest_labels.mkdir(parents=True, exist_ok=True)

    copied = 0

    for label_file in source_labels.glob("*.txt"):
        lines = label_file.read_text(encoding="utf-8").splitlines()

        no_seatbelt_lines = []

        for line in lines:
            parts = line.strip().split()

            if len(parts) >= 5 and parts[0] == "0":
                parts[0] = "0"
                no_seatbelt_lines.append(" ".join(parts))

        if not no_seatbelt_lines:
            continue

        image_file = None

        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
            candidate = source_images / (label_file.stem + ext)
            if candidate.exists():
                image_file = candidate
                break

        if image_file is None:
            print(f"WARNING: Image not found for {label_file.name}")
            continue

        shutil.copy2(image_file, dest_images / image_file.name)

        (dest_labels / label_file.name).write_text(
            "\n".join(no_seatbelt_lines) + "\n",
            encoding="utf-8"
        )

        copied += 1

    print(f"{dest_name}: {copied} images copied")
    return copied


total = 0

for source_name, dest_name in SPLITS.items():
    total += extract_split(source_name, dest_name)

print(f"\nTotal no-seatbelt images copied: {total}")
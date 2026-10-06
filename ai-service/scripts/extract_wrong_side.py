from pathlib import Path
import shutil

SOURCE = Path(r"D:\TrafficDatasets\Wrong Way Driving Detection.v1i.yolov11")
DEST = Path(r"D:\TrafficDatasets\WrongSide_Project")

SOURCE_CLASS_ID = "1"
TARGET_CLASS_ID = "0"

SPLITS = {
    "train": "train",
    "valid": "val",
    "test": "test",
}

IMAGE_EXTENSIONS = [
    ".jpg", ".jpeg", ".png",
    ".JPG", ".JPEG", ".PNG"
]


def find_image(images_dir, stem):
    for ext in IMAGE_EXTENSIONS:
        image = images_dir / (stem + ext)
        if image.exists():
            return image
    return None


def extract_split(source_split, dest_split):
    source_images = SOURCE / source_split / "images"
    source_labels = SOURCE / source_split / "labels"

    dest_images = DEST / dest_split / "images"
    dest_labels = DEST / dest_split / "labels"

    dest_images.mkdir(parents=True, exist_ok=True)
    dest_labels.mkdir(parents=True, exist_ok=True)

    copied = 0

    for label_file in source_labels.glob("*.txt"):

        lines = label_file.read_text(
            encoding="utf-8"
        ).splitlines()

        selected = []

        for line in lines:
            parts = line.strip().split()

            if len(parts) >= 5 and parts[0] == SOURCE_CLASS_ID:
                parts[0] = TARGET_CLASS_ID
                selected.append(" ".join(parts))

        if not selected:
            continue

        image_file = find_image(
            source_images,
            label_file.stem
        )

        if image_file is None:
            print(
                f"WARNING: Image not found: {label_file.name}"
            )
            continue

        shutil.copyfile(
            image_file,
            dest_images / image_file.name
        )

        (dest_labels / label_file.name).write_text(
            "\n".join(selected) + "\n",
            encoding="utf-8"
        )

        copied += 1

    print(f"{dest_split}: {copied} images copied")
    return copied


def main():
    print("Starting wrong_side extraction...\n")

    total = 0

    for source_split, dest_split in SPLITS.items():
        total += extract_split(
            source_split,
            dest_split
        )

    print(
        f"\nTotal wrong_side images copied: {total}"
    )

    print(f"Destination: {DEST}")


if __name__ == "__main__":
    main()
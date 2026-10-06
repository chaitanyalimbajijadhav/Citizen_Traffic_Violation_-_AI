from pathlib import Path
import shutil

# Source IMVT dataset
SOURCE = Path(r"D:\TrafficDatasets\IMVTDataset\IMVT_Project")

# Absolute destination path
DEST = Path(
    r"C:\Users\HP\OneDrive\Desktop\Member 2"
    r"\Citizen_Traffic_Violation_-_AI\ai-service"
    r"\dataset\traffic_violation\mobile_phone"
)

# Source split -> destination split
SPLITS = {
    "train": "train",
    "val": "val",
    "test": "test",
}

# IMVT class 5 = mobile_phone
SOURCE_CLASS_ID = "5"

# Unified dataset class 0 = mobile_phone
TARGET_CLASS_ID = "0"


def extract_split(split):
    source_images = SOURCE / split / "images"
    source_labels = SOURCE / split / "labels"

    dest_images = DEST / split / "images"
    dest_labels = DEST / split / "labels"

    # Create destination folders automatically
    dest_images.mkdir(parents=True, exist_ok=True)
    dest_labels.mkdir(parents=True, exist_ok=True)

    copied = 0

    for label_file in source_labels.glob("*.txt"):

        lines = label_file.read_text(
            encoding="utf-8"
        ).splitlines()

        mobile_phone_lines = []

        for line in lines:

            parts = line.strip().split()

            if len(parts) >= 5 and parts[0] == SOURCE_CLASS_ID:

                # Change source class 5 -> unified class 0
                parts[0] = TARGET_CLASS_ID

                mobile_phone_lines.append(
                    " ".join(parts)
                )

        # Skip images without mobile_phone
        if not mobile_phone_lines:
            continue

        # Find corresponding image
        image_file = None

        for ext in [
            ".jpg",
            ".jpeg",
            ".png",
            ".JPG",
            ".JPEG",
            ".PNG"
        ]:

            candidate = source_images / (
                label_file.stem + ext
            )

            if candidate.exists():
                image_file = candidate
                break

        if image_file is None:

            print(
                f"WARNING: Image not found: "
                f"{label_file.name}"
            )

            continue

        # Copy image
        shutil.copy2(
            image_file,
            dest_images / image_file.name
        )

        # Write only mobile_phone annotations
        destination_label = dest_labels / label_file.name

        destination_label.write_text(
            "\n".join(mobile_phone_lines) + "\n",
            encoding="utf-8"
        )

        copied += 1

    print(
        f"{split}: {copied} images copied"
    )

    return copied


def main():

    total = 0

    print("Starting mobile_phone extraction...\n")

    for split in SPLITS:

        total += extract_split(split)

    print(
        f"\nTotal mobile_phone images copied: {total}"
    )

    print("\nDestination:")
    print(DEST)


if __name__ == "__main__":
    main()
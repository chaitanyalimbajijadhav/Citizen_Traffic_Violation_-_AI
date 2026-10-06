from pathlib import Path
import shutil


SOURCE = Path(r"D:\TrafficDatasets\IMVTDataset\IMVT_Project")
DEST = Path(
    r"C:\Users\HP\OneDrive\Desktop\Member 2\Citizen_Traffic_Violation_-_AI"
    r"\ai-service\dataset\traffic_violation\no_helmet"
)

# IMVT dataset: class 6 = no_helmet
SOURCE_CLASS_ID = "6"

splits = ["train", "val", "test"]

images_copied = 0
labels_created = 0

for split in splits:

    source_images = SOURCE / split / "images"
    source_labels = SOURCE / split / "labels"

    dest_images = DEST / split / "images"
    dest_labels = DEST / split / "labels"

    dest_images.mkdir(parents=True, exist_ok=True)
    dest_labels.mkdir(parents=True, exist_ok=True)

    for label_file in source_labels.glob("*.txt"):

        selected_lines = []

        for line in label_file.read_text().splitlines():
            parts = line.strip().split()

            if len(parts) >= 5 and parts[0] == SOURCE_CLASS_ID:
                # Convert IMVT class 6 -> unified no_helmet class 0
                parts[0] = "0"
                selected_lines.append(" ".join(parts))

        if selected_lines:

            image_found = False

            for extension in [
                ".jpg", ".jpeg", ".png",
                ".JPG", ".JPEG", ".PNG"
            ]:
                image_file = source_images / (label_file.stem + extension)

                if image_file.exists():
                    shutil.copy2(
                        image_file,
                        dest_images / image_file.name
                    )
                    image_found = True
                    break

            if image_found:
                (dest_labels / label_file.name).write_text(
                    "\n".join(selected_lines) + "\n"
                )

                images_copied += 1
                labels_created += 1

print()
print("IMVT No Helmet extraction completed.")
print(f"Images copied : {images_copied}")
print(f"Labels created: {labels_created}")
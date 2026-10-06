from pathlib import Path


ROOT = Path(r"D:\TrafficDatasets\IMVTDataset\IMVT_Project")


def polygon_to_bbox(points):
    xs = points[0::2]
    ys = points[1::2]

    x_min = min(xs)
    y_min = min(ys)
    x_max = max(xs)
    y_max = max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return x_center, y_center, width, height


converted = 0
unchanged = 0
skipped = 0

for split in ["train", "val", "test"]:
    labels_dir = ROOT / split / "labels"

    for label_file in labels_dir.glob("*.txt"):
        new_lines = []

        for line in label_file.read_text().splitlines():
            parts = line.strip().split()

            if not parts:
                continue

            class_id = parts[0]
            values = list(map(float, parts[1:]))

            # Standard YOLO detection:
            # class + 4 coordinates
            if len(values) == 4:
                new_lines.append(line.strip())
                unchanged += 1

            # YOLO segmentation polygon:
            # class + multiple x,y coordinate pairs
            elif len(values) >= 6 and len(values) % 2 == 0:
                bbox = polygon_to_bbox(values)

                new_line = (
                    f"{class_id} "
                    f"{bbox[0]:.6f} "
                    f"{bbox[1]:.6f} "
                    f"{bbox[2]:.6f} "
                    f"{bbox[3]:.6f}"
                )

                new_lines.append(new_line)
                converted += 1

            else:
                print(f"SKIPPED: {label_file}")
                skipped += 1

        label_file.write_text("\n".join(new_lines) + "\n")

print()
print("Conversion completed.")
print(f"Polygon annotations converted : {converted}")
print(f"Bounding boxes unchanged      : {unchanged}")
print(f"Invalid annotations skipped   : {skipped}")
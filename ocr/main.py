import json
import sys

from ocr_service import process_plate_image


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else ""
    result = process_plate_image(image_path)
    print(json.dumps(result, indent=2))

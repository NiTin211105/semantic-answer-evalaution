"""
OCR Module — Semantic AI Based Short Answer Evaluation
"""

import os

reader = None


def get_reader():
    global reader

    if reader is None:
        import easyocr
        reader = easyocr.Reader(["en"], gpu=False)

    return reader


def extract_text(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    ocr_reader = get_reader()

    result = ocr_reader.readtext(image_path, detail=0)

    return " ".join(result)


if _name_ == "_main_":
    test_images = ["sample_images/2_cleaned.jpg"]

    for img in test_images:
        try:
            text = extract_text(img)
            print(f"\n===== {img} =====")
            print(text)
        except FileNotFoundError as e:
            print(e)

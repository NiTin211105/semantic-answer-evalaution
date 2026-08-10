"""
OCR Module — Semantic AI Based Short Answer Evaluation
Extracts text from handwritten/typed answer images using EasyOCR.
"""

import os
import easyocr

reader = None


def get_reader():
    global reader

    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)

    return reader


def extract_text(image_path):
    """
    Takes an image file path, returns the extracted text as a string.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    ocr_reader = get_reader()

    result = ocr_reader.readtext(image_path, detail=0)

    extracted_text = " ".join(result)

    return extracted_text


# Quick test when running this file directly
if _name_ == "_main_":
    test_images = ["sample_images/2_cleaned.jpg"]

    for img in test_images:
        try:
            text = extract_text(img)
            print(f"\n===== {img} =====")
            print(text)
        except FileNotFoundError as e:
            print(e)

"""
OCR Module — Semantic AI Based Short Answer Evaluation
Extracts text from handwritten/typed answer images using EasyOCR.
"""

import easyocr
import os

# Initialize the reader once (loads the AI model)
reader = easyocr.Reader(['en'])


def extract_text(image_path):
    """
    Takes an image file path, returns the extracted text as a string.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    result = reader.readtext(image_path, detail=0)
    extracted_text = " ".join(result)
    return extracted_text


# Quick test when running this file directly
if __name__ == "__main__":
    test_images = ["sample_images/2_cleaned.jpg"]

    for img in test_images:
        try:
            text = extract_text(img)
            print(f"\n===== {img} =====")
            print(text)
        except FileNotFoundError as e:
            print(e)
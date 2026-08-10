"""
Quick Diagnostic — compares OCR accuracy on the RAW image vs the PREPROCESSED image,
to check if preprocessing is helping or hurting on well-lit, clean photos.
"""

from ocr_module import extract_text
from preprocessing import preprocess_image

# CHANGE THIS to your actual clean photo filename
image_path = "sample_images/q1.jpg"

print("--- OCR on RAW (unprocessed) image ---")
raw_direct = extract_text(image_path)
print(raw_direct)

print("\n--- OCR on PREPROCESSED image ---")
cleaned_path = "sample_images/q1_final.jpg"
preprocess_image(image_path, cleaned_path)
raw_preprocessed = extract_text(cleaned_path)
print(raw_preprocessed)
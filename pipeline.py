import os
from preprocessing import preprocess_image
from ocr_module import extract_text
from text_cleaning import clean_text


def run_pipeline(image_path):
    cleaned_image_path = image_path.replace(".jpeg", "_cleaned.jpg").replace(".jpg", "_cleaned.jpg").replace(".png", "_cleaned.jpg")
    preprocess_image(image_path, cleaned_image_path)

    raw_text = extract_text(cleaned_image_path)

    final_text = clean_text(raw_text)

    return raw_text, final_text


if __name__ == "__main__":
    test_images = [
        "sample_images/1.jpeg",
        "sample_images/2.jpeg",
        "sample_images/3.jpeg",
    ]

    for img_path in test_images:
        if not os.path.exists(img_path):
            print(f"⚠️ Skipping, not found: {img_path}")
            continue

        print(f"\n===== PROCESSING: {img_path} =====")
        raw_text, final_text = run_pipeline(img_path)

        print("--- Raw OCR text ---")
        print(raw_text)
        print("--- Final cleaned text ---")
        print(final_text)
        print("=" * 50)
"""
Preprocessing Module — Semantic AI Based Short Answer Evaluation
Cleans up an answer sheet image before OCR reads it:
- Converts to grayscale
- Increases contrast
- Removes noise
Saves the cleaned image so you can visually check the result.
"""

import cv2
import os


def preprocess_image(image_path, output_path="preprocessed_output.jpg"):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)

    denoised = cv2.fastNlMeansDenoising(contrast_enhanced, h=10)

    cv2.imwrite(output_path, denoised)
    return output_path


if __name__ == "__main__":
    test_image = "sample_images/3.jpeg"
    result_path = preprocess_image(test_image, "sample_images/3_cleaned.jpg")
    print(f"Cleaned image saved at: {result_path}")
    print("Open it and compare visually with the original.")
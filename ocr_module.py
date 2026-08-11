"""
OCR Module — Semantic AI Based Short Answer Evaluation
"""
import os
import sys
import types

# Vercel packaging workaround for scikit-image lazy loading
try:
    import lazy_loader
    original_attach_stub = lazy_loader.attach_stub

    def safe_attach_stub(package_name, filename, *args, **kwargs):
        try:
            return original_attach_stub(package_name, filename, *args, **kwargs)
        except ValueError as e:
            if "non-existent stub" in str(e):
                return {}, lambda: [], []
            raise

    lazy_loader.attach_stub = safe_attach_stub
except Exception:
    pass

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


if __name__ == "__main__":
    test_images = ["sample_images/2_cleaned.jpg"]

    for img in test_images:
        try:
            text = extract_text(img)
            print(f"\n===== {img} =====")
            print(text)
        except FileNotFoundError as e:
            print(e)

"""
OCR Module — Semantic AI Based Short Answer Evaluation
"""
import os
import sys
import types

# Vercel packaging workaround for scikit-image lazy loading
try:
    
    original_attach_stub = lazy_loader.attach_stub

    def safe_attach_stub(package_name, filename, *args, **kwargs):
        try:
            return original_attach_stub(package_name, filename, *args, **kwargs)
        except ValueError as e:
            if "non-existent stub" in str(e):
                return {}, lambda: [], []
            raise

except Exception:
    pass

reader = None

def get_reader():
    global reader
if reader is None:
    import sys
    import types
    import cv2

    # EasyOCR imports skimage.io only for reading the image.
    # Use OpenCV instead so Vercel does not need skimage's .pyi stubs.
    if "skimage" not in sys.modules:
        skimage_stub = types.ModuleType("skimage")
        skimage_stub._path_ = []

        io_stub = types.ModuleType("skimage.io")

        def imread(path):
            image = cv2.imread(path)
            if image is None:
                raise ValueError(f"Could not read image: {path}")
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        io_stub.imread = imread
        skimage_stub.io = io_stub

        sys.modules["skimage"] = skimage_stub
        sys.modules["skimage.io"] = io_stub

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

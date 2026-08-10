"""
OCR Quality Checker — Semantic AI Based Short Answer Evaluation
Detects likely OCR failures (garbled text, background noise, etc.) BEFORE grading,
so we don't silently give a student 0 marks due to a bad photo instead of a bad answer.
"""

import re


def check_ocr_quality(cleaned_text):
    """
    Runs some simple heuristic checks on OCR output to flag likely garbage text.
    Returns a dictionary: {"is_likely_valid": bool, "reason": str, "warnings": list}
    """
    warnings = []

    if not cleaned_text or not cleaned_text.strip():
        return {
            "is_likely_valid": False,
            "reason": "No text was extracted from the image at all.",
            "warnings": ["Empty OCR output — check if the image is clear and contains visible text."]
        }

    words = cleaned_text.split()
    total_words = len(words)

    if total_words < 3:
        return {
            "is_likely_valid": False,
            "reason": "Extracted text is too short to be a real answer.",
            "warnings": [f"Only {total_words} word(s) detected."]
        }

    # HEURISTIC 1: too many very short "words" (1-2 characters) often means
    # OCR broke words apart into garbage fragments (common with background noise)
    short_words = [w for w in words if len(w) <= 2]
    short_word_ratio = len(short_words) / total_words

    if short_word_ratio > 0.4:
        warnings.append(
            f"{len(short_words)}/{total_words} words are very short (1-2 characters) — "
            f"this often means OCR misread the image (background clutter, blur, or bad lighting)."
        )

    # HEURISTIC 2: too many numbers/symbols mixed into what should be prose text
    # (a few numbers are fine, e.g. math answers, but a LOT suggests garbage)
    numeric_or_symbol_words = [w for w in words if re.match(r'^[\d\W]+$', w)]
    numeric_ratio = len(numeric_or_symbol_words) / total_words

    if numeric_ratio > 0.3:
        warnings.append(
            f"{len(numeric_or_symbol_words)}/{total_words} words are just numbers/symbols — "
            f"possible OCR noise from background text or unclear handwriting."
        )

    # Decide overall validity based on how many warnings triggered
    is_likely_valid = len(warnings) == 0

    reason = "Text looks reasonable." if is_likely_valid else "Text quality looks questionable — see warnings."

    return {
        "is_likely_valid": is_likely_valid,
        "reason": reason,
        "warnings": warnings
    }


# Quick test when running this file directly
if __name__ == "__main__":
    # Test 1: Good, clean text (should pass)
    good_text = "plants use sunlight as an energy source carbon dioxide and water are raw materials"
    result1 = check_ocr_quality(good_text)
    print("TEST 1 (good text):")
    print(result1)
    print()

    # Test 2: Garbled text like what we saw with background clutter (should fail)
    garbled_text = "3 ftu 57 7 ao 37 4 3 7d 81 3 4 roq 4 1 te dp 8 4 on je st 3 4 9 78 6"
    result2 = check_ocr_quality(garbled_text)
    print("TEST 2 (garbled text):")
    print(result2)
    print()

    # Test 3: Empty text (should fail)
    result3 = check_ocr_quality("")
    print("TEST 3 (empty text):")
    print(result3)
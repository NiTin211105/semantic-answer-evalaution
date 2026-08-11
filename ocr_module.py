"""
OCR Module — Semantic AI Based Short Answer Evaluation
Uses Gemini Vision for OCR.
"""

import os
import base64
import json
import urllib.request
import urllib.error


def extract_text(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    extension = os.path.splitext(image_path)[1].lower()

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp"
    }

    mime_type = mime_types.get(extension, "image/jpeg")

    prompt = """
Extract ONLY the student's written answer from this image.

The image may contain handwritten or typed text.

Return ONLY the extracted answer text.
Do not explain the answer.
Do not add comments.
Do not use markdown.
Preserve the wording and meaning as accurately as possible.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_data
                        }
                    }
                ]
            }
        ]
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.1-flash-lite:generateContent"
        f"?key={api_key}"
    )

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini API HTTP {e.code}: {error_body}"
        )

    except Exception as e:
        raise RuntimeError(f"OCR API request failed: {e}")

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Unexpected OCR API response: {result}")

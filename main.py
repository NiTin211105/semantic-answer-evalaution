"""
Master Pipeline — Semantic AI Based Short Answer Evaluation
The complete flow: raw answer image -> preprocessed image -> OCR text ->
cleaned text -> key point matching -> marks -> feedback.
"""

import os

from preprocessing import preprocess_image
from ocr_module import extract_text
from text_cleaning import clean_text
from answer_matching_v2 import check_keypoints_coverage
from marks_calculator import calculate_marks
from feedback_generator import generate_feedback
from question_loader import load_questions, get_question_by_id
from ocr_quality_check import check_ocr_quality


def evaluate_answer(image_path, question_id):
    """
    The full pipeline. Takes a path to a student's answer image and the
    question_id it's answering. Returns a complete result dictionary.
    """

    questions = load_questions()
    question = get_question_by_id(questions, question_id)

    if question is None:
        raise ValueError(f"No question found with id: {question_id}")

    cleaned_image_path = os.path.splitext(image_path)[0] + "_cleaned.jpg"

    preprocess_image(image_path, cleaned_image_path)

    raw_ocr_text = extract_text(cleaned_image_path)

    cleaned_text = clean_text(raw_ocr_text)

    quality_check = check_ocr_quality(cleaned_text)

    coverage_results = check_keypoints_coverage(
        cleaned_text,
        question["key_points"]
    )

    marks_result = calculate_marks(
        coverage_results,
        question["key_points"],
        question["total_marks"]
    )

    feedback = generate_feedback(
        coverage_results,
        marks_result
    )

    return {
        "question_text": question["question_text"],
        "raw_ocr_text": raw_ocr_text,
        "cleaned_text": cleaned_text,
        "quality_check": quality_check,
        "coverage_results": coverage_results,
        "marks_result": marks_result,
        "feedback": feedback
    }


def print_full_report(result):
    print("=" * 60)
    print(f"QUESTION: {result['question_text']}")
    print("=" * 60)

    print("\n--- Raw OCR Output ---")
    print(result["raw_ocr_text"])

    print("\n--- Cleaned Text ---")
    print(result["cleaned_text"])

    if not result["quality_check"]["is_likely_valid"]:
        print("\nOCR QUALITY WARNING")
        print(result["quality_check"]["reason"])

        for w in result["quality_check"]["warnings"]:
            print(f"  - {w}")

    print("\n--- Key Point Coverage ---")

    for r in result["coverage_results"]:
        status = "COVERED" if r["covered"] else "MISSING"
        print(
            f"[{r['point_id']}] "
            f"{r['point_text']} "
            f"(score: {r['score']}) -> {status}"
        )

    print("\n--- Feedback ---")
    print(result["feedback"])

    print("=" * 60)


if _name_ == "_main_":
    test_image = "sample_images/q1_demo.jpg"
    test_question_id = "Q1"

    if not os.path.exists(test_image):
        print(f"Test image not found: {test_image}")
    else:
        result = evaluate_answer(test_image, test_question_id)
        print_full_report(result)

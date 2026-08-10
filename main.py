"""
Master Pipeline — Semantic AI Based Short Answer Evaluation
The complete flow: raw answer image -> preprocessed image -> OCR text ->
cleaned text -> key point matching -> marks -> feedback.

This is the main entry point for the whole project.
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
    # STEP 0: Load the question and its key points
    questions = load_questions()
    question = get_question_by_id(questions, question_id)
    if question is None:
        raise ValueError(f"No question found with id: {question_id}")

    # STEP 1: Preprocess the image (grayscale, contrast, denoise)
    cleaned_image_path = os.path.splitext(image_path)[0] + "_cleaned.jpg"
    preprocess_image(image_path, cleaned_image_path)

    # STEP 2: Run OCR to extract raw text
    raw_ocr_text = extract_text(cleaned_image_path)

    # STEP 3: Clean the OCR text
    cleaned_text = clean_text(raw_ocr_text)

    # STEP 3.5: Check OCR quality BEFORE grading — catches bad photos, not bad answers
    quality_check = check_ocr_quality(cleaned_text)

    # STEP 4: Check key point coverage using semantic similarity
    coverage_results = check_keypoints_coverage(cleaned_text, question["key_points"])

    # STEP 5: Calculate marks
    marks_result = calculate_marks(coverage_results, question["key_points"], question["total_marks"])

    # STEP 6: Generate feedback
    feedback = generate_feedback(coverage_results, marks_result)

    # Return everything, in case we want to inspect intermediate steps too
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
    """
    Nicely prints out a full evaluation report to the console.
    """
    print("=" * 60)
    print(f"QUESTION: {result['question_text']}")
    print("=" * 60)

    print("\n--- Raw OCR Output ---")
    print(result["raw_ocr_text"])

    print("\n--- Cleaned Text (used for evaluation) ---")
    print(result["cleaned_text"])

    if not result["quality_check"]["is_likely_valid"]:
        print("\n⚠️  OCR QUALITY WARNING ⚠️")
        print(f"  {result['quality_check']['reason']}")
        for w in result["quality_check"]["warnings"]:
            print(f"  - {w}")
        print("  --> Marks below may be UNRELIABLE. Consider retaking the photo.")

    print("\n--- Key Point Coverage ---")
    for r in result["coverage_results"]:
        status = "✅" if r["covered"] else "❌"
        print(f"  {status} [{r['point_id']}] {r['point_text']} (score: {r['score']})")

    print("\n--- Feedback ---")
    print(result["feedback"])
    print("=" * 60)


# Quick test when running this file directly
if __name__ == "__main__":
    # Change these to match an actual image + question in your project
    test_image = "sample_images/q1_demo.jpg"
    test_question_id = "Q1"

    if not os.path.exists(test_image):
        print(f"⚠️ Test image not found: {test_image}")
    else:
        result = evaluate_answer(test_image, test_question_id)
        print_full_report(result)
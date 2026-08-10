"""
Batch Testing Module — Semantic AI Based Short Answer Evaluation
Runs multiple real handwritten answer images through the full pipeline
and prints a summary table, so we can review overall system performance
across several questions and handwriting styles at once.
"""

import os
from main import evaluate_answer, print_full_report

# EDIT THIS LIST: add your real handwritten test images here
# Each entry needs: the image filename (inside sample_images/) and the question_id it answers
BATCH_TEST_CASES = [
    {"image": "sample_images/q1.jpg", "question_id": "Q1", "label": "Good answer"},
    {"image": "sample_images/q2.jpg", "question_id": "Q2", "label": "Partial answer"},
    {"image": "sample_images/q3.jpg", "question_id": "Q3", "label": "Weak/bad answer"},
]


def run_batch_test():
    summary_rows = []

    for case in BATCH_TEST_CASES:
        image_path = case["image"]
        question_id = case["question_id"]

        if not os.path.exists(image_path):
            print(f"⚠️ Skipping, image not found: {image_path}")
            continue

        print(f"\n\n########## Processing: {image_path} | Question {question_id} | {case.get('label','')} ##########")

        try:
            result = evaluate_answer(image_path, question_id)
            print_full_report(result)

            summary_rows.append({
                "image": image_path,
                "question": question_id,
                "label": case.get("label", ""),
                "marks": f"{result['marks_result']['awarded_marks']} / {result['marks_result']['total_marks']}",
                "points": f"{result['marks_result']['points_covered']} / {result['marks_result']['points_total']}"
            })

        except Exception as e:
            print(f"❌ ERROR processing {image_path}: {e}")
            summary_rows.append({
                "image": image_path,
                "question": question_id,
                "label": case.get("label", ""),
                "marks": "ERROR",
                "points": "ERROR"
            })

    # Print a final summary table
    print("\n\n" + "=" * 60)
    print("BATCH TEST SUMMARY")
    print("=" * 60)
    for row in summary_rows:
        print(f"{row['image']:22} | Q:{row['question']:4} | {row['label']:15} | Marks: {row['marks']:8} | Points: {row['points']}")


if __name__ == "__main__":
    run_batch_test()
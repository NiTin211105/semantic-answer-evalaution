"""
End-to-End Evaluation Test — Semantic AI Based Short Answer Evaluation
Runs the full flow: student answer -> key point matching -> marks calculation,
across several sample answers, so we can sanity-check the whole system together.
"""

from question_loader import load_questions, get_question_by_id
from answer_matching_v2 import check_keypoints_coverage
from marks_calculator import calculate_marks

# Sample answers of varying quality across different questions
TEST_ANSWERS = [
    {
        "question_id": "Q1",
        "label": "Strong answer",
        "answer": (
            "Photosynthesis is how plants make their food. "
            "They use sunlight as their main source of energy. "
            "Water and carbon dioxide are taken in by the plant. "
            "This whole process takes place inside the chloroplasts, "
            "producing glucose and oxygen as the final result."
        ),
        "expected_human_marks": "close to full marks (4/4)"
    },
    {
        "question_id": "Q1",
        "label": "Average answer",
        "answer": "Plants use sunlight to make their own food through photosynthesis.",
        "expected_human_marks": "partial marks (around 1-2/4)"
    },
    {
        "question_id": "Q6",
        "label": "Strong answer",
        "answer": (
            "An acid releases hydrogen ions when dissolved in water and has a pH below 7. "
            "A base releases hydroxide ions and has a pH above 7. "
            "Acids turn blue litmus paper red, while bases turn red litmus paper blue."
        ),
        "expected_human_marks": "close to full marks (3/3)"
    },
    {
        "question_id": "Q6",
        "label": "Weak/blank-ish answer",
        "answer": "acid and base are chemicals",
        "expected_human_marks": "very low or zero marks"
    },
]


def run_full_evaluation():
    questions = load_questions()

    for case in TEST_ANSWERS:
        question = get_question_by_id(questions, case["question_id"])

        coverage_results = check_keypoints_coverage(case["answer"], question["key_points"])
        marks_result = calculate_marks(coverage_results, question["key_points"], question["total_marks"])

        print(f"\n{'='*60}")
        print(f"Question: {question['question_text']}")
        print(f"Test case: {case['label']}")
        print(f"Answer: {case['answer']}")
        print(f"{'-'*60}")

        for r in coverage_results:
            status = "✅" if r["covered"] else "❌"
            print(f"  {status} [{r['point_id']}] {r['point_text']} (score: {r['score']})")

        print(f"\n  MARKS AWARDED: {marks_result['awarded_marks']} / {marks_result['total_marks']}")
        print(f"  Expected (human judgement guess): {case['expected_human_marks']}")


if __name__ == "__main__":
    run_full_evaluation()
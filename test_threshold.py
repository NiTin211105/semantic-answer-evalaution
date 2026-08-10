"""
Threshold Testing Module — Semantic AI Based Short Answer Evaluation
Tests the key-point matching logic against several sample answers of varying quality,
to help decide if the similarity threshold needs adjusting.
"""

from question_loader import load_questions, get_question_by_id
from answer_matching_v2 import check_keypoints_coverage

# A small set of test answers with varying quality, for different questions
TEST_CASES = [
    {
        "question_id": "Q1",
        "label": "GOOD answer (covers most points)",
        "answer": (
            "plants take in sunlight and use it as energy they also use water and "
            "carbon dioxide this process happens in the chloroplasts and produces "
            "glucose and oxygen"
        )
    },
    {
        "question_id": "Q1",
        "label": "PARTIAL answer (covers only 1-2 points)",
        "answer": "plants use sunlight to make food"
    },
    {
        "question_id": "Q1",
        "label": "BAD answer (completely off-topic)",
        "answer": "newton's law says an object at rest stays at rest unless a force acts on it"
    },
    {
        "question_id": "Q5",
        "label": "GOOD answer for Ohm's Law",
        "answer": "voltage is directly proportional to current when temperature is constant, v equals i times r, where r is resistance"
    },
    {
        "question_id": "Q5",
        "label": "PARTIAL answer for Ohm's Law",
        "answer": "voltage and current are related by a formula"
    },
]


def run_threshold_tests():
    questions = load_questions()

    for case in TEST_CASES:
        question = get_question_by_id(questions, case["question_id"])

        print(f"\n{'='*60}")
        print(f"Question: {question['question_text']}")
        print(f"Test case: {case['label']}")
        print(f"Answer: {case['answer']}")
        print(f"{'-'*60}")

        results = check_keypoints_coverage(case["answer"], question["key_points"])

        covered_count = 0
        for r in results:
            status = "✅ COVERED" if r["covered"] else "❌ MISSING"
            print(f"  [{r['point_id']}] Score: {r['score']}  -->  {status}")
            if r["covered"]:
                covered_count += 1

        print(f"Result: {covered_count} / {len(results)} points covered")


if __name__ == "__main__":
    run_threshold_tests()
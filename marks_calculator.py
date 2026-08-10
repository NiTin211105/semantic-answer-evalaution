"""
Marks Calculation Module — Semantic AI Based Short Answer Evaluation
Converts key-point coverage results into an actual numeric score for a question.
"""


def calculate_marks(coverage_results, key_points, total_marks):
    """
    Takes the coverage results (from answer_matching_v2), the original key_points
    list (for weights), and total_marks for the question.

    Returns a dictionary with the awarded marks and a breakdown.
    """
    # Build a lookup of point_id -> weight, from the original key_points list
    weight_lookup = {p["point_id"]: p["weight"] for p in key_points}

    total_weight = sum(weight_lookup.values())
    covered_weight = 0

    for r in coverage_results:
        if r["covered"]:
            covered_weight += weight_lookup[r["point_id"]]

    # Avoid division by zero (shouldn't normally happen, but just in case)
    if total_weight == 0:
        awarded_marks = 0
    else:
        awarded_marks = (covered_weight / total_weight) * total_marks

    return {
        "awarded_marks": round(awarded_marks, 2),
        "total_marks": total_marks,
        "covered_weight": covered_weight,
        "total_weight": total_weight,
        "points_covered": sum(1 for r in coverage_results if r["covered"]),
        "points_total": len(coverage_results)
    }


# Quick test when running this file directly
if __name__ == "__main__":
    from question_loader import load_questions, get_question_by_id
    from answer_matching_v2 import check_keypoints_coverage

    questions = load_questions()
    question = get_question_by_id(questions, "Q1")

    student_answer = (
        "Photosynthesis is how plants make their food. "
        "They use sunlight as their main source of energy. "
        "Water and carbon dioxide are taken in by the plant. "
        "This whole process takes place inside the chloroplasts."
    )

    coverage_results = check_keypoints_coverage(student_answer, question["key_points"])

    marks_result = calculate_marks(
        coverage_results,
        question["key_points"],
        question["total_marks"]
    )

    print(f"Question: {question['question_text']}")
    print(f"Student answer: {student_answer}\n")

    print("----- KEY POINT COVERAGE -----")
    for r in coverage_results:
        status = "✅ COVERED" if r["covered"] else "❌ MISSING"
        print(f"[{r['point_id']}] {r['point_text']} --> {status} (score: {r['score']})")

    print("\n----- MARKS AWARDED -----")
    print(f"Points covered: {marks_result['points_covered']} / {marks_result['points_total']}")
    print(f"Marks: {marks_result['awarded_marks']} / {marks_result['total_marks']}")
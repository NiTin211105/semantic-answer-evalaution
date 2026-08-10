"""
Feedback Generation Module — Semantic AI Based Short Answer Evaluation
Converts key-point coverage results into plain-language feedback for the student.
"""


def generate_feedback(coverage_results, marks_result):
    """
    Takes the coverage results and marks result, returns a readable feedback string.
    """
    covered_points = [r for r in coverage_results if r["covered"]]
    missing_points = [r for r in coverage_results if not r["covered"]]

    lines = []

    # STEP 1: Opening line based on overall performance
    percentage = 0
    if marks_result["total_marks"] > 0:
        percentage = (marks_result["awarded_marks"] / marks_result["total_marks"]) * 100

    if percentage >= 90:
        opening = "Excellent answer! You covered nearly all the key points."
    elif percentage >= 70:
        opening = "Good answer. You covered most of the key points, with a few gaps."
    elif percentage >= 40:
        opening = "Partial answer. You covered some key points, but several are missing."
    elif percentage > 0:
        opening = "Your answer is missing most of the key points expected here."
    else:
        opening = "Your answer did not cover any of the key points expected for this question."

    lines.append(opening)
    lines.append("")

    # STEP 2: What was covered
    if covered_points:
        lines.append("What you got right:")
        for p in covered_points:
            lines.append(f"  ✓ {p['point_text']}")
        lines.append("")

    # STEP 3: What was missing
    if missing_points:
        lines.append("What you missed:")
        for p in missing_points:
            lines.append(f"  ✗ {p['point_text']}")
        lines.append("")

    # STEP 4: Closing summary line
    lines.append(
        f"Marks awarded: {marks_result['awarded_marks']} / {marks_result['total_marks']} "
        f"({marks_result['points_covered']}/{marks_result['points_total']} key points covered)"
    )

    return "\n".join(lines)


# Quick test when running this file directly
if __name__ == "__main__":
    from question_loader import load_questions, get_question_by_id
    from answer_matching_v2 import check_keypoints_coverage
    from marks_calculator import calculate_marks

    questions = load_questions()
    question = get_question_by_id(questions, "Q1")

    student_answer = "Plants use sunlight to make their own food through photosynthesis."

    coverage_results = check_keypoints_coverage(student_answer, question["key_points"])
    marks_result = calculate_marks(coverage_results, question["key_points"], question["total_marks"])

    feedback = generate_feedback(coverage_results, marks_result)

    print(f"Question: {question['question_text']}")
    print(f"Student answer: {student_answer}\n")
    print("----- FEEDBACK -----")
    print(feedback)
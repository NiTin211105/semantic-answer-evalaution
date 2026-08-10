"""
Answer Matching Module — Semantic AI Based Short Answer Evaluation
Checks which key points are covered in a student's answer using semantic similarity.
"""

from similarity_matching import get_similarity

# If similarity score is above this, we consider the point "covered"
SIMILARITY_THRESHOLD = 0.5


def check_keypoints_coverage(student_answer, key_points):
    """
    Takes the student's full answer text and a list of key points (from question_loader).
    Returns a list of results showing which points were covered and their scores.
    """
    results = []

    for point in key_points:
        point_text = point["point_text"]
        score = get_similarity(student_answer, point_text)
        covered = score >= SIMILARITY_THRESHOLD

        results.append({
            "point_id": point["point_id"],
            "point_text": point_text,
            "score": round(score, 3),
            "covered": covered
        })

    return results


# Quick test when running this file directly
if __name__ == "__main__":
    from question_loader import load_questions, get_question_by_id

    # Load your questions and pick one to test with
    questions = load_questions()
    question = get_question_by_id(questions, "Q1")  # photosynthesis question

    # A sample student answer (imagine this came from OCR + cleaning)
    student_answer = (
        "plants take in sunlight and use it as energy they also use water and "
        "carbon dioxide this process happens in the leaves and produces oxygen"
    )

    print(f"Question: {question['question_text']}\n")
    print(f"Student answer: {student_answer}\n")

    results = check_keypoints_coverage(student_answer, question["key_points"])

    print("----- KEY POINT COVERAGE -----")
    covered_count = 0
    for r in results:
        status = "✅ COVERED" if r["covered"] else "❌ MISSING"
        print(f"[{r['point_id']}] {r['point_text']}")
        print(f"    Score: {r['score']}  -->  {status}")
        if r["covered"]:
            covered_count += 1

    print(f"\nTotal points covered: {covered_count} / {len(results)}")
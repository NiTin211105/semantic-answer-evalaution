"""
Question Data Loader — Semantic AI Based Short Answer Evaluation
Loads questions and their key points from the JSON file.
"""

import json


def load_questions(json_path="sample_data/questions_keypoints.json"):
    """
    Loads the questions JSON file and returns the data as a Python dictionary.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["questions"]


def get_question_by_id(questions, question_id):
    """
    Finds and returns one specific question (with its key points) by its ID.
    """
    for q in questions:
        if q["question_id"] == question_id:
            return q
    return None


# Quick test when running this file directly
if __name__ == "__main__":
    questions = load_questions()

    print(f"Loaded {len(questions)} questions.\n")

    for q in questions:
        print(f"Question ID: {q['question_id']}")
        print(f"Question: {q['question_text']}")
        print(f"Total marks: {q['total_marks']}")
        print("Key points:")
        for point in q["key_points"]:
            print(f"  - [{point['point_id']}] {point['point_text']} (weight: {point['weight']})")
        print("-" * 50)
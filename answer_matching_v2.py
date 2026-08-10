"""
Answer Matching Module (Refined) — Semantic AI Based Short Answer Evaluation
Improvement over Day 9 version:
- Splits student answer into sentences, checks each sentence against each key point,
  and takes the BEST match (instead of comparing the whole answer as one blob).
- Handles edge cases: empty answers, very short/junk answers.
"""

import re
from similarity_matching import get_similarity

SIMILARITY_THRESHOLD = 0.65

# If the student answer has fewer than this many characters, treat it as "too short to grade"
MIN_ANSWER_LENGTH = 5


def split_into_word_chunks(text, chunk_size=10, overlap=5):
    """
    Fallback splitter: breaks text into overlapping chunks of `chunk_size` words,
    sliding forward by (chunk_size - overlap) words each time.
    Used when the text has no punctuation at all to split on (common with
    OCR output or students who write run-on sentences without periods/commas).
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text.strip()]

    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break

    return chunks


def split_into_sentences(text):
    """
    Splits a block of text into individual sentences/chunks for comparison.
    Tries punctuation-based splitting first (., !, ?, newlines, commas).
    If that produces only ONE piece (i.e. no real punctuation was found) and
    the text is long, falls back to overlapping word-chunking instead.
    """
    # Try splitting on sentence-ending punctuation, newlines, OR commas
    raw_pieces = re.split(r'[.!?\n,]+', text)
    sentences = [s.strip() for s in raw_pieces if s.strip()]

    if not sentences:
        return [text.strip()] if text.strip() else []

    # If punctuation splitting only found ONE big chunk, and it's a long run-on
    # answer, use the word-chunking fallback instead for better granularity
    if len(sentences) == 1 and len(sentences[0].split()) > 12:
        return split_into_word_chunks(sentences[0])

    return sentences


def check_keypoints_coverage(student_answer, key_points):
    """
    Takes the student's full answer text and a list of key points.
    Returns a list of results showing which points were covered, using
    sentence-level best-match comparison.
    """
    results = []

    # EDGE CASE: empty or too-short answer -> mark everything as missing, skip AI calls
    if not student_answer or len(student_answer.strip()) < MIN_ANSWER_LENGTH:
        for point in key_points:
            results.append({
                "point_id": point["point_id"],
                "point_text": point["point_text"],
                "score": 0.0,
                "covered": False,
                "matched_sentence": None
            })
        return results

    sentences = split_into_sentences(student_answer)

    for point in key_points:
        point_text = point["point_text"]

        best_score = 0.0
        best_sentence = None

        # Compare this key point against EVERY sentence, keep the best match
        for sentence in sentences:
            score = get_similarity(sentence, point_text)
            if score > best_score:
                best_score = score
                best_sentence = sentence

        covered = best_score >= SIMILARITY_THRESHOLD

        results.append({
            "point_id": point["point_id"],
            "point_text": point_text,
            "score": round(best_score, 3),
            "covered": covered,
            "matched_sentence": best_sentence
        })

    return results


# Quick test when running this file directly
if __name__ == "__main__":
    from question_loader import load_questions, get_question_by_id

    questions = load_questions()
    question = get_question_by_id(questions, "Q1")

    # A longer, multi-sentence student answer (more realistic)
    student_answer = (
        "Photosynthesis is how plants make their food. "
        "They use sunlight as their main source of energy. "
        "Water and carbon dioxide are taken in by the plant. "
        "This whole process takes place inside the chloroplasts."
    )

    print(f"Question: {question['question_text']}\n")
    print(f"Student answer: {student_answer}\n")

    results = check_keypoints_coverage(student_answer, question["key_points"])

    print("----- KEY POINT COVERAGE (sentence-level matching) -----")
    covered_count = 0
    for r in results:
        status = "✅ COVERED" if r["covered"] else "❌ MISSING"
        print(f"[{r['point_id']}] {r['point_text']}")
        print(f"    Best score: {r['score']}  -->  {status}")
        print(f"    Matched sentence: \"{r['matched_sentence']}\"")
        if r["covered"]:
            covered_count += 1

    print(f"\nTotal points covered: {covered_count} / {len(results)}")

    # EDGE CASE test: empty answer
    print("\n\n----- EDGE CASE TEST: empty answer -----")
    empty_results = check_keypoints_coverage("", question["key_points"])
    for r in empty_results:
        print(f"[{r['point_id']}] Score: {r['score']} --> covered: {r['covered']}")
"""
Semantic Similarity Module — Semantic AI Based Short Answer Evaluation
Uses Sentence-BERT to check how similar two pieces of text are in MEANING,
not just exact word matching.
"""

from sentence_transformers import SentenceTransformer, util

# Load the pre-trained model (only needs to happen once)
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_similarity(text1, text2):
    """
    Takes two pieces of text and returns a similarity score between 0 and 1.
    1.0 = identical meaning, 0.0 = completely unrelated meaning.
    """
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    similarity_score = util.cos_sim(embedding1, embedding2)

    return similarity_score.item()


# Quick test when running this file directly
if __name__ == "__main__":
    # Test case 1: same meaning, different wording (should score HIGH)
    text_a = "Plants use sunlight as an energy source"
    text_b = "Sunlight is converted to energy by plants"
    score1 = get_similarity(text_a, text_b)
    print(f"Text A: {text_a}")
    print(f"Text B: {text_b}")
    print(f"Similarity score: {score1:.3f}  (expect: HIGH, close to 1.0)\n")

    # Test case 2: unrelated meaning (should score LOW)
    text_c = "Plants use sunlight as an energy source"
    text_d = "Newton's first law is about objects staying at rest"
    score2 = get_similarity(text_c, text_d)
    print(f"Text C: {text_c}")
    print(f"Text D: {text_d}")
    print(f"Similarity score: {score2:.3f}  (expect: LOW, close to 0.0)\n")

    # Test case 3: exact same sentence (should score ~1.0)
    text_e = "The process produces glucose and oxygen"
    score3 = get_similarity(text_e, text_e)
    print(f"Text E vs itself")
    print(f"Similarity score: {score3:.3f}  (expect: ~1.0)")
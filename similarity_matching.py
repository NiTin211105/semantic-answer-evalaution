from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def calculate_similarity(reference_answer, student_answer):
    """
    Calculate semantic similarity between reference and student answers.
    Returns a score between 0 and 1.
    """

    if not reference_answer or not student_answer:
        return 0.0

    embedding_model = get_model()

    embeddings = embedding_model.encode(
        [reference_answer, student_answer]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)

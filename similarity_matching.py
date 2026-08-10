"""
Semantic Similarity Module
Uses Sentence-BERT to compare answer meaning.
"""

model = None


def get_model():
    global model

    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def get_similarity(text1, text2):
    """
    Returns semantic similarity between two pieces of text.
    """

    if not text1 or not text2:
        return 0.0

    embedding_model = get_model()

    embedding1 = embedding_model.encode(
        text1,
        convert_to_tensor=True
    )

    embedding2 = embedding_model.encode(
        text2,
        convert_to_tensor=True
    )

    from sentence_transformers import util

    similarity_score = util.cos_sim(
        embedding1,
        embedding2
    )

    return float(similarity_score.item())

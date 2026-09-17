from sentence_transformers import SentenceTransformer


# Multilingual embedding model.
# Supports English, Hindi and Gujarati.
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

print("Loading embedding model...")
print(f"Model: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


def encode_texts(texts, batch_size=64):
    """
    Convert all dataset records into normalized embeddings.
    """

    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )


def encode_query(query):
    """
    Convert a user query into a normalized embedding.
    """

    return model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
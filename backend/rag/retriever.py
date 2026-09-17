import json
from pathlib import Path

import faiss
import numpy as np

from rag.embeddings import encode_query


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_DIR = BASE_DIR / ".index"

INDEX_PATH = INDEX_DIR / "gita_qa.index"
METADATA_PATH = INDEX_DIR / "metadata.json"


# ---------------------------------------------------------
# LOAD FAISS INDEX
# ---------------------------------------------------------

_index = None
_metadata = None


def load_index():

    global _index
    global _metadata

    if _index is not None and _metadata is not None:
        return _index, _metadata

    # Check FAISS index
    if not INDEX_PATH.exists():

        raise FileNotFoundError(
            f"FAISS index not found:\n{INDEX_PATH}\n\n"
            "Please run:\n"
            "python build.py"
        )

    # Check metadata
    if not METADATA_PATH.exists():

        raise FileNotFoundError(
            f"Metadata file not found:\n{METADATA_PATH}\n\n"
            "Please run:\n"
            "python build.py"
        )

    print("Loading FAISS index...")

    _index = faiss.read_index(
        str(INDEX_PATH)
    )

    print(
        f"FAISS index loaded successfully: "
        f"{_index.ntotal} vectors"
    )

    print("Loading metadata...")

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        _metadata = json.load(file)

    print(
        f"Metadata loaded successfully: "
        f"{len(_metadata)} records"
    )

    return _index, _metadata


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

def search_verses(
    query: str,
    top_k: int = 5
):

    index, metadata = load_index()

    if not query or not query.strip():

        return []

    # Make sure top_k is valid
    top_k = max(
        1,
        min(
            int(top_k),
            len(metadata)
        )
    )

    # Create embedding for user query
    query_embedding = encode_query(
        query
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # FAISS semantic search
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0]
    ):

        if index_id < 0:
            continue

        record = metadata[
            int(index_id)
        ].copy()

        record[
            "similarity_score"
        ] = float(score)

        results.append(record)

    return results
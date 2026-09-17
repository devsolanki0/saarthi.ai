import json
from pathlib import Path

import faiss
import numpy as np

from rag.data_loader import load_all_records, make_search_text
from rag.embeddings import encode_texts


BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_DIR = BASE_DIR / ".index"
INDEX_PATH = INDEX_DIR / "gita_qa.index"
METADATA_PATH = INDEX_DIR / "metadata.json"


def build_index():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Loading Bhagavad Gita QA dataset...")
    print("=" * 60)

    records = load_all_records()

    if not records:
        raise RuntimeError("No dataset records were loaded.")

    print()
    print(f"Total records loaded: {len(records)}")

    texts = [
        make_search_text(record)
        for record in records
    ]

    print()
    print("=" * 60)
    print(f"Creating embeddings for {len(texts)} records...")
    print("=" * 60)
    print("This may take several minutes on the first build.")
    print()

    embeddings = encode_texts(texts)

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    print()
    print(f"Embedding dimension: {dimension}")

    # Inner Product works as cosine similarity because
    # embeddings are normalized in embeddings.py.
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(f"FAISS index contains: {index.ntotal} vectors")

    # Save FAISS index
    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    # Save corresponding metadata
    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("=" * 60)
    print("SAARTHI.AI RAG INDEX READY")
    print("=" * 60)
    print(f"Records indexed : {len(records)}")
    print(f"Embedding size  : {dimension}")
    print(f"FAISS index     : {INDEX_PATH}")
    print(f"Metadata        : {METADATA_PATH}")
    print("=" * 60)

    return len(records)
from datasets import load_dataset


DATASET_ID = "JDhruv14/Bhagavad-Gita-QA"

LANGUAGES = [
    "English",
    "Hindi",
    "Gujarati",
]


REQUIRED_COLUMNS = {
    "chapter_no",
    "verse_no",
    "question",
    "answer",
}


def load_all_records():

    records = []

    for language in LANGUAGES:

        print()
        print("=" * 60)
        print(f"Loading {language} dataset...")
        print("=" * 60)

        dataset = load_dataset(
            DATASET_ID,
            language,
            split="train"
        )

        print(f"Columns: {dataset.column_names}")
        print(f"Rows: {len(dataset)}")

        missing_columns = REQUIRED_COLUMNS - set(dataset.column_names)

        if missing_columns:
            raise ValueError(
                f"{language} dataset is missing columns: "
                f"{missing_columns}"
            )

        for row in dataset:

            question = str(row["question"]).strip()
            answer = str(row["answer"]).strip()

            if not question or not answer:
                continue

            records.append({
                "language": language,
                "chapter_no": int(row["chapter_no"]),
                "verse_no": int(row["verse_no"]),
                "question": question,
                "answer": answer,
            })

        print(f"{language}: {len(dataset)} records loaded")

    print()
    print("=" * 60)
    print(f"TOTAL RECORDS: {len(records)}")
    print("=" * 60)

    return records


def make_search_text(record):

    return (
        f"Language: {record['language']}. "
        f"Bhagavad Gita Chapter {record['chapter_no']}, "
        f"Verse {record['verse_no']}. "
        f"Question: {record['question']} "
        f"Answer: {record['answer']}"
    )
from rag.indexer import build_index


def main():
    print("=" * 60)
    print("SAARTHI.AI - BUILDING FULL GITA KNOWLEDGE BASE")
    print("=" * 60)
    print()

    print("Dataset:")
    print("JDhruv14/Bhagavad-Gita-QA")
    print()

    print("Languages:")
    print("1. English")
    print("2. Hindi")
    print("3. Gujarati")
    print()

    print("Loading the complete dataset...")
    print("No sampling or record limit will be applied.")
    print()

    try:
        total_records = build_index()

        print()
        print("=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Total records indexed: {total_records}")
        print()
        print("Your FAISS knowledge base is ready.")
        print()
        print("You can now start the backend with:")
        print("python -m uvicorn main:app --reload")
        print("=" * 60)

    except Exception as error:
        print()
        print("=" * 60)
        print("BUILD FAILED")
        print("=" * 60)
        print(f"Error: {error}")
        print()
        print("Check the error above and try again.")
        raise


if __name__ == "__main__":
    main()
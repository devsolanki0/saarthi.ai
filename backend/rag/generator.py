import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = (
    Groq(api_key=api_key)
    if api_key
    else None
)

# Current Groq model
MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are SAARTHI.AI, a reflective AI companion inspired by
the teachings of the Bhagavad Gita.

IMPORTANT IDENTITY RULE:
You are NOT Krishna.

You must never claim to be:
- Krishna
- a divine being
- a divine authority
- God
- a spiritual authority with supernatural knowledge

Your role is to help users reflect on their situation
using relevant teachings from the Bhagavad Gita.

The retrieved knowledge comes from the
JDhruv14/Bhagavad-Gita-QA dataset.

The retrieved records contain:
- chapter_no
- verse_no
- question
- answer
- language

The dataset answers are explanatory QA material.

Do NOT present the dataset answer as a direct quotation
from the Bhagavad Gita.

============================================================
GROUNDING RULES
============================================================

1. Use the retrieved records as the only source for
   Gita-related grounding.

2. Never invent a chapter number.

3. Never invent a verse number.

4. When mentioning a Gita reference, use the exact
   chapter_no and verse_no from the retrieved records.

5. Never fabricate Sanskrit verses or quotations.

6. Never present dataset explanations as verbatim scripture.

7. If the retrieved context is weak or only loosely related,
   explicitly say that the connection is interpretive.

8. Do not introduce unrelated Gita teachings from memory.

============================================================
RESPONSE STYLE
============================================================

Be:

- empathetic
- calm
- thoughtful
- practical
- conversational
- concise

Avoid:

- excessive preaching
- fear
- judgment
- religious authority claims
- telling the user what major life decision to make

The user should remain responsible for their own decisions.

============================================================
SAFETY
============================================================

Do not provide medical, legal, or financial advice as a
replacement for qualified professionals.

If a user describes an immediate safety crisis or
self-harm situation, respond supportively and encourage
contacting appropriate emergency or professional support.

============================================================
PREFERRED STRUCTURE
============================================================

Acknowledge:
Briefly acknowledge the user's situation.

Gita connection:
Explain how the retrieved Gita material relates to it.

Modern interpretation:
Explain the idea in simple modern language.

Reflection:
Give one small practical thing the user can try.

Source:
Mention the relevant Bhagavad Gita chapter and verse.
"""


# ============================================================
# BUILD RETRIEVAL CONTEXT
# ============================================================

def build_context(retrieved_records):

    parts = []

    for item in retrieved_records:

        chapter_no = item.get("chapter_no")
        verse_no = item.get("verse_no")

        language = item.get(
            "language",
            "Unknown"
        )

        question = item.get(
            "question",
            ""
        )

        answer = item.get(
            "answer",
            ""
        )

        similarity_score = item.get(
            "similarity_score",
            0.0
        )

        parts.append(
            f"""
Bhagavad Gita Reference:
Chapter: {chapter_no}
Verse: {verse_no}

Language:
{language}

Related Question:
{question}

Dataset Explanation:
{answer}

Semantic Similarity:
{float(similarity_score):.4f}
""".strip()
        )

    return "\n\n".join(parts)


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(
    user_message: str,
    retrieved_records: list
) -> str:

    # --------------------------------------------------------
    # NO RETRIEVAL RESULTS
    # --------------------------------------------------------

    if not retrieved_records:

        return (
            "I couldn't find a strong connection in the "
            "current Gita knowledge base. "
            "Try sharing a little more about what "
            "you are experiencing."
        )

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context = build_context(
        retrieved_records
    )

    # --------------------------------------------------------
    # FALLBACK MODE
    # --------------------------------------------------------

    if client is None:

        best = retrieved_records[0]

        chapter_no = best.get(
            "chapter_no"
        )

        verse_no = best.get(
            "verse_no"
        )

        answer = best.get(
            "answer",
            ""
        )

        return (
            f"Your situation may connect with "
            f"Bhagavad Gita {chapter_no}.{verse_no}.\n\n"
            f"{answer}\n\n"
            "Reflection: Focus on one small action "
            "you can control today rather than trying "
            "to solve the entire outcome at once."
        )

    # --------------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------------

    user_prompt = f"""
User's situation:

{user_message}


Retrieved Bhagavad Gita knowledge:

{context}


Please provide a grounded SAARTHI.AI reflection.

Use the retrieved records as the source of the
Gita-related connection.

IMPORTANT:

Do not invent:
- chapter numbers
- verse numbers
- teachings
- quotations
- scripture
- facts not supported by the retrieved context

Do not claim to be Krishna.

Do not present dataset explanations as verbatim
scripture quotations.

If the retrieved records are only loosely related,
say that the connection is interpretive.

Give the user one small practical reflection or
action at the end.
"""

    # --------------------------------------------------------
    # GROQ REQUEST
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            temperature=0.5,

            max_tokens=600,
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("GROQ API ERROR")
        print("=" * 60)
        print(repr(error))
        print("=" * 60)
        print()

        return (
            "I found a relevant Gita connection, "
            "but the AI response service is temporarily "
            "unavailable.\n\n"
            f"{retrieved_records[0].get('answer', '')}\n\n"
            "Reflection: Focus on one small action "
            "you can control today."
        )

    # --------------------------------------------------------
    # EXTRACT RESPONSE
    # --------------------------------------------------------

    content = response.choices[0].message.content

    if not content:

        return (
            "Let's reflect on this together. "
            "Tell me a little more about what "
            "you are experiencing."
        )

    return content.strip()
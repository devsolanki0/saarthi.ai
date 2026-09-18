from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SAARTHI.AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "SAARTHI.AI"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag.retriever import search_verses
from rag.generator import generate_response


# ============================================================
# SAARTHI.AI FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="SAARTHI.AI",
    description="AI companion inspired by the Bhagavad Gita using RAG",
    version="2.0.0",
)


# ============================================================
# CORS CONFIGURATION
# ============================================================
#
# The Next.js frontend runs on localhost:3000 or
# 127.0.0.1:3000 during development.
#
# This allows the browser to call:
#
# http://127.0.0.1:8000/api/chat
#
# directly from Chat.tsx.
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's life situation or question",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of Gita records to retrieve",
    )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "SAARTHI.AI backend is running",
        "status": "healthy",
        "version": "2.0.0",
        "rag": "multilingual_full_dataset",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "SAARTHI.AI",
    }


# ============================================================
# RAG SEARCH ENDPOINT
# ============================================================

@app.get("/api/search")
def search(
    query: str,
    top_k: int = 5,
):
    """
    Search the Bhagavad Gita knowledge base
    using semantic similarity.
    """

    query = query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    try:
        results = search_verses(
            query,
            top_k,
        )

        return {
            "query": query,
            "results": results,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    except Exception as error:
        print("SEARCH ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="RAG search failed.",
        )


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Main SAARTHI.AI conversation endpoint.

    Flow:

    User message
          ↓
    Semantic retrieval
          ↓
    Top relevant Gita records
          ↓
    Grounded response generation
          ↓
    Response + source references
    """

    user_message = request.message.strip()

    if not user_message:
        return {
            "response": "Please share what is on your mind.",
            "verses": [],
        }

    try:

        # ----------------------------------------------------
        # STEP 1 — RETRIEVE RELEVANT GITA RECORDS
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("SAARTHI.AI CHAT REQUEST")
        print("=" * 60)
        print("User:", user_message)
        print("Top K:", request.top_k)

        verses = search_verses(
            user_message,
            request.top_k,
        )

        print(
            f"Retrieved {len(verses)} Gita records"
        )

        # ----------------------------------------------------
        # STEP 2 — GENERATE GROUNDED RESPONSE
        # ----------------------------------------------------

        response = generate_response(
            user_message,
            verses,
        )

        print("Response generated successfully.")
        print("=" * 60)
        print()

        # ----------------------------------------------------
        # STEP 3 — RETURN JSON TO FRONTEND
        # ----------------------------------------------------

        return {
            "response": response,
            "verses": verses,
        }

    except FileNotFoundError as error:

        print(
            "RAG FILE ERROR:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

    #except Exception as error:

        print(
            "CHAT ERROR:",
            repr(error),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "SAARTHI.AI could not process "
                "the request. Check the backend terminal "
                "for the detailed error."
            ),
        )

    except Exception as error:

        import traceback

        print()
        print("=" * 60)
        print("CHAT ERROR")
        print("=" * 60)

        traceback.print_exc()

        print("=" * 60)
        print()

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )      


# ============================================================
# DEVELOPMENT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

"""FastAPI service for the local Ollama-powered code tutor."""

import os
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import save_conversation, search_knowledge
from question_bank import QUESTIONS
from rag import context_for, is_tree_question

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
MAX_CODE_LENGTH = 50_000

app = FastAPI(title="AI Code Tutor API", version="1.0.0")

# The Next.js dev server runs on port 3000. Configure FRONTEND_ORIGIN for deployments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class TutorRequest(BaseModel):
    code: str = Field(default="", max_length=MAX_CODE_LENGTH)
    question: str = Field(min_length=1, max_length=4_000)
    language: Literal["javascript", "python", "java"]
    output: str = Field(default="", max_length=10_000)
    mode: Literal["chat", "debug", "question"] = "chat"
    problem: str = Field(default="", max_length=4_000)


class TutorResponse(BaseModel):
    answer: str
    model: str
    sources: list[str]


TREE_ONLY_SYSTEM_PROMPT = (
    "You are a precise, friendly Tree Data Structures and Algorithms tutor. "
    "Answer ONLY questions about trees, binary trees, BSTs, traversals, heaps, "
    "tries, balanced trees, or tree algorithms. Use the retrieved knowledge "
    "base as your primary factual context. Do not claim to have run code. "
    "Keep answers concise and include corrected snippets only when useful."
)

DEBUG_SYSTEM_PROMPT = (
    "You are a precise, friendly coding assistant embedded in a code editor. "
    "You can see the user's current code and the latest terminal output below. "
    "Diagnose errors with the exact line/cause when possible, suggest concrete fixes, "
    "and answer questions about the code's behavior, complexity, or style. "
    "You are not restricted to tree topics in this mode. Do not claim to have run the "
    "code yourself beyond what the provided terminal output shows. Keep answers concise "
    "and include corrected snippets only when useful."
)

QUESTION_SYSTEM_PROMPT = (
    "You are a friendly Tree DSA mentor helping a learner solve the specific practice "
    "problem described below in a code editor. You can see the problem statement, their "
    "current code, and the latest terminal output. Give hints, explain the approach, or "
    "point out the exact bug/line causing a failure — without simply handing over a full "
    "solution unless they explicitly ask you to check or reveal one. Use the retrieved "
    "tree knowledge base as supporting context. Do not claim to have run the code yourself "
    "beyond what the provided terminal output shows."
)


def build_messages(request: TutorRequest, retrieved_context: str) -> list[dict[str, str]]:
    context = f"""Language: {request.language}
Code:
```{request.language}
{request.code}
```

Latest program output:
```
{request.output or "(No output provided)"}
```"""

    if request.mode == "debug":
        system_prompt = DEBUG_SYSTEM_PROMPT
    elif request.mode == "question":
        system_prompt = QUESTION_SYSTEM_PROMPT
        if request.problem:
            context = f"Problem statement:\n{request.problem}\n\n{context}"
    else:
        system_prompt = TREE_ONLY_SYSTEM_PROMPT

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Retrieved Tree DSA knowledge:\n{retrieved_context}\n\n{context}\n\nQuestion: {request.question}"},
    ]


@app.get("/health")
async def health() -> dict[str, str]:
    """Lightweight service health check; it does not contact Ollama."""
    return {"status": "ok", "model": OLLAMA_MODEL}


@app.get("/api/questions")
async def questions() -> list[dict[str, str]]:
    """Return the Tree DSA challenge bank for the coding workspace."""
    return QUESTIONS


@app.post("/api/tutor", response_model=TutorResponse)
async def tutor(request: TutorRequest) -> TutorResponse:
    """Ask the configured local Ollama model about submitted code."""
    if request.mode == "chat" and not is_tree_question(request.question):
        return TutorResponse(
            answer="I’m the Tree DSA tutor, so I can help with binary trees, BSTs, traversals, heaps, tries, LCA, and related tree algorithms.",
            model=OLLAMA_MODEL,
            sources=[],
        )

    retrieved_context, sources = context_for(request.question)
    # If pgvector has been seeded, prefer semantic retrieval over keyword fallback.
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            embedding_response = await client.post(
                f"{OLLAMA_URL.rstrip('/')}/api/embed",
                json={"model": EMBEDDING_MODEL, "input": request.question},
            )
            embedding_response.raise_for_status()
            vector_documents = search_knowledge(embedding_response.json()["embeddings"][0])
            if vector_documents:
                retrieved_context = "\n\n".join(item["content"] for item in vector_documents)
                sources = [item["title"] for item in vector_documents]
    except (httpx.HTTPError, KeyError, IndexError):
        pass
    payload = {
        "model": OLLAMA_MODEL,
        "messages": build_messages(request, retrieved_context),
        "stream": False,
        "options": {"temperature": 0.2},
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.ConnectError as error:
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Ollama. Start it with `ollama serve` and pull the configured model.",
        ) from error
    except httpx.TimeoutException as error:
        raise HTTPException(status_code=504, detail="Ollama took too long to respond.") from error
    except httpx.HTTPStatusError as error:
        detail = error.response.text or "Ollama returned an error."
        raise HTTPException(status_code=502, detail=detail) from error

    answer = data.get("message", {}).get("content", "").strip()
    if not answer:
        raise HTTPException(status_code=502, detail="Ollama returned an empty response.")

    save_conversation(request.question, answer)
    return TutorResponse(answer=answer, model=OLLAMA_MODEL, sources=sources)
"""FastAPI service for the local Ollama-powered code tutor, backed by CrewAI agents."""

import asyncio
import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents import run_crew
from question_bank import QUESTIONS
from rag import context_for, is_tree_question

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
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


def build_context(request: TutorRequest, retrieved_context: str) -> str:
    """Assemble the context block handed to the mode's CrewAI agent as its task description."""
    parts = []
    if request.mode == "question" and request.problem:
        parts.append(f"Problem statement:\n{request.problem}")
    parts.append(
        f"Language: {request.language}\n"
        f"Code:\n```{request.language}\n{request.code}\n```\n\n"
        f"Latest program output:\n```\n{request.output or '(No output provided)'}\n```"
    )
    parts.append(f"Retrieved Tree DSA knowledge:\n{retrieved_context or '(No matching knowledge-base sections)'}")
    return "\n\n".join(parts)


@app.get("/health")
async def health() -> dict[str, str]:
    """Lightweight service health check; it does not contact Ollama."""
    return {"status": "ok", "model": OLLAMA_MODEL}


@app.get("/api/questions")
async def questions() -> list[dict]:
    """Return the Tree DSA challenge bank."""
    return QUESTIONS


@app.post("/api/tutor", response_model=TutorResponse)
async def tutor(request: TutorRequest) -> TutorResponse:
    """Route the request to the CrewAI agent for its mode (chat / debug / question)."""
    if request.mode == "chat" and not is_tree_question(request.question):
        return TutorResponse(
            answer="I’m the Tree DSA tutor, so I can help with binary trees, BSTs, traversals, heaps, tries, LCA, and related tree algorithms.",
            model=OLLAMA_MODEL,
            sources=[],
        )

    retrieved_context, sources = context_for(request.question)
    context = build_context(request, retrieved_context)

    try:
        # CrewAI's kickoff() is a blocking call, so it runs off the event loop.
        answer = await asyncio.to_thread(run_crew, request.mode, context, request.question)
    except Exception as error:  # CrewAI/LiteLLM raise a range of provider errors here.
        message = str(error).lower()
        if "connect" in message or "connection" in message:
            raise HTTPException(
                status_code=503,
                detail="Cannot reach Ollama. Start it with `ollama serve` and pull the configured model.",
            ) from error
        if "timeout" in message or "timed out" in message:
            raise HTTPException(status_code=504, detail="Ollama took too long to respond.") from error
        raise HTTPException(status_code=502, detail=f"Agent request failed: {error}") from error

    if not answer:
        raise HTTPException(status_code=502, detail="The agent returned an empty response.")

    return TutorResponse(answer=answer, model=OLLAMA_MODEL, sources=sources)
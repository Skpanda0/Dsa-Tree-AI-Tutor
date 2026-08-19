"""Seed Postgres/pgvector with the local Tree DSA question and RAG documents.

Run after `docker compose up -d` and `ollama pull nomic-embed-text`.
"""
import os
import re
from pathlib import Path

import httpx
import psycopg

from question_bank import QUESTIONS

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://tree_tutor:change-me-local@localhost:5432/tree_tutor")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")


def chunks():
    text = (Path(__file__).parent / "knowledge_base" / "tree_dsa.md").read_text(encoding="utf-8")
    for section in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        title, content = section.split("\n", 1)
        yield title.strip(), section.strip()


def embed(client, text):
    response = client.post(f"{OLLAMA_URL.rstrip('/')}/api/embed", json={"model": EMBEDDING_MODEL, "input": text})
    response.raise_for_status()
    return response.json()["embeddings"][0]


with psycopg.connect(DATABASE_URL) as conn, httpx.Client(timeout=90) as client:
    with conn.cursor() as cur:
        for item in QUESTIONS:
            cur.execute("""INSERT INTO questions (id, title, difficulty, prompt, examples, starter)
                VALUES (%(id)s, %(title)s, %(difficulty)s, %(prompt)s, %(examples)s, %(starter)s)
                ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title, difficulty=EXCLUDED.difficulty,
                prompt=EXCLUDED.prompt, examples=EXCLUDED.examples, starter=EXCLUDED.starter""", item)
        cur.execute("DELETE FROM knowledge_documents")
        for title, content in chunks():
            cur.execute("INSERT INTO knowledge_documents (title, content, embedding) VALUES (%s, %s, %s::vector)", (title, content, str(embed(client, content))))
    conn.commit()

print("Seeded 20 Tree DSA challenges and knowledge-base embeddings.")

"""Optional PostgreSQL + pgvector persistence for questions, RAG documents, and chats."""
import os
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL")


@contextmanager
def connection():
    if not DATABASE_URL:
        yield None
        return
    import psycopg
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def save_conversation(question: str, answer: str) -> None:
    try:
        with connection() as conn:
            if not conn:
                return
            with conn.cursor() as cur:
                cur.execute("INSERT INTO tutor_messages (role, content) VALUES ('user', %s), ('assistant', %s)", (question, answer))
            conn.commit()
    except Exception:
        # Persistence is optional; a temporary database outage should not break tutoring.
        return


def search_knowledge(embedding: list[float], limit: int = 3) -> list[dict[str, str]]:
    """Return nearest pgvector documents, or an empty list when DB is optional/unavailable."""
    if not DATABASE_URL:
        return []
    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT title, content FROM knowledge_documents "
                    "ORDER BY embedding <=> %s::vector LIMIT %s",
                    (str(embedding), limit),
                )
                return [{"title": title, "content": content} for title, content in cur.fetchall()]
    except Exception:
        return []

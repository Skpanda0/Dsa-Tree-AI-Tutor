"""Small, dependency-free retrieval layer for the Tree DSA knowledge base."""

import re
from pathlib import Path

KNOWLEDGE_BASE = Path(__file__).parent / "knowledge_base" / "tree_dsa.md"
TREE_TERMS = {
    "tree", "trees", "binary", "bst", "traversal", "preorder", "inorder",
    "postorder", "level order", "bfs", "dfs", "heap", "trie", "lca", "ancestor",
    "subtree", "leaf", "root", "avl", "red-black", "rotation", "diameter", "path sum",
}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9-]*", text.lower()))


def _chunks() -> list[tuple[str, str]]:
    sections = re.split(r"^## ", KNOWLEDGE_BASE.read_text(encoding="utf-8"), flags=re.MULTILINE)
    return [(part.split("\n", 1)[0].strip(), part.strip()) for part in sections[1:]]


def is_tree_question(question: str) -> bool:
    normalized = question.lower()
    return any(term in normalized for term in TREE_TERMS)


def retrieve(question: str, limit: int = 3) -> list[dict[str, str]]:
    query_tokens = _tokens(question)
    ranked = []
    for title, text in _chunks():
        score = len(query_tokens & _tokens(text))
        if score:
            ranked.append((score, title, text))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [{"title": title, "content": text} for _, title, text in ranked[:limit]]


def context_for(question: str) -> tuple[str, list[str]]:
    documents = retrieve(question)
    return "\n\n".join(item["content"] for item in documents), [item["title"] for item in documents]

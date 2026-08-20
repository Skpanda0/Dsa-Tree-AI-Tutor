# TreeTutor AI

TreeTutor AI is a learning workspace for Tree Data Structures and Algorithms. It combines a Next.js interface for writing and running small programs with an optional local Python tutor service powered by Ollama.

The project is deliberately database-free. Practice questions and Tree DSA reference material live in version-controlled files, so a fresh clone can run without Docker, migrations, credentials, embeddings, or external storage.

## Features

- Tree DSA tutoring with focused context from a local knowledge base.
- Code Lab that runs JavaScript, Python, or Java locally through the Next.js API.
- Built-in Tree DSA practice question bank.
- Separate tutor modes for conceptual questions, debugging guidance, and problem-solving hints.

## Tech stack

| Area | Technology |
| --- | --- |
| Frontend | Next.js 15, React 19, JavaScript |
| Local API routes | Next.js route handlers |
| Tutor backend | Python, FastAPI, CrewAI, Ollama |
| Knowledge retrieval | Local Markdown with dependency-free keyword retrieval |
| Content storage | Version-controlled Markdown and Python files |

## Project structure

```text
.
├── app/                    # Next.js pages and API routes
├── components/             # Tutor UI
├── backend/
│   ├── knowledge_base/     # Local Tree DSA reference material
│   ├── agents.py           # Tutor, debugging, and mentor agents
│   ├── main.py             # FastAPI service
│   ├── question_bank.py    # Built-in practice questions
│   └── rag.py              # Local retrieval helper
├── package.json
└── README.md
```

## Run the frontend

Prerequisites: Node.js 20.9+ and npm.

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). On Windows PowerShell, use `npm.cmd install` and `npm.cmd run dev` if the execution policy blocks npm.

For a production check:

```bash
npm run build
npm run start
```

## Run the Python tutor backend

The backend is optional for the frontend, but provides the local Ollama-powered tutor API.

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5-coder:7b
uvicorn main:app --reload --port 8000
```

Copy `backend/.env.example` to `backend/.env` only to change the Ollama URL, model, or permitted frontend origin. The default settings are suitable for local development.

The service exposes:

- `GET /health` for a local health check.
- `GET /api/questions` for the built-in question bank.
- `POST /api/tutor` for tutor, debugging, and practice-mentor responses.

## Knowledge base

`backend/knowledge_base/tree_dsa.md` is the tutor's local reference source. At request time, `backend/rag.py` compares the learner's question with each `##`-level section and sends the best-matching sections to the tutor. No database, embedding model, indexing command, or seed step is required.

The included material covers tree fundamentals, binary trees, traversals, BST operations and validation, balanced trees, heaps, tries, LCA, recursion contracts, path backtracking, iterative traversal, and common edge cases.

To extend it, add a descriptive `##` section to `tree_dsa.md`. Keep each section focused and include the relevant definition, complexity, trade-offs, and edge cases so retrieval has useful context to select from.

## Frontend API routes

- `POST /api/tutor` returns lightweight local tutor guidance for the frontend.
- `POST /api/run` executes JavaScript, Python, or Java code locally.

The code runner is intended for local learning only. Do not expose it publicly without moving execution into a properly isolated sandbox.

## Security and Git hygiene

- `.gitignore` excludes dependencies, build output, Python caches, virtual environments, logs, and `.env` files.
- Never commit API keys or provider secrets.
- Keep `.env.example` files limited to safe local defaults.

## Roadmap

1. Connect the frontend to the FastAPI tutor and question endpoints.
2. Add more focused Tree DSA reference sections and practice questions.
3. Show retrieved source sections alongside tutor responses in the UI.
4. Add authentication if user accounts become necessary.
5. Move code execution and AI analysis into a safe worker or sandbox before deployment.

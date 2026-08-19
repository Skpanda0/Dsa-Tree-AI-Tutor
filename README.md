# TreeTutor AI

TreeTutor AI is a Tree Data Structures and Algorithms learning platform. It is designed around three focused learning experiences rather than a generic chatbot:

- **Tree Tutor** — ask questions about Tree DSA concepts, patterns, complexity, and examples.
- **Code Lab** — write and run small JavaScript Tree DSA exercises, with guided AI-style feedback.
- **Practice and Concepts** — browse Tree problems and build conceptual foundations before solving them.

The repository has separate frontend and Python backend folders. The frontend currently uses polished mock data so it can be developed without a live API. Backend integration points are marked with `TODO` comments in the UI.

## Tech stack

| Area | Technology |
| --- | --- |
| Frontend | Next.js 15, React 19, JavaScript, Tailwind CSS 4 |
| Icons | Lucide React |
| Backend | Python (existing service under `backend/`) |
| Planned database | PostgreSQL |
| Planned AI capabilities | Python agents, RAG, code analysis, question generation |

## Project structure

```text
.
├── app/                    # Next.js routes and page UI
│   ├── dashboard/          # Tree Tutor chat
│   ├── debugger/           # Code Lab
│   ├── practice/           # Problem catalogue and problem page
│   ├── concepts/           # Concept catalogue and lesson page
│   └── login/              # Authentication UI placeholder
├── components/
│   ├── chat/               # Tutor chat components
│   ├── layout/             # App shell and sidebar
│   ├── practice/           # Problem cards
│   └── tree/               # Tree visualizer
├── data/mockData.js        # Temporary frontend mock data
├── backend/                # Existing Python AI/RAG service
├── package.json
└── README.md
```

## Run the frontend

### Prerequisites

- Node.js 20.9 or newer (LTS recommended)
- npm

### Install and start

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

On Windows PowerShell, if your execution policy blocks `npm`, use:

```powershell
npm.cmd install
npm.cmd run dev
```

### Production check

```bash
npm run build
npm run start
```

The project must build successfully before deployment. The latest production build completes successfully.

## Available frontend pages

| Route | Purpose |
| --- | --- |
| `/` | Product landing page |
| `/login` | Auth UI placeholder |
| `/dashboard` | Tree Tutor chat workspace |
| `/debugger` | Lightweight Code Lab and guided question picker |
| `/practice` | Tree problem catalogue |
| `/practice/[id]` | Individual problem workspace |
| `/concepts` | Tree concept library |
| `/concepts/[slug]` | Individual concept lesson |

## How the current UI works

### Tree Tutor

The dashboard is intentionally viewport-bound: the overall page does not scroll, while the **message history is the scrollable chat area**. The tutor response, code example, source list, and tree visualization are mock content for now.

### Code Lab

The Code Lab is deliberately not a full LeetCode clone. It provides:

1. A simple JavaScript editor.
2. A `Run code` action and a local output area.
3. An AI-assistant-style guidance panel.
4. Tree questions that can be selected and loaded into the same editor.

Browser execution is **JavaScript only**. It is useful for simple examples and learning interactions. Never treat browser execution as a secure sandbox or as server-side code execution. Real multi-language compilation, secure test execution, and AI analysis should be handled by the Python backend.

## Mock data and future API integration

`data/mockData.js` is the single source of mock tree, concept, and practice data. This makes the eventual transition to backend data straightforward.

Suggested future backend endpoints:

```text
POST /chat       # Tutor question -> answer, sources, tree data
POST /debug      # Code + language -> analysis and suggested fix
GET  /problems   # Practice catalogue
GET  /concepts   # Learning catalogue/content
POST /submit     # Submission -> test results and AI feedback
GET  /history    # User chat history
```

Keep API calls in small client/service functions. Do not mix request logic through visual components. Replace each mock-data import with an isolated function that calls the Python service and handles loading, error, and empty states.

## PostgreSQL setup for the backend

PostgreSQL credentials must only be used by the Python backend. Do **not** expose the database URL in a Next.js client component or a `NEXT_PUBLIC_*` environment variable.

### 1. Create the database

Run in `psql` as a PostgreSQL administrator:

```sql
CREATE USER treetutor_user WITH PASSWORD 'replace-with-a-strong-password';
CREATE DATABASE treetutor OWNER treetutor_user;
GRANT ALL PRIVILEGES ON DATABASE treetutor TO treetutor_user;
```

### 2. Configure the backend environment

Copy the backend example environment file and add the connection string:

```env
DATABASE_URL=postgresql://treetutor_user:replace-with-a-strong-password@localhost:5432/treetutor
```

`backend/.env` is ignored by Git. Commit only `backend/.env.example` with placeholder values.

### 3. Install Python database packages

From `backend/`, use a virtual environment and install the PostgreSQL driver plus your ORM or query layer. With SQLAlchemy:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install sqlalchemy "psycopg[binary]" python-dotenv
```

Minimal connection example:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
```

### 4. Store application data

Useful first tables are `users`, `chats`, `messages`, `problems`, and `practice_submissions`. Store structured AI metadata such as source citations and test feedback in PostgreSQL `JSONB` fields when appropriate. Use migrations (for example Alembic) once schema changes begin.

## Authentication

The login page is UI-only at present. When Auth.js/NextAuth is configured, connect the existing login UI to it; do not put database credentials or provider secrets in the browser.

## Security and Git hygiene

- `.gitignore` excludes dependencies, build output, Python caches, virtual environments, local databases, logs, and `.env` files.
- Never commit real API keys, database URLs, or passwords.
- Keep `*.example` environment files with only dummy values.
- Run user-provided code in a properly isolated backend sandbox before offering real multi-language execution.

## Development roadmap

1. Connect authentication and user identity.
2. Add PostgreSQL migrations and persistence for users, chats, and submissions.
3. Add Python API endpoints with CORS configured for the frontend origin.
4. Replace mock data one page at a time.
5. Add RAG sources and tree data to Tutor API responses.
6. Move code execution and AI analysis into a safe backend worker/sandbox.
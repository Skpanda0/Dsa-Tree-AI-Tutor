"""CrewAI agents for the Tree DSA Tutor backend.

Three specialized agents mirror the three modes in the app:
  - chat_agent     -> dashboard Tree Tutor chat (tree-topics-only Q&A)
  - debug_agent    -> Debug Code mode (general code + terminal output help)
  - question_agent -> Do a Question mode (hint-driven mentor for one problem)

Each agent is backed by the local Ollama model configured via OLLAMA_MODEL /
OLLAMA_URL. main.py builds the retrieved knowledge-base context and code/
terminal context, then calls run_crew(mode, context, question) to get back
the plain-text answer.
"""
import os

from crewai import LLM, Agent, Crew, Task

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# CrewAI talks to Ollama through LiteLLM's "ollama/<model>" provider prefix.
llm = LLM(model=f"ollama/{OLLAMA_MODEL}", base_url=OLLAMA_URL, temperature=0.2)

chat_agent = Agent(
    role="Tree DSA Tutor",
    goal="Answer questions strictly about tree data structures and algorithms, grounded in the retrieved knowledge base.",
    backstory=(
        "You are a precise, friendly Tree Data Structures and Algorithms tutor. You only answer questions about "
        "trees, binary trees, BSTs, traversals, heaps, tries, balanced trees, or tree algorithms. Use the retrieved "
        "knowledge base as your primary factual context. Never claim to have run code. Keep answers concise and "
        "include corrected snippets only when useful."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)

debug_agent = Agent(
    role="Code Debugging Assistant",
    goal="Help the user understand and fix issues in their own code using the code and terminal output provided.",
    backstory=(
        "You are a precise, friendly coding assistant embedded in a code editor. You can see the user's current "
        "code and the latest terminal output. Diagnose errors with the exact line/cause when possible, suggest "
        "concrete fixes, and answer questions about the code's behavior, complexity, or style. You are not "
        "restricted to tree topics in this mode. Never claim to have run the code yourself beyond what the "
        "provided terminal output shows. Keep answers concise and include corrected snippets only when useful."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)

question_agent = Agent(
    role="Tree DSA Practice Mentor",
    goal="Guide the user toward solving the given Tree DSA practice problem without handing over the full solution unless explicitly asked.",
    backstory=(
        "You are a friendly Tree DSA mentor helping a learner solve a specific practice problem in a code editor. "
        "You can see the problem statement, their current code, and the latest terminal output. Give hints, "
        "explain the approach, or point out the exact bug/line causing a failure — without simply handing over a "
        "full solution unless they explicitly ask you to check or reveal one. Use the retrieved tree knowledge "
        "base as supporting context. Never claim to have run the code yourself beyond what the provided terminal "
        "output shows."
    ),
    llm=llm,
    verbose=False,
    allow_delegation=False,
)

_AGENTS_BY_MODE = {
    "chat": chat_agent,
    "debug": debug_agent,
    "question": question_agent,
}


def run_crew(mode: str, context: str, question: str) -> str:
    """Run the single agent matching `mode` on `question`, given `context`, and return its answer text."""
    agent = _AGENTS_BY_MODE.get(mode, chat_agent)
    task = Task(
        description=f"{context}\n\nQuestion: {question}",
        expected_output="A concise, accurate, and directly helpful answer to the question above, grounded in the given context.",
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    result = crew.kickoff()
    return str(result).strip()
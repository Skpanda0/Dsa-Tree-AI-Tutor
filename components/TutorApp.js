"use client";

import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import { Bot, BookOpen, CheckCircle2, Code2, MessageCircle, Play, RotateCcw, Send, Terminal, XCircle } from "lucide-react";

const languages = {
  javascript: { label: "JavaScript", monaco: "javascript", starter: `class TreeNode {\n  constructor(value, left = null, right = null) {\n    this.value = value; this.left = left; this.right = right;\n  }\n}\n\nfunction inorder(root) {\n  if (!root) return [];\n  return [...inorder(root.left), root.value, ...inorder(root.right)];\n}` },
  python: { label: "Python", monaco: "python", starter: `class TreeNode:\n    def __init__(self, value, left=None, right=None):\n        self.value = value\n        self.left = left\n        self.right = right\n\n\ndef inorder(root):\n    if root is None:\n        return []\n    return inorder(root.left) + [root.value] + inorder(root.right)` },
  java: { label: "Java", monaco: "java", starter: `import java.util.*;\n\npublic class Main {\n    static class TreeNode {\n        int value; TreeNode left, right;\n        TreeNode(int value) { this.value = value; }\n    }\n\n    static void inorder(TreeNode node, List<Integer> values) {\n        if (node == null) return;\n        inorder(node.left, values);\n        values.add(node.value);\n        inorder(node.right, values);\n    }\n}` }
};

const treePrompts = ["Explain inorder traversal", "How do I delete a BST node?", "What is the LCA?", "When should I use BFS?"];
const fallbackQuestion = { id: "inorder", title: "Binary Tree Inorder Traversal", difficulty: "Easy", prompt: "Given the root of a binary tree, return the inorder traversal of its node values.", starter: "def inorder_traversal(root):\n    # Write your solution\n    pass", test_cases: [["root = [1,null,2,3]", "[1,3,2]"], ["root = []", "[]"]] };
const fallbackQuestions = [
  fallbackQuestion,
  ["max-depth", "Maximum Depth of Binary Tree", "Easy", "max_depth"], ["same-tree", "Same Tree", "Easy", "is_same_tree"], ["invert", "Invert Binary Tree", "Easy", "invert_tree"], ["symmetric", "Symmetric Tree", "Easy", "is_symmetric"], ["diameter", "Diameter of Binary Tree", "Easy", "diameter_of_binary_tree"], ["balanced", "Balanced Binary Tree", "Easy", "is_balanced"], ["level-order", "Binary Tree Level Order Traversal", "Medium", "level_order"], ["right-view", "Binary Tree Right Side View", "Medium", "right_side_view"], ["good-nodes", "Count Good Nodes", "Medium", "good_nodes"], ["validate-bst", "Validate Binary Search Tree", "Medium", "is_valid_bst"], ["kth-smallest", "Kth Smallest Element in a BST", "Medium", "kth_smallest"], ["lca-bst", "LCA of a BST", "Medium", "lowest_common_ancestor"], ["lca-binary", "LCA of a Binary Tree", "Medium", "lowest_common_ancestor"], ["build-tree", "Construct Tree from Preorder and Inorder", "Medium", "build_tree"], ["max-path", "Binary Tree Maximum Path Sum", "Hard", "max_path_sum"], ["serialize", "Serialize and Deserialize Binary Tree", "Hard", "serialize"], ["trie", "Implement Trie", "Medium", "insert"], ["heap", "Kth Largest Element", "Medium", "find_kth_largest"], ["path-sum", "Path Sum", "Easy", "has_path_sum"]
].map((item) => Array.isArray(item) ? ({ id: item[0], title: item[1], difficulty: item[2], prompt: `Solve the Tree DSA problem: ${item[1]}. Implement the requested function and consider empty trees and single-node trees.`, starter: `def ${item[3]}(root):\n    # Write your solution\n    pass`, test_cases: [["root = [1,2,3]", "Expected result depends on the problem"], ["root = []", "Handle the empty tree"]] }) : item);
const tutorApi = process.env.NEXT_PUBLIC_TUTOR_API_URL || "http://localhost:8000/api/tutor";

function testCasesFor(question) {
  if (question.test_cases?.length) return question.test_cases;
  if (question.examples) {
    const [input = "See problem description", output = ""] = question.examples.split("\nOutput:");
    return [[input.replace("Input: ", ""), output], ["Edge case: empty tree", "Use the expected empty-tree result"]];
  }
  return fallbackQuestion.test_cases;
}

function challengeStarter(question, targetLanguage) {
  const match = question.starter?.match(/def\s+([a-zA-Z_]\w*)|class\s+([a-zA-Z_]\w*)/);
  const name = match?.[1] || match?.[2] || "solve";
  if (targetLanguage === "python") return question.starter || fallbackQuestion.starter;
  if (targetLanguage === "javascript") return `function ${name}(root) {\n  // Write your solution\n}\n`;
  return `class Solution {\n    public Object ${name}(Object root) {\n        // Write your solution\n        return null;\n    }\n}\n`;
}

export default function TutorApp() {
  const [activeView, setActiveView] = useState("chat");
  const [language, setLanguage] = useState("javascript");
  const [code, setCode] = useState(languages.javascript.starter);
  const [output, setOutput] = useState("Choose a language and click Run.");
  const [running, setRunning] = useState(false);
  const [asking, setAsking] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([{ role: "assistant", text: "I’m your Tree DSA tutor. Ask about binary trees, BSTs, traversals, heaps, tries, or LCA." }]);
  const [questions, setQuestions] = useState(fallbackQuestions);
  const [selectedQuestion, setSelectedQuestion] = useState(fallbackQuestion);

  useEffect(() => {
    fetch(tutorApi.replace(/\/api\/tutor$/, "/api/questions"))
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then((data) => { if (data.length) { setQuestions(data); setSelectedQuestion(data[0]); } })
      .catch(() => {});
  }, []);

  function changeLanguage(nextLanguage) {
    setLanguage(nextLanguage);
    setCode(activeView === "editor" ? challengeStarter(selectedQuestion, nextLanguage) : languages[nextLanguage].starter);
    setOutput(`Ready to run ${languages[nextLanguage].label} tree code.`);
  }
  async function runCode() {
    setRunning(true); setOutput("Running...");
    try {
      const response = await fetch("/api/run", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ language, code }) });
      const data = await response.json();
      setOutput([data.stdout, data.stderr].filter(Boolean).join("") || (data.ok ? "Process exited successfully with no output." : "Execution failed."));
    } catch { setOutput("Error: Could not reach the code runner."); }
    finally { setRunning(false); }
  }
  async function askTutor(prompt = question) {
    if (!prompt.trim() || asking) return;
    setMessages((current) => [...current, { role: "user", text: prompt }]); setQuestion(""); setAsking(true);
    try {
      const response = await fetch(tutorApi, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ code, output, question: prompt, language }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Tutor request failed.");
      setMessages((current) => [...current, { role: "assistant", text: data.answer, sources: data.sources?.length ? `Knowledge: ${data.sources.join(" · ")}` : "" }]);
    } catch (error) { setMessages((current) => [...current, { role: "assistant", text: error.message || "Tutor request failed. Please try again." }]); }
    finally { setAsking(false); }
  }
  const outputIsError = /error|exception|failed/.test(output.toLowerCase());

  return <main className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-icon"><Code2 size={20} /></div><div><div className="brand-title">Tree DSA Tutor</div><div className="brand-subtitle">RAG-powered learning workspace</div></div></div><div className="tree-badge"><BookOpen size={14} /> Tree knowledge base</div></header>
    <section className="app-layout">
      <nav className="sidebar" aria-label="Workspace navigation"><button className={activeView === "chat" ? "nav-item active" : "nav-item"} onClick={() => setActiveView("chat")}><MessageCircle size={19} /><span>Chat</span></button><button className={activeView === "editor" ? "nav-item active" : "nav-item"} onClick={() => setActiveView("editor")}><Code2 size={19} /><span>Code Editor</span></button></nav>
      {activeView === "chat" ? <section className="chat-page panel"><div className="chat-page-header"><div className="bot-icon"><Bot size={20} /></div><div><div className="panel-title">Tree DSA chat</div><div className="muted">Answers are grounded in the local tree knowledge base.</div></div></div><div className="messages">{messages.map((message, index) => <div key={index} className={`chat-message ${message.role}`}><div>{message.text}</div>{message.sources && <small>{message.sources}</small>}</div>)}{asking && <div className="chat-message assistant">Thinking…</div>}</div><div className="quick-actions">{treePrompts.map((prompt) => <button key={prompt} onClick={() => askTutor(prompt)}>{prompt}</button>)}</div><div className="chat-input"><textarea value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); askTutor(); } }} placeholder="Ask a Tree DSA question…" rows={3} /><button onClick={() => askTutor()} disabled={asking} aria-label="Ask tree tutor"><Send size={17} /></button></div></section> : <section className="editor-page"><div className="editor-toolbar"><div><div className="panel-title"><Code2 size={16} /> Tree challenge</div><div className="muted">Choose a problem, write your solution, then run it.</div></div><div className="top-actions"><button className="ghost-button" onClick={() => setCode(challengeStarter(selectedQuestion, language))}><RotateCcw size={16} /> Reset</button><button className="run-button" onClick={runCode} disabled={running}><Play size={16} fill="currentColor" />{running ? "Running..." : "Run"}</button></div></div><div className="leetcode-layout"><aside className="problem-panel panel"><select className="problem-select" value={selectedQuestion.id} onChange={(e) => { const next = questions.find((item) => item.id === e.target.value); setSelectedQuestion(next); setLanguage("python"); setCode(challengeStarter(next, "python")); }}>{questions.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}</select><h2>{selectedQuestion.title}</h2><span className={`difficulty ${selectedQuestion.difficulty.toLowerCase()}`}>{selectedQuestion.difficulty}</span><p>{selectedQuestion.prompt}</p><div className="tree-reference"><strong>Tree representation</strong><pre>      1{`\n`}     / \\{`\n`}    2   3{`\n`}   / \\{`\n`}  4   5</pre><small>Level-order array: [1,2,3,4,5]</small></div><h3>Examples</h3>{testCasesFor(selectedQuestion).map(([input, expected], index) => <div className="test-case" key={index}><strong>Example {index + 1}</strong><pre>Input: {input}{"\n"}Output: {expected}</pre></div>)}<h3>Constraints</h3><p className="constraints">Use O(n) time where possible. Handle null/empty trees and duplicate values when the problem permits them.</p></aside><div className="editor-split"><div className="panel editor-panel"><div className="panel-header"><div className="panel-title">Solution — implement only the function</div><select className="language-select" value={language} onChange={(e) => changeLanguage(e.target.value)}>{Object.entries(languages).map(([key, item]) => <option key={key} value={key}>{item.label}</option>)}</select></div><div className="editor-wrap"><Editor height="100%" language={languages[language].monaco} theme="vs-dark" value={code} onChange={(value) => setCode(value ?? "")} options={{ minimap: { enabled: false }, fontSize: 14, padding: { top: 16 }, automaticLayout: true, tabSize: language === "python" ? 4 : 2, wordWrap: "on", scrollBeyondLastLine: false }} /></div></div><div className="panel terminal-panel"><div className="panel-header"><div className="panel-title"><Terminal size={16} /> Test output</div><span className={`status ${outputIsError ? "error" : "success"}`}>{outputIsError ? <XCircle size={14} /> : <CheckCircle2 size={14} />}{outputIsError ? "Error" : "Output"}</span></div><pre className="terminal-output">{output}</pre><div className="terminal-chat"><div className="panel-title"><Bot size={15} /> Need a hint?</div><button onClick={() => { setActiveView("chat"); askTutor(`I am solving ${selectedQuestion.title}. Give me a hint without the full solution.`); }}>Ask AI for a hint</button><button onClick={() => { setActiveView("chat"); askTutor(`I am solving ${selectedQuestion.title}. Help me fix this error: ${output}`); }}>Fix terminal error</button></div></div></div></div></section>}
    </section>
  </main>;
}

# 🤖 Dev Logger Agent

> An AI agent that reads your git history, understands your code, and writes your daily dev log — automatically.

Point it at any git repository and it autonomously inspects commits, diffs, and source files to produce a structured, human-readable development log. No more forgetting what you worked on.

---

## ✨ Demo

```bash
$ python main.py --path ./leadwall --date 2026-03-10
```

```
╭──────────────────────────── 🤖 Starting ────────────────────────────╮
│ Dev Logger Agent                                                     │
│ Repo: /home/karthik/Documents/Development/Codes/leadwall             │
│ Date: 2026-03-10                                                     │
│ Model: llama-3.3-70b-versatile                                       │
╰──────────────────────────────────────────────────────────────────────╯

## 🗓️ Dev Log — 2026-03-10

**Project:** leadwall | **Branch:** main

### 📌 Summary
Session focused on Firebase Anonymous Authentication integration.
Users can now participate without creating an account, reducing
onboarding friction significantly.

### ✅ What Was Built / Changed
- Anonymous auth flow with Firebase SDK
- AuthContext provider with React hooks
- Mobile navbar responsiveness fix

### 📁 Key Files Modified
- `src/auth/AuthContext.tsx` — new context provider for auth state
- `src/components/Navbar.tsx` — CSS fix for mobile breakpoints
- `src/config/firebase.ts` — added anonymous auth initialization

### 🧠 Engineering Decisions
- Chose anonymous auth to minimize onboarding friction for demo users
- Deferred persistent auth (email/Google) to v2

### 🚧 TODOs / Open Threads
- Firebase security rules need tightening before production
- Custom domain setup pending
```

---

## 🏗️ How It Works

The agent uses a **ReAct (Reasoning + Acting)** loop — it decides which tools to call, observes the results, and iterates until it has enough context to write a complete log. This is not just a script that dumps `git log` into an LLM.

```
CLI (main.py)
      ↓
 ReAct Agent (LangGraph)
  ↙    ↓      ↓      ↘
get_repo  get_commits  list_changed_files  get_diff  read_file
  ↘         ↓        ↙
   Structured Markdown Log
         ↓
  logs/YYYY-MM-DD.md
```

The agent has 5 tools it calls autonomously:

| Tool | What it does |
|------|-------------|
| `get_repo_info` | Repo name, branch, remote, commit count |
| `get_commits` | Commits for the day with messages and timestamps |
| `list_changed_files` | All files touched across the day's commits |
| `get_diff` | Code diff for a specific commit |
| `read_file` | Read current file contents for deeper context |

---

## 🚀 Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/K4rthik14/dev-logger-agent
cd dev-logger-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure your LLM

**Option A — Groq (cloud, best quality):**
```bash
cp .env.example .env
# Add your free API key from https://console.groq.com
```

**Option B — Ollama (local, no rate limits, private):**
```bash
ollama pull qwen3.5:9b
# No API key needed
```

### 3. Run it

```bash
# Log today's work
python main.py --path /path/to/your/repo

# Log a specific date
python main.py --path ./my-project --date 2026-03-10

# Log a date range (skips days with no commits)
python main.py --path ./my-project --since 2026-03-01

# Use local Ollama instead of Groq
python main.py --path ./my-project --local --model qwen3.5:9b

# Don't save, just print
python main.py --path . --no-save
```

---

## 🔀 LLM Backends

| Mode | Command | Best for |
|------|---------|----------|
| ☁️ Groq (default) | `python main.py --path .` | Best quality logs |
| 🖥️ Local Ollama | `python main.py --path . --local --model qwen3.5:9b` | Private repos, no rate limits |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent framework | [LangGraph](https://langchain-ai.github.io/langgraph/) (ReAct) |
| Cloud LLM | [Groq](https://groq.com) + Llama 3.3 70B (free tier) |
| Local LLM | [Ollama](https://ollama.com) (any model) |
| Git access | [GitPython](https://gitpython.readthedocs.io) |
| CLI | [Typer](https://typer.tiangolo.com) |
| Terminal UI | [Rich](https://rich.readthedocs.io) |

---

## 📁 Project Structure

```
dev-logger-agent/
├── dev_logger/
│   ├── __init__.py
│   ├── tools.py      # LangChain tools (git operations)
│   ├── agent.py      # ReAct agent + LLM backend switching
│   └── prompts.py    # System prompt + log format
├── logs/             # Generated logs saved here
├── main.py           # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 Sample Log Output

```markdown
## 🗓️ Dev Log — 2026-03-21

**Project:** dev-logger-agent | **Branch:** main

### 📌 Summary
Added local LLM support via Ollama, allowing the agent to run
fully offline with no rate limits. Fixed date scoping bug where
--since was generating false logs for days with no commits.

### ✅ What Was Built / Changed
- Local Ollama backend via --local flag
- Fixed iter_commits date scoping (after + before)
- Added skip logic for days with no commits in --since range

### 📁 Key Files Modified
- `dev_logger/agent.py` — added build_agent local/cloud switching
- `dev_logger/tools.py` — fixed date range filter
- `main.py` — added --local flag and skip-empty-day logic

### 🧠 Engineering Decisions
- Kept Groq as default for quality; Ollama as opt-in for privacy
- Used before= filter in iter_commits to scope to exact day

### 🚧 TODOs / Open Threads
- Add rate limit retry with exponential backoff for Groq
- Consider adding --output-format flag (json, markdown)
```

---

## 📝 License

MIT# 🤖 Dev Logger Agent

> An AI agent that reads your git history, understands your code, and writes your daily dev log — automatically.

Point it at any git repository and it autonomously inspects commits, diffs, and source files to produce a structured, human-readable development log. No more forgetting what you worked on.

---

## ✨ Demo

```bash
$ python main.py --path ./leadwall --date 2026-03-10
```

```
╭──────────────────────────── 🤖 Starting ────────────────────────────╮
│ Dev Logger Agent                                                     │
│ Repo: /home/karthik/Documents/Development/Codes/leadwall             │
│ Date: 2026-03-10                                                     │
│ Model: llama-3.3-70b-versatile                                       │
╰──────────────────────────────────────────────────────────────────────╯

## 🗓️ Dev Log — 2026-03-10

**Project:** leadwall | **Branch:** main

### 📌 Summary
Session focused on Firebase Anonymous Authentication integration.
Users can now participate without creating an account, reducing
onboarding friction significantly.

### ✅ What Was Built / Changed
- Anonymous auth flow with Firebase SDK
- AuthContext provider with React hooks
- Mobile navbar responsiveness fix

### 📁 Key Files Modified
- `src/auth/AuthContext.tsx` — new context provider for auth state
- `src/components/Navbar.tsx` — CSS fix for mobile breakpoints
- `src/config/firebase.ts` — added anonymous auth initialization

### 🧠 Engineering Decisions
- Chose anonymous auth to minimize onboarding friction for demo users
- Deferred persistent auth (email/Google) to v2

### 🚧 TODOs / Open Threads
- Firebase security rules need tightening before production
- Custom domain setup pending
```

---

## 🏗️ How It Works

The agent uses a **ReAct (Reasoning + Acting)** loop — it decides which tools to call, observes the results, and iterates until it has enough context to write a complete log. This is not just a script that dumps `git log` into an LLM.

```
CLI (main.py)
      ↓
 ReAct Agent (LangGraph)
  ↙    ↓      ↓      ↘
get_repo  get_commits  list_changed_files  get_diff  read_file
  ↘         ↓        ↙
   Structured Markdown Log
         ↓
  logs/YYYY-MM-DD.md
```

The agent has 5 tools it calls autonomously:

| Tool | What it does |
|------|-------------|
| `get_repo_info` | Repo name, branch, remote, commit count |
| `get_commits` | Commits for the day with messages and timestamps |
| `list_changed_files` | All files touched across the day's commits |
| `get_diff` | Code diff for a specific commit |
| `read_file` | Read current file contents for deeper context |

---

## 🚀 Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/K4rthik14/dev-logger-agent
cd dev-logger-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure your LLM

**Option A — Groq (cloud, best quality):**
```bash
cp .env.example .env
# Add your free API key from https://console.groq.com
```

**Option B — Ollama (local, no rate limits, private):**
```bash
ollama pull qwen3.5:9b
# No API key needed
```

### 3. Run it

```bash
# Log today's work
python main.py --path /path/to/your/repo

# Log a specific date
python main.py --path ./my-project --date 2026-03-10

# Log a date range (skips days with no commits)
python main.py --path ./my-project --since 2026-03-01

# Use local Ollama instead of Groq
python main.py --path ./my-project --local --model qwen3.5:9b

# Don't save, just print
python main.py --path . --no-save
```

---

## 🔀 LLM Backends

| Mode | Command | Best for |
|------|---------|----------|
| ☁️ Groq (default) | `python main.py --path .` | Best quality logs |
| 🖥️ Local Ollama | `python main.py --path . --local --model qwen3.5:9b` | Private repos, no rate limits |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent framework | [LangGraph](https://langchain-ai.github.io/langgraph/) (ReAct) |
| Cloud LLM | [Groq](https://groq.com) + Llama 3.3 70B (free tier) |
| Local LLM | [Ollama](https://ollama.com) (any model) |
| Git access | [GitPython](https://gitpython.readthedocs.io) |
| CLI | [Typer](https://typer.tiangolo.com) |
| Terminal UI | [Rich](https://rich.readthedocs.io) |

---

## 📁 Project Structure

```
dev-logger-agent/
├── dev_logger/
│   ├── __init__.py
│   ├── tools.py      # LangChain tools (git operations)
│   ├── agent.py      # ReAct agent + LLM backend switching
│   └── prompts.py    # System prompt + log format
├── logs/             # Generated logs saved here
├── main.py           # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 Sample Log Output

```markdown
## 🗓️ Dev Log — 2026-03-21

**Project:** dev-logger-agent | **Branch:** main

### 📌 Summary
Added local LLM support via Ollama, allowing the agent to run
fully offline with no rate limits. Fixed date scoping bug where
--since was generating false logs for days with no commits.

### ✅ What Was Built / Changed
- Local Ollama backend via --local flag
- Fixed iter_commits date scoping (after + before)
- Added skip logic for days with no commits in --since range

### 📁 Key Files Modified
- `dev_logger/agent.py` — added build_agent local/cloud switching
- `dev_logger/tools.py` — fixed date range filter
- `main.py` — added --local flag and skip-empty-day logic

### 🧠 Engineering Decisions
- Kept Groq as default for quality; Ollama as opt-in for privacy
- Used before= filter in iter_commits to scope to exact day

### 🚧 TODOs / Open Threads
- Add rate limit retry with exponential backoff for Groq
- Consider adding --output-format flag (json, markdown)
```

---

## 📝 License

MIT# 🤖 Dev Logger Agent

> An AI agent that reads your git history, understands your code, and writes your daily dev log — automatically.

Point it at any git repository and it autonomously inspects commits, diffs, and source files to produce a structured, human-readable development log. No more forgetting what you worked on.

---

## ✨ Demo

```bash
$ python main.py --path ./leadwall --date 2026-03-10
```

```
╭──────────────────────────── 🤖 Starting ────────────────────────────╮
│ Dev Logger Agent                                                     │
│ Repo: /home/karthik/Documents/Development/Codes/leadwall             │
│ Date: 2026-03-10                                                     │
│ Model: llama-3.3-70b-versatile                                       │
╰──────────────────────────────────────────────────────────────────────╯

## 🗓️ Dev Log — 2026-03-10

**Project:** leadwall | **Branch:** main

### 📌 Summary
Session focused on Firebase Anonymous Authentication integration.
Users can now participate without creating an account, reducing
onboarding friction significantly.

### ✅ What Was Built / Changed
- Anonymous auth flow with Firebase SDK
- AuthContext provider with React hooks
- Mobile navbar responsiveness fix

### 📁 Key Files Modified
- `src/auth/AuthContext.tsx` — new context provider for auth state
- `src/components/Navbar.tsx` — CSS fix for mobile breakpoints
- `src/config/firebase.ts` — added anonymous auth initialization

### 🧠 Engineering Decisions
- Chose anonymous auth to minimize onboarding friction for demo users
- Deferred persistent auth (email/Google) to v2

### 🚧 TODOs / Open Threads
- Firebase security rules need tightening before production
- Custom domain setup pending
```

---

## 🏗️ How It Works

The agent uses a **ReAct (Reasoning + Acting)** loop — it decides which tools to call, observes the results, and iterates until it has enough context to write a complete log. This is not just a script that dumps `git log` into an LLM.

```
CLI (main.py)
      ↓
 ReAct Agent (LangGraph)
  ↙    ↓      ↓      ↘
get_repo  get_commits  list_changed_files  get_diff  read_file
  ↘         ↓        ↙
   Structured Markdown Log
         ↓
  logs/YYYY-MM-DD.md
```

The agent has 5 tools it calls autonomously:

| Tool | What it does |
|------|-------------|
| `get_repo_info` | Repo name, branch, remote, commit count |
| `get_commits` | Commits for the day with messages and timestamps |
| `list_changed_files` | All files touched across the day's commits |
| `get_diff` | Code diff for a specific commit |
| `read_file` | Read current file contents for deeper context |

---

## 🚀 Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/K4rthik14/dev-logger-agent
cd dev-logger-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure your LLM

**Option A — Groq (cloud, best quality):**
```bash
cp .env.example .env
# Add your free API key from https://console.groq.com
```

**Option B — Ollama (local, no rate limits, private):**
```bash
ollama pull qwen3.5:9b
# No API key needed
```

### 3. Run it

```bash
# Log today's work
python main.py --path /path/to/your/repo

# Log a specific date
python main.py --path ./my-project --date 2026-03-10

# Log a date range (skips days with no commits)
python main.py --path ./my-project --since 2026-03-01

# Use local Ollama instead of Groq
python main.py --path ./my-project --local --model qwen3.5:9b

# Don't save, just print
python main.py --path . --no-save
```

---

## 🔀 LLM Backends

| Mode | Command | Best for |
|------|---------|----------|
| ☁️ Groq (default) | `python main.py --path .` | Best quality logs |
| 🖥️ Local Ollama | `python main.py --path . --local --model qwen3.5:9b` | Private repos, no rate limits |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent framework | [LangGraph](https://langchain-ai.github.io/langgraph/) (ReAct) |
| Cloud LLM | [Groq](https://groq.com) + Llama 3.3 70B (free tier) |
| Local LLM | [Ollama](https://ollama.com) (any model) |
| Git access | [GitPython](https://gitpython.readthedocs.io) |
| CLI | [Typer](https://typer.tiangolo.com) |
| Terminal UI | [Rich](https://rich.readthedocs.io) |

---

## 📁 Project Structure

```
dev-logger-agent/
├── dev_logger/
│   ├── __init__.py
│   ├── tools.py      # LangChain tools (git operations)
│   ├── agent.py      # ReAct agent + LLM backend switching
│   └── prompts.py    # System prompt + log format
├── logs/             # Generated logs saved here
├── main.py           # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📄 Sample Log Output

```markdown
## 🗓️ Dev Log — 2026-03-21

**Project:** dev-logger-agent | **Branch:** main

### 📌 Summary
Added local LLM support via Ollama, allowing the agent to run
fully offline with no rate limits. Fixed date scoping bug where
--since was generating false logs for days with no commits.

### ✅ What Was Built / Changed
- Local Ollama backend via --local flag
- Fixed iter_commits date scoping (after + before)
- Added skip logic for days with no commits in --since range

### 📁 Key Files Modified
- `dev_logger/agent.py` — added build_agent local/cloud switching
- `dev_logger/tools.py` — fixed date range filter
- `main.py` — added --local flag and skip-empty-day logic

### 🧠 Engineering Decisions
- Kept Groq as default for quality; Ollama as opt-in for privacy
- Used before= filter in iter_commits to scope to exact day

### 🚧 TODOs / Open Threads
- Add rate limit retry with exponential backoff for Groq
- Consider adding --output-format flag (json, markdown)
```

---

## 📝 License

Apache
### Read before
This repo is a fork of the original [ayushh0110/ScreenMind](https://github.com/ayushh0110/ScreenMind) <br>
All new code and changes are done using AI tools, mainly [qwen-coder](https://coder.qwen.ai/) <br>
The main focus here is to separate LLM inference backend and use any OpenAI chat completions API, since I want to run this on a miniPC without dedicated GPU, and use another high-end desktop to do the heavy-lifting model inferencing for it.

<div align="center">
<br>

<img src="https://img.shields.io/badge/🧠_ScreenMind-Your_AI_Memory-8B5CF6?style=for-the-badge&labelColor=0a0e1a" alt="ScreenMind" height="40">

<br><br>


**Captures your screen → Analyzes with LLM → Builds a searchable AI memory**<br>
**100% private. Your data stays local.**

<br>

[![CI](https://github.com/ayushh0110/ScreenMind/actions/workflows/ci.yml/badge.svg)](https://github.com/ayushh0110/ScreenMind/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License MIT](https://img.shields.io/badge/License-MIT-10B981?style=flat-square)](LICENSE)
[![MCP Ready](https://img.shields.io/badge/MCP-Claude_%7C_Cursor_%7C_VSCode-F59E0B?style=flat-square)](MCP_SETUP.md)

<br>

[**Features**](#-features) · [**Quick Start**](#-quick-start) · [**Architecture**](#-architecture) · [**Agent Platform**](#-agent-platform) · [**MCP**](#-mcp-server-claude--cursor--vs-code) · [**API**](#-api-reference)

<br>

![Timeline — AI-analyzed screen activity feed](docs/screenshots/timeline.png)

| Agents | 
|:---:|
| ![Agents](docs/screenshots/agents.png) |

<br>

**💬 Chat in Action** — *Ask anything about your screen history*

![Chat Demo — conversational AI with screen memory](docs/screenshots/chat-demo.gif)

</div>

<br>

> **Microsoft showed the world wants screen-aware AI with Recall.** But Recall stores data in plaintext, sends telemetry, and was met with massive privacy backlash. ScreenMind is the open-source, privacy-first alternative — every screenshot analyzed, every insight generated, every search result — all computed locally.
>
> It's not just a screen recorder. It's an **AI memory** you can talk to, search through, and build automations on top of.

---


## ✨ Features

### 🧠 Core Intelligence

- **📸 Smart Capture** — Content-change detection, not a fixed timer. Captures when your screen *actually* changes.
- **🔬 LLM Vision Analysis** — Every screenshot analyzed: app detection, activity categorization, mood, scene description, spatial layout regions. Uses any OpenAI-compatible API endpoint.
- **🔍 Hybrid Search** — Semantic embeddings (MiniLM-L6-v2 local) + FTS5 keyword search. Find anything by *meaning*, not just keywords.
- **💬 Chat with Memory** — Conversational RAG with follow-up support. Ask "what did Alex say on Discord?" → get the actual message.
- **🧠 Model Hub** — In-app model download with live progress tracking. Chat and Summary are locked with witty brain animations until the model is ready — then auto-unlock. No terminal needed.
- **🎙️ Voice Memos** — Hold `Ctrl+Shift+V` → transcribe audio. Screenshot captured alongside. *(Note: Audio transcription feature temporarily disabled - will be re-enabled with a more robust workflow in the future)*
- **🎤 Meeting Transcription** — Auto-detects Zoom/Teams/Meet, records audio, transcribes, generates structured summaries. *(Note: Temporarily disabled)*
- **📊 Analytics Dashboard** — Category breakdown, top apps, hourly heatmap, meeting stats, focus metrics.
- **⏪ Day Rewind** — Timelapse playback of your entire day with play/pause/scrub/speed controls.

### ⚡ Performance

- **Three Analysis Modes** — Accurate (deep thinking + layout), Balanced (thinking), or Fast (no thinking). You choose.
- **Per-App pHash Cache** — 3-tier caching with app-aware staleness. Communication apps refresh faster than IDEs. Significantly fewer inference calls.
- **Chat-First GPU Priority** — Chat cancels in-flight analysis instantly. GPU freed in <1s.
- **Auto-Pause Heavy Apps** — Games, video editors, 3D software detected → capture pauses automatically.

### 🔒 Privacy & Security

- **100% Local Embeddings** — MiniLM-L6-v2 runs locally for semantic search.
- **Flexible LLM Backend** — Use any OpenAI-compatible API (local or cloud). You control where your data goes.
- **Sensitive Data Filter** — Auto-redacts credit cards, SSNs, API keys, passwords before storage.
- **Encryption at Rest** — AES encryption for screenshots (Fernet + OS keyring).
- **Dashboard PIN Lock** — Session-based auth with configurable auto-lock timeout.
- **Incognito Mode** — One-click pause. Nothing recorded.

<details>
<summary><b>🔌 Integrations & Extensibility</b></summary>

<br>

| Integration | Description |
|---|---|
| 🤖 **Agent Platform** | Build automations in Markdown (English) or Python. Drop a file, get an agent. |
| 🔌 **MCP Server** | Expose screen history to Claude Desktop, Cursor, VS Code |
| 📓 **Obsidian** | Auto-sync daily summaries to your vault |
| 📋 **Notion** | Push summaries to a Notion database |
| 🪝 **Webhooks** | Fire events to Slack, Discord, IFTTT (HMAC signed, auto-retry) |
| 🔔 **Smart Notifications** | Distraction alerts, break reminders |
| ⭐ **Auto-Bookmark** | Keyword triggers (`git push`, `deploy`) auto-flag important moments |

</details>

### ⌨️ System-Wide Hotkeys

| Hotkey | Action |
|---|---|
| `Ctrl+Shift+B` | 📸 Instant bookmarked capture |
| `Ctrl+Shift+P` | ⏸ Toggle pause/resume |
| `Ctrl+Shift+V` | 🎤 Hold to record voice memo |

> All hotkeys customizable from Settings.

---

## 🚀 Quick Start

> **Requirements:** Python 3.10+ · GPU recommended (4GB+ VRAM) for local LLM servers · Disk space for model weights (varies by model)

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ayushh0110/ScreenMind.git
cd ScreenMind
```

#### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -e ".[ai]"
```

#### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your LLM API configuration:

```ini
# Custom LLM API Endpoint (OpenAI-compatible Chat Completions)
LLM_API_BASE_URL=http://localhost:11434/v1    # e.g., Ollama, vLLM, or any OpenAI-compatible server
LLM_API_KEY=your-api-key-if-required          # Leave empty if not required
LLM_MODEL_NAME=gemma4:e2b                     # Model identifier to use

# Embedding API Endpoint (OpenAI-compatible Embeddings)
# Uses all-MiniLM-L6-v2 model (384 dimensions) - fixed for vector compatibility
EMBED_API_BASE_URL=http://localhost:11434/v1  # Can be same or different from LLM endpoint
EMBED_API_KEY=                                # API key for embedding endpoint (if required)
EMBED_API_BATCH_SIZE=8                        # Batch size for embedding API calls (1-32)

# LLM Concurrency (for parallel task processing)
LLM_API_CONCURRENCY=1                         # Number of concurrent LLM API calls (1-10)

# Capture Settings
CAPTURE_INTERVAL=40
SCREENSHOT_QUALITY=70
DATA_DIR=~/.screenmind

# Performance Mode
PERFORMANCE_MODE=balanced    # minimal, balanced, or maximum

# Analysis Mode
ANALYSIS_MODE=fast           # fast, balanced

# Privacy
BLOCKED_APPS=
HOTKEY_BOOKMARK=ctrl+shift+b
```

> **Note:** You can also configure most settings from the **Settings** tab in the web dashboard.

#### 5️⃣ Run ScreenMind

```bash
python -m screenmind
```

#### 6️⃣ Open Dashboard → **http://127.0.0.1:7777**

On first run, ScreenMind will:
- Create `~/.screenmind/` for data storage
- Show the welcome screen to set up an optional PIN
- Open the **Model Hub** — configure your LLM API endpoint and download required models
- Chat and Summary features become available once the LLM is configured

<details>
<summary><b>🔧 Optional: Use with Different LLM Backends</b></summary>

<br>

ScreenMind supports any OpenAI-compatible API endpoint. Common setups:

**Ollama (local):**
```ini
LLM_API_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=
LLM_MODEL_NAME=gemma4:e2b
```

**vLLM (local GPU):**
```ini
LLM_API_BASE_URL=http://localhost:8000/v1
LLM_API_KEY=
LLM_MODEL_NAME=google/gemma-2b-it
```

**Cloud Provider:**
```ini
LLM_API_BASE_URL=https://api.provider.com/v1
LLM_API_KEY=sk-your-key-here
LLM_MODEL_NAME=gemma-2b
```

</details>

---

## 🏗️ Architecture

> For a full deep-dive into threading, caching, search internals, and the privacy pipeline, see [**ARCHITECTURE.md**](ARCHITECTURE.md).

```
┌─────────────────────────────────────────────────────────────────────┐
│                          ScreenMind                                  │
│                                                                     │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────────────────┐ │
│  │  Capture   │───▶│  Async Queue │───▶│    Analysis Worker      │ │
│  │  Worker    │    │  (max: 100)  │    │                         │ │
│  │            │    └──────────────┘    │  ┌───────────────────┐  │ │
│  │ • Screen   │                        │  │  Per-App pHash    │  │ │
│  │ • Window   │                        │  │  Cache (3-tier)   │  │ │
│  │ • Dedup    │                        │  └───────────────────┘  │ │
│  │ • A11y     │                        │           │             │ │
│  │ • Privacy  │                        │           ▼             │ │
│  └────────────┘                        │  ┌───────────────────┐  │ │
│                                        │  │   EasyOCR         │  │ │
│  ┌────────────┐                        │  │   (text extract)  │  │ │
│  │   Audio    │                        │  └───────────────────┘  │ │
│  │   Worker   │                        │           │             │ │
│  │            │                        │           ▼             │ │
│  │ • Meeting  │                        │  ┌───────────────────┐  │ │
│  │   detect   │                        │  │   LLM API     │  │ │
│  │ • Record   │                        │  │   (OpenAI-compatible) │  │ │
│  │ • Transcr. │                        │  │   Vision + Text  │  │ │
│  └────────────┘                        │  └───────────────────┘  │ │
│                                        │           │             │ │
│  ┌────────────┐                        │           ▼             │ │
│  │   Agent    │                        │  ┌───────────────────┐  │ │
│  │  Scheduler │                        │  │  Layout Analyzer  │  │ │
│  │            │                        │  │  (spatial OCR)    │  │ │
│  │ • .md AI   │                        │  └───────────────────┘  │ │
│  │ • .py code │                        │           │             │ │
│  └────────────┘                        │           ▼             │ │
│                                        │  ┌───────────────────┐  │ │
│                                        │  │  MiniLM-L6-v2     │  │ │
│                                        │  │  (embeddings)     │  │ │
│                                        │  └───────────────────┘  │ │
│                                        └─────────────────────────┘ │
│                                                    │               │
│                                                    ▼               │
│                                        ┌───────────────────┐       │
│                                        │   SQLite (WAL)    │       │
│                                        │   + FTS5 index    │       │
│                                        └─────────┬─────────┘       │
│                                                  │                 │
│  ┌───────────────────────────────────────────────┘                 │
│  │                                                                 │
│  ▼                                                                 │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                    FastAPI REST Server                         │ │
│  │  /timeline · /search · /chat · /stats · /agents · /mcp       │ │
│  │                                                               │ │
│  │  ┌───────────────────────────────────────────────────────┐   │ │
│  │  │           Web Dashboard (Vanilla JS SPA)               │   │ │
│  │  │  Timeline · Chat · Search · Analytics · Agents · Settings │ │
│  │  └───────────────────────────────────────────────────────┘   │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Multi-Model AI Pipeline

```
Screenshot → EasyOCR (text) → LLM API (understanding) → MiniLM (embeddings) → SQLite + FTS5
                                     ↑
                              OCR text fed as context
                              (LLM sees image + reads text)
```

Four AI models working in concert, with LLM as the brain:
1. **EasyOCR** — extracts raw screen text
2. **LLM API** — understands what you're doing (vision + reasoning)
3. **MiniLM-L6-v2** — generates semantic vectors for natural language search
4. **FTS5** — indexes text for instant keyword search

---

## 🤖 Agent Platform

ScreenMind includes a full agent/plugin system. Build any automation on top of your screen data.

### Two Modes

| Mode | File Type | For | Example |
|---|---|---|---|
| 🤖 AI Agent | `.md` | Everyone | Write a prompt in English → LLM runs it on your data |
| 🐍 Python Plugin | `.py` | Developers | Full code with SDK access, state persistence, LLM calls |

### Markdown Agent Example

```markdown
---
name: Daily Focus Report
schedule: every 6h
data: timeline, apps, mood
output: local, obsidian
---

Analyze my screen activity and generate a focus report:
- How many hours of deep work vs shallow work?
- What were my main distractions?
- Give me a focus score out of 10.
```

Drop this file in `~/.screenmind/agents/` — it runs automatically.

### Python Plugin SDK

```python
from screenmind.screenmind_sdk import ScreenMindSDK

sdk = ScreenMindSDK("my-tracker")

# Get today's activities filtered by app
activities = sdk.get_activities(app="Chrome", limit=20)

# Persistent state across runs
last_count = sdk.load_state("url_count", 0)
urls = sdk.get_urls_visited()
sdk.save_state("url_count", len(urls))

# Ask LLM (GPU-safe — waits for idle)
insight = sdk.ask_gemma(f"Summarize these URLs: {urls}")
print(insight)
```

### Data Selectors (Frontmatter)

Markdown agents declare what data they need:

| Selector | Injects |
|---|---|
| `timeline` | Recent activities with timestamps, apps, summaries |
| `apps` | App usage counts + category breakdown |
| `urls` | URLs visited (extracted from browser address bars) |
| `meetings` | Meeting summaries and durations |
| `mood` | Mood/sentiment from screen analysis |

Data injection auto-scales to your model's context window.

### 4 Agents Ship Built-In

- **daily-journal.md** — First-person journal entry from your day
- **focus-report.md** — Focus score, deep work hours, distractions
- **meeting-actions.md** — Extract action items from meeting transcripts
- **code-changelog.md** — Summarize coding activity (commits, files, repos)

---

## 🔌 MCP Server (Claude / Cursor / VS Code)

ScreenMind exposes your screen history to any MCP-compatible AI tool:

```bash
python -m screenmind.mcp_server  # stdio transport
```

**Claude Desktop config** (`~/.claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "screenmind": {
      "command": "python",
      "args": ["C:/path/to/screenmind/mcp_server.py"]
    }
  }
}
```

### Tools Available

| Tool | Description |
|---|---|
| `search_screen` | Semantic + keyword search across all history |
| `get_recent_activity` | Last N activities with full details |
| `get_activity_by_time` | Activities for a specific date/time range |
| `get_daily_summary` | AI-generated daily summary |
| `capture_now` | Trigger instant screenshot |
| `get_stats` | Usage statistics |
| `search_audio` | Search meeting transcripts |
| `get_screenshot` | Retrieve screenshot path by activity ID |

---

## 📡 API Reference

Full Swagger docs at `http://127.0.0.1:7777/docs`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/status` | System health, worker stats |
| `GET` | `/api/timeline?date=2026-05-21` | Activities for a date |
| `GET` | `/api/search?q=debugging auth` | Hybrid semantic + keyword search |
| `POST` | `/api/chat` | Conversational AI with screen memory (SSE stream) |
| `GET` | `/api/stats?range=day` | Analytics (categories, apps, meetings) |
| `GET` | `/api/rewind?date=2026-05-21` | Timelapse frames |
| `POST` | `/api/summary/generate` | Generate AI daily summary |
| `GET` | `/api/agents` | List all agents |
| `POST` | `/api/agents/{name}/run` | Trigger agent execution |
| `POST` | `/api/capture/pause` | Pause capture |
| `POST` | `/api/incognito/toggle` | Toggle incognito mode |

---

<details>
<summary><h2>⚙️ Configuration</h2></summary>

<br>

All settings configurable via `.env`, environment variables, or the **Settings** dashboard (persists to `settings.json`).

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPTURE_INTERVAL` | `40` | Seconds between captures |
| `ANALYSIS_MODE` | `fast` | `fast` (~12s), `balanced` (~40s), or `merged` (~76s, accurate) |
| `PERFORMANCE_MODE` | `balanced` | GPU layers: `minimal` / `balanced` / `maximum` |
| `BLOCKED_APPS` | *(empty)* | Comma-separated apps to never capture |
| `MEETING_TRANSCRIPTION` | `false` | Auto-transcribe when meeting apps detected |
| `RETENTION_DAYS` | `7` | Auto-delete data older than N days (0 = forever) |
| `ENCRYPTION_ENABLED` | `false` | Encrypt screenshots at rest |
| `SENSITIVE_FILTER_ENABLED` | `true` | Redact credit cards, SSNs, API keys |
| `SCREENMIND_LOG_LEVEL` | `INFO` | Log verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `SCREENMIND_LOG_FILE` | *(none)* | Path to a log file (rotating, 10MB × 3 backups) |

> See `.env.example` for the full list.

</details>

---

## 🔧 Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Vision + Text AI** | LLM API (OpenAI-compatible) | Only model with vision + audio + reasoning that runs locally on 4GB VRAM |
| **Inference Server** | LLM server (LLM inference backend) | Direct GGUF inference, OpenAI-compatible API |
| **OCR** | EasyOCR | Extracts screen text fed to LLM as context |
| **Embeddings** | all-MiniLM-L6-v2 | 80MB, runs on CPU, 384-dim vectors for semantic search |
| **Backend** | FastAPI + Uvicorn | Async-first, auto-generated API docs |
| **Database** | SQLite (WAL) + FTS5 | Zero-config, concurrent reads, full-text search |
| **Capture** | mss + ctypes/UI Automation | Native screen capture + accessibility text extraction |
| **Wayland Capture** | grim (wlroots) / XDG Portal | Automatic fallback; no X11 dependency on Wayland |
| **Frontend** | Vanilla JS + CSS | No build step, instant load, dark glassmorphism UI |
| **Platform** | Windows / macOS / Linux (X11 + Wayland) | Abstraction layer with OS-specific adapters |

---

### 🐧 Wayland Support

ScreenMind auto-detects Wayland sessions and uses compositor-native capture:

| Compositor | Capture | Window Detection | Notes |
|---|---|---|---|
| **Sway** | ✅ grim | ✅ swaymsg IPC | Full support |
| **Hyprland** | ✅ grim | ✅ hyprctl IPC | Full support |
| **Niri** | ✅ grim | ✅ niri msg IPC | Full support |
| **river / Wayfire / labwc** | ✅ grim | ⚠️ Title only (no IPC) | Capture works, app name may be unavailable |
| **GNOME (Mutter)** | ⚠️ XDG Portal | ❌ No IPC available | Portal prompts on every capture — not viable for background recording |
| **KDE (KWin)** | ⚠️ XDG Portal | ❌ No IPC available | Same as GNOME |

**Install grim** (recommended for wlroots compositors):
```bash
# Arch
sudo pacman -S grim

# Ubuntu / Debian (if available)
sudo apt install grim

# Fedora
sudo dnf install grim
```

**GNOME / KDE Wayland**: Best-effort only. Screenshots use the XDG Desktop Portal,
which prompts for permission on each capture — not viable for continuous background
recording. For full functionality, use an X11 session or a wlroots-based compositor with grim.

**Optional** (for portal fallback): `python3-gi` / `python-gobject` system package.

---

<details>
<summary><h2>📁 Project Structure</h2></summary>

<br>

```
screenmind/
├── screenmind/                    # Entry point — starts all services
├── config.py                  # Pydantic settings (env + runtime overrides)
├── LLM server setup             # Auto-detect + install LLM server
├── requirements.txt           # Full Python dependencies
├── requirements-test.txt      # Lightweight CI deps (no PyTorch)
│   ├── main.py              # MCP server for Claude/Cursor/VS Code
├── screenmind_sdk.py          # SDK for Python plugin agents
│
│   ├── capture/                   # Screenshot capture layer
│   ├── screen.py              # Capture facade (mss / Wayland backend)
│   ├── wayland.py             # Wayland backend (grim / XDG Portal)
│   ├── window.py              # Active window detection
│   ├── dedup.py               # Perceptual hash deduplication
│   ├── hotkey.py              # Global hotkeys (bookmark, pause, voice)
│   └── voice_recorder.py      # Mic recording for voice memos
│
│   ├── engine/                    # AI & intelligence layer
│   ├── analyzer.py            # LLM vision analysis (dual mode)
│   ├── llm_client.py          # LLM server client (chat, vision, audio)
│   ├── model_manager.py       # Server lifecycle, model download/switch
│   ├── embedder.py            # MiniLM semantic embeddings
│   ├── ocr.py                 # EasyOCR text extraction
│   ├── layout_analyzer.py     # Spatial OCR organization
│   ├── dev_context.py         # Git repo/branch/diff detection
│   ├── a11y_extractor.py      # Accessibility API text extraction
│   └── agent_runner.py        # Agent scheduling & execution
│
│   ├── workers/                   # Background processing
│   ├── capture_worker.py      # Smart capture loop + privacy filtering
│   ├── analysis_worker.py     # OCR → LLM → Layout → Embed → Store
│   └── audio_worker.py        # Meeting detection & transcription
│
│   ├── storage/                   # Data persistence
│   ├── database.py            # SQLite + FTS5 + migrations
│   └── models.py              # Pydantic data models
│
│   ├── privacy/                   # Privacy & security
│   ├── encryption.py          # Fernet AES encryption at rest
│   └── data_filter.py         # Sensitive data redaction
│
│   ├── platform_support/          # Cross-platform abstraction
│   ├── windows.py             # Win32 + UI Automation
│   ├── macos.py               # AppKit + AXUIElement
│   └── linux.py               # xdotool + AT-SPI
│
│   ├── integrations/              # External connections
│   ├── obsidian.py            # Vault markdown export
│   ├── notion.py              # Notion API export
│   ├── webhooks.py            # HTTP webhooks (HMAC, retry)
│   └── smart_notify.py        # Distraction/break notifications
│
│   ├── api/                       # REST API + dashboard
│   ├── server.py              # FastAPI app + auth middleware
│   ├── dependencies.py        # Shared state for routes
│   ├── routes/                # 16 route modules
│   └── static/                # Web dashboard (HTML + CSS + JS)
│
├── default_agents/            # 4 built-in agents
│   ├── daily-journal.md
│   ├── focus-report.md
│   ├── meeting-actions.md
│   └── code-changelog.md
│
├── tests/                     # pytest test suite (25 modules)
│   ├── conftest.py            # Shared fixtures
│   └── test_*.py              # Unit + integration tests
│
└── docs/
    └── BUILD_YOUR_OWN_AGENT.md
```

</details>

---

## 🛡️ Error Handling & Resilience

| Scenario | Behavior |
|----------|----------|
| **LLM server not found** | Auto-downloads correct binary from GitHub releases (CUDA/CPU auto-detected). Checks disk space first. |
| **Model not downloaded** | Model Hub shows lock screen with download cards. Progress tracked in UI. Chat/Summary locked until ready. |
| **GPU out of memory** | Detects OOM, retries with delay, re-queues on persistent failure. |
| **Duplicate frames** | pHash dedup skips identical screenshots (threshold: 8 hamming distance). |
| **Stale queue items** | Captures >3 min old auto-skipped. Backfilled during idle. |
| **App in blocklist** | Silently skips — no screenshot saved. |
| **Meeting app closed** | Process-alive check + silence detection + 5-min hard timeout. |
| **Chat during analysis** | Cancels in-flight inference, frees GPU in <1s, re-queues analysis. |
| **Crash recovery** | Stale meetings cleaned on startup. Unanalyzed entries backfilled. |

---

## 🎨 Dashboard

The web dashboard at `http://127.0.0.1:7777` features:

- **Timeline** — Browse activities by date with thumbnails, AI summaries, category badges
- **Chat** — Conversational AI with screen memory. Ask anything about your history. Locked with 🧠💤 brain animation until model is ready.
- **Search** — Semantic + keyword hybrid search with OCR highlighting on screenshots
- **Analytics** — Category charts, top apps, hourly heatmap, meeting stats
- **Rewind** — Timelapse player with play/pause/scrub/speed controls
- **Memos** — Voice memo list with audio player
- **Agents** — Create, edit, run, and monitor agents
- **Settings** — Model Hub (download/switch models with progress), Shortcuts, Capture, AI, Audio, Privacy, Automation, Integrations, Storage

Dark glassmorphism UI. No build step. Instant load.

---

## 🧪 Development

Run the test suite:

```bash
# Fast (lightweight deps — same as CI, ~2 min install)
pip install -r requirements-test.txt
pytest --cov=. --cov-report=term-missing -q

# Full (includes ML models — sentence-transformers, easyocr)
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov
pytest --cov=. --cov-report=term-missing -q
```

CI runs automatically on push/PR via GitHub Actions using the lightweight deps.

---

## 🤝 Contributing

Contributions welcome! Here are some high-impact areas:

- 🍎 **macOS/Linux testing** — platform adapters exist, need real hardware testing
- 🐳 **Docker container** — one-command setup
- 🧩 **Community agent registry** — share agents between users
- 🌐 **Browser extension** — richer URL/tab context
- 📤 **Export formats** — Markdown, CSV, JSON

---

## ⭐ Show Your Support

If you find ScreenMind useful, please consider:

- **⭐ Star this repo** — it helps others discover the project
- **🍴 Fork it** — build your own agents and features
- **🐛 Report issues** — help us improve
- **📣 Share it** — tell others about privacy-first AI

<div align="center">

<br>

<a href="https://github.com/ayushh0110/ScreenMind/stargazers"><img src="https://img.shields.io/github/stars/ayushh0110/ScreenMind?style=social" alt="Stars"></a>
<a href="https://github.com/ayushh0110/ScreenMind/network/members"><img src="https://img.shields.io/github/forks/ayushh0110/ScreenMind?style=social" alt="Forks"></a>

<br>

</div>

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

<br>

**Built with 🔒 Privacy-First · 🧠 Flexible LLM Backend · 🚀 Your Data Stays Local**

*Configurable LLM endpoint (local or cloud) + local MiniLM embeddings.*

<br>

<sub>Made with ❤️ by <a href="https://github.com/ayushh0110">ayushh0110</a></sub>

</div>

# PROJECT EXODUS — SYSTEM DOCUMENTATION

**Version:** 2.1  
**Lead Architect:** Vamsi  
**Core Identity:** Public AI Companion / Comprehensive Life Advisor.

---

## ⬡ 1. SYSTEM OVERVIEW
EXODUS is a modular, privacy-focused (local-first) AI companion designed to assist with every facet of human life—from productivity and coding to health and emotional support. It combines a high-speed **FastAPI** backend with a low-latency, cyberpunk-themed **Vanilla JS** interface.

---

## ⬡ 2. ARCHITECTURE & TECHNOLOGY
The project is built for speed and modularity:
- **Backend:** Python 3.10+ / FastAPI.
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (No heavy frameworks).
- **LLM Engine:** Google Gemini (via `google-generativeai`).
- **Semantic Memory:** **ChromaDB** (Vector store for PDF ingestion and long-term facts).
- **Persistent History:** **SQLite** (Stores multi-session chat history).
- **Web Intelligence:** DuckDuckGo Search API integration.

---

## ⬡ 3. CORE ENGINES
The backend logic is partitioned into distinct "Engines" for safety and intelligence:

### 🛡️ Guardian (`core/guardian.py`)
Responsible for ensuring output safety and monitoring "emotional drift." It validates all AI responses before they reach the UI.

### ⚖️ Rules Engine (`core/rules.py`)
Enforces the system's "Constitution." In the public version, it ensures the AI remains helpful and direct while blocking malicious intent.

### 🧠 The Brain (`core/brain.py`)
The central orchestrator. It manages intent routing, context retrieval from the Vector Store, and initiates the LLM generation cycle.

---

## ⬡ 4. MODULAR SKILLS (The Intel Layer)
EXODUS dynamically routes requests to specialized modules:

- **Financial Brain (`skills/finance.py`):** Analyzes investment opportunities and financial concepts.
- **Lifestyle Advisor (`skills/lifestyle.py`):** Provides health, energy, and habit suggestions.
- **Web Search (`skills/search.py`):** Fetches real-time internet data for current events.
- **Image Gen (`skills/image_gen.py`):** Direct integration with Pollinations.ai for AI-generated visuals.
- **Code Sandbox (`skills/sandbox.py`):** A restricted environment for running Python logic locally.
- **Daily Briefing (`skills/briefing.py`):** Summarizes news and personal reminders.

---

## ⬡ 5. USER COMMANDS & FEATURES

### 🤖 Intelligence Commands
| Command | Action |
|---|---|
| `/image [prompt]` | Generates an AI image (e.g., `/image a futuristic car`). |
| `/run [code]` | Executes Python code safely (e.g., `/run print(5+5)`). |
| `/briefing` | Generates a daily summary of news and personal context. |
| `Remember this: [fact]` | Commits a fact to long-term memory for future recall. |

### ⚡ Productivity Tools
- **PDF/TXT Ingestion:** Click the 📎 button to upload documents. EXODUS reads them into vector memory, allowing you to "chat with your files."
- **Voice Input:** Use the 🎤 button for live speech-to-text dictation.
- **Chat History:** The left sidebar stores all sessions. Start a **+ New Chat** or delete old ones easily.
- **PDF Export:** Use the **DOWNLOAD PDF** button in the HUD to export your current log as a `.txt` file.

---

## ⬡ 6. SETUP & RUNNING
To run EXODUS on your local machine:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API Key:**
   - Create a `.env` file with `GEMINI_API_KEY="your_key"`.
   - OR paste the key directly into the **API CONFIGURATION** section in the UI.
3. **Start Server:**
   ```bash
   uvicorn api.main:app --port 8000
   ```
4. **Access UI:**
   Navigate to `http://127.0.0.1:8000` in your browser.

---


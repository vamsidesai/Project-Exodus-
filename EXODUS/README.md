# PROJECT EXODUS

**Repository:** [https://github.com/vamsidesai/Project-Exodus-](https://github.com/vamsidesai/Project-Exodus-)
**Core Identity:** Public AI Companion / Comprehensive Life Advisor.

## Architecture
- **Backend:** Python (FastAPI Engine)
- **Model:** Google Gemini (via API)
- **Storage:** Vector Memory (ChromaDB)
- **Interface:** Deeply integrated Web UI (HTML/CSS/JS served directly from FastAPI)

## Setup & Running Locally

1. **Clone the repository and set up environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # On Windows
   # source venv/bin/activate # On Mac/Linux
   ```

2. **Install Libraries and Packages**
   Install all the required packages to run the application (like `fastapi`, `uvicorn`, `google-generativeai`, etc):
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key**
   Create a `.env` file in the root of the project and add your Gemini API Key like this:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
   *Alternatively, you can paste the key directly into the Web UI "API CONFIGURATION" panel when the app is running!*

4. **Start the EXODUS Server**
   Use `uvicorn` to spin up the local server, which will host both the backend logic and the Web UI.
   ```bash
   uvicorn api.main:app --port 8000
   ```

5. **Open the Application**
   Open your browser and navigate to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

Enjoy interacting with EXODUS!

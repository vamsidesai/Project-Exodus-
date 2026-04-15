from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict
import os
from dotenv import load_dotenv

# Load env variables (useful for picking up GEMINI_API_KEY from .env if present)
load_dotenv()

# Import EXODUS Core Singletons
from core.state import ModeState
from core.rules import RulesEngine, RuleViolation
from core.guardian import Guardian
from memory.vault import IdentityVault
from core.brain import Brain
import core.database as db

app = FastAPI(title="EXODUS API", version="1.0")

# Allow all CORS for local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances representing our system state
state = ModeState()
rules = RulesEngine()
guardian = Guardian()
vault = IdentityVault()
brain = Brain()

class ChatRequest(BaseModel):
    user_input: str
    api_key: Optional[str] = None
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/api/status")
def get_status():
    return state.to_dict()

@app.post("/api/chat", response_model=ChatResponse)
async def handle_chat(
    user_input: str = Form(...),
    api_key: Optional[str] = Form(None),
    session_id: Optional[str] = Form("default"),
    reply_to_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        # 1. Handle File first (if present)
        image_data = None
        image_mime = None
        
        if file:
            contents = await file.read()
            filename = file.filename.lower()
            
            if filename.endswith('.pdf'):
                # PDF: Extract and store in ChromaDB for immediate context
                brain.memory.ingest_pdf_bytes(contents, file.filename)
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Image: Keep for direct Vision analysis
                image_data = contents
                image_mime = file.content_type
            else:
                # Text/Other: Ingest as document
                text = contents.decode("utf-8", errors="ignore")
                brain.memory.ingest_document(text, file.filename)

        # 2. Safety & Rules
        rules.enforce(state, user_input)
        
        if session_id and session_id != "default":
            db.create_session(session_id, user_input[:20] + "...")
            # Save message and get its ID
            db.save_message(session_id, "user", user_input, reply_to_id)
            
        # 3. Process Turn via Brain (with optional image data)
        raw_response = brain.process_turn(user_input, state, api_key, image_data, image_mime)
        
        # 4. Post-check context
        safe_response = guardian.validate_output(state, raw_response)
        
        if session_id and session_id != "default":
            db.save_message(session_id, "assistant", safe_response)
            
        return ChatResponse(response=safe_response, status="success")
        
    except RuleViolation as e:
        return ChatResponse(response=f"⛔ RULE VIOLATION: {str(e)}", status="error")
    except Exception as e:
        return ChatResponse(response=f"ERROR: {str(e)}", status="error")

@app.get("/api/sessions")
def get_sessions():
    return {"sessions": db.get_sessions()}

@app.get("/api/sessions/{session_id}/messages")
def get_messages(session_id: str):
    return {"messages": db.get_messages(session_id)}

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    db.delete_session(session_id)
    return {"status": "success"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename
        
        if filename.lower().endswith('.pdf'):
            chunks = brain.memory.ingest_pdf_bytes(contents, filename)
        else:
            text = contents.decode("utf-8", errors="ignore")
            chunks = brain.memory.ingest_document(text, filename)
            
        return {"status": "success", "chunks": chunks, "filename": filename}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

app.mount("/", StaticFiles(directory="web", html=True), name="web")

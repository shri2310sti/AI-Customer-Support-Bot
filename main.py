from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

from database import get_db, create_tables, Session as DBSession, Message
from gemini_service import GeminiService

app = FastAPI(title="AI Customer Support Bot", version="1.0.0")
gemini_service = GeminiService()
create_tables()

# Pydantic models
class AskRequest(BaseModel):
    session_id: str
    query: str
    concise: bool = True  # Add concise mode

class AskResponse(BaseModel):
    response: str
    escalated: bool

class NewSessionResponse(BaseModel):
    session_id: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[MessageResponse]

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(Message).filter(Message.session_id == request.session_id).order_by(Message.timestamp).all()
    conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages]

    response_text, is_escalated = gemini_service.generate_response(
        request.query, conversation_history, concise=request.concise
    )

    db.add(Message(session_id=request.session_id, role="user", content=request.query))
    db.add(Message(session_id=request.session_id, role="bot", content=response_text))
    db.commit()

    return AskResponse(response=response_text, escalated=is_escalated)

@app.post("/new_session", response_model=NewSessionResponse)
async def create_new_session(db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    db.add(DBSession(id=session_id))
    db.commit()
    return NewSessionResponse(session_id=session_id)

@app.get("/get_history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    return HistoryResponse(
        session_id=session_id,
        messages=[MessageResponse(id=msg.id, role=msg.role, content=msg.content, timestamp=msg.timestamp) for msg in messages]
    )

@app.get("/faqs")
async def get_faqs():
    return gemini_service.get_faqs()

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("chat.html", {"request": request})

# routes/ai_assistant.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, crud
import google.generativeai as genai
from dotenv import load_dotenv
import os

router = APIRouter(prefix="/ai", tags=["AI"])

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/advice/{task_id}")
def get_task_advice(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    prompt = f"""Tenho a seguinte tarefa para fazer:
Título: {task.title}
Descrição: {task.description}

Como você aconselharia realizar essa tarefa da melhor forma possível?
Seja breve com tópicos
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-002")

    response = model.generate_content(prompt)

    return {"advice": response.text}

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from .. import database, crud, schemas
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import json
import re

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


class TextInput(BaseModel):
    text: str

@router.post("/process-text", response_model=list[schemas.TaskOut])
def process_text(input: TextInput, db: Session = Depends(get_db)):
    prompt = f"""
Você é um assistente para extração de tarefas.

Dado o texto abaixo, devolva **somente** uma lista JSON com as tarefas identificadas. Para cada tarefa, inclua:
- "title": título da tarefa
- "description": breve explicação da tarefa

⚠️ NÃO EXPLIQUE. Apenas devolva a lista JSON.

Exemplo:
[
  {{
    "title": "fazer almoço",
    "description": "vou fazer arroz com carne e batata"
  }}
]

Texto: {input.text}
"""


    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-002")

    try:
        response = model.generate_content(prompt)
        print("RAW IA:", response.text)

        json_match = re.search(r"\[\s*{.*?}\s*\]", response.text, re.DOTALL)

        if not json_match:
            raise HTTPException(status_code=500, detail="IA não retornou uma lista JSON válida.")

        json_text = json_match.group(0)
        tasks_data = json.loads(json_text)

        created_tasks = []
        for task in tasks_data:
            task_schema = schemas.TaskCreate(**task)
            created = crud.create_task(db, task_schema)
            created_tasks.append(created)

        return created_tasks

    except Exception as e:
        print("ERRO AO PROCESSAR IA:", e)
        print("RESPOSTA DA IA:", response.text)
        raise HTTPException(status_code=500, detail=f"Erro ao processar com IA: {str(e)}")
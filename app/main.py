import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .database import Base, engine
from .routes import tasks, ai_assistant
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo API",
    description="API de gerenciamento de tarefas com FastAPI",
    version="1.0.0"
)

app.include_router(tasks.router)
app.include_router(ai_assistant.router)
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL:", DATABASE_URL)

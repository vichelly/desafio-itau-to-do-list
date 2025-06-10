# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .database import Base, engine
from .routes import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo API",
    description="API de gerenciamento de tarefas com FastAPI",
    version="1.0.0"
)

app.include_router(tasks.router)
load_dotenv()  # carrega variáveis do arquivo .env para o ambiente

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL:", DATABASE_URL)

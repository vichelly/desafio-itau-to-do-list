from fastapi import FastAPI
from .database import Base, engine
from .routes import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo API",
    description="API de gerenciamento de tarefas com FastAPI",
    version="1.0.0"
)

app.include_router(tasks.routes)
print("DATABASE_URL:", DATABASE_URL)

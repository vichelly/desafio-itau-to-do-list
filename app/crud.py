from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    # Verifica se já existe uma task com mesmo título e descrição
    existing = db.query(models.Task).filter_by(
        title=task.title,
        description=task.description
    ).first()

    if existing:
        return existing  # ou raise HTTPException(status_code=400, detail="Tarefa duplicada")

    db_task = models.Task(**task.model_dump())  # para Pydantic v2
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).order_by(models.Task.id).offset(skip).limit(limit).all()
    
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def update_task_status(db: Session, task_id: int, status: str):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.status = status
        db.commit()
        db.refresh(db_task)
    return db_task

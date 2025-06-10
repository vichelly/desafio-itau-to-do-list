from pydantic import BaseModel, ConfigDict
from typing import Literal


class TaskBase(BaseModel):
    title: str
    description: str = ""
    status: Literal["pendente", "concluido"] = "pendente"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["pendente", "concluido"] | None = None

class TaskUpdateStatus(BaseModel):
    status: Literal["pendente", "concluido"]

class TaskOut(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)




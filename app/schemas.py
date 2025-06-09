from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = ""
    status: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True

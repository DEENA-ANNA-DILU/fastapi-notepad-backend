from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Task(TaskCreate):
    id: int
    owner: str
    status: str  # "pending" or "done"



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None



from datetime import date

class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: date   # YYYY-MM-DD format

class CalendarEvent(CalendarEventCreate):
    id: int
    owner: str



class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None

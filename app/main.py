from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas
from app.auth import get_current_user
from app import auth
from datetime import timedelta, date
from typing import Optional
from app.database import Base, engine, get_db
from app import models
from sqlalchemy.orm import Session
from app.llm import summarize_text
from fastapi import Body
from fastapi.responses import HTMLResponse
from fastapi import Form
from app.schemas import UserCreate, TaskCreate
from app.models import Task, User
from app.llm import summarize_text



app = FastAPI()


# Create tables
Base.metadata.create_all(bind=engine)



@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth.hash_password(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered successfully"}


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }







@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user": current_user
    }




@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        status="pending",
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task





@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(status: Optional[str] = None,
              current_user: str = Depends(auth.get_current_user),
              db: Session = Depends(get_db)):
    query = db.query(models.Task).filter(models.Task.owner == current_user)
    if status:
        if status not in ["pending", "done"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(models.Task.status == status)
    return db.query(Task).filter(Task.user_id == current_user.id).all()



@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate,
                current_user: str = Depends(auth.get_current_user),
                db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description

    db.commit()
    db.refresh(task)
    return task




@app.put("/tasks/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, status: str,
                       current_user: str = Depends(auth.get_current_user),
                       db: Session = Depends(get_db)):
    if status not in ["pending", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")

    task.status = status
    db.commit()
    db.refresh(task)
    return task








@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,
                current_user: str = Depends(auth.get_current_user),
                db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}




@app.post("/calendar", response_model=schemas.CalendarEvent)
def create_event(event: schemas.CalendarEventCreate,
                 current_user: str = Depends(auth.get_current_user),
                 db: Session = Depends(get_db)):
    new_event = models.CalendarEvent(
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        owner=current_user
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event





@app.get("/calendar", response_model=list[schemas.CalendarEvent])
def get_events(current_user: str = Depends(auth.get_current_user),
               db: Session = Depends(get_db)):
    events = db.query(models.CalendarEvent).filter(models.CalendarEvent.owner == current_user).all()
    return events





@app.put("/calendar/{event_id}", response_model=schemas.CalendarEvent)
def update_event(event_id: int, event_update: schemas.CalendarEventUpdate,
                 current_user: str = Depends(auth.get_current_user),
                 db: Session = Depends(get_db)):
    event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")

    if event_update.title is not None:
        event.title = event_update.title
    if event_update.description is not None:
        event.description = event_update.description
    if event_update.event_date is not None:
        event.event_date = event_update.event_date

    db.commit()
    db.refresh(event)
    return event




@app.delete("/calendar/{event_id}")
def delete_event(event_id: int,
                 current_user: str = Depends(auth.get_current_user),
                 db: Session = Depends(get_db)):
    event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}





"""@app.post("/ai/summarize")
def summarize_note(
    text: str = Body(..., embed=True)
):
    summary = summarize_text(text)
    return {
        "original": text,
        "summary": summary
    }"""





@app.get("/", response_class=HTMLResponse)
def home():
    with open("app/templates/index.html") as f:
        return f.read()

"""@app.post("/ui/summarize")
def ui_summarize(text: str = Form(...)):
    return {"summary": text[:100]}"""




@app.post("/llm/summarize")
def summarize_note(
    text: str,
    current_user: User = Depends(get_current_user)
):
    return {"summary": summarize_text(text)}
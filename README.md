# FastAPI Notepad Backend

A backend application built using **FastAPI** that provides authentication, task management, calendar features, database persistence, and designed integration support for open-source LLMs from Hugging Face.

---

## Features

- JWT-based Authentication (Register & Login)
- Task Management (CRUD operations)
- Task History (Pending / Completed)
- Calendar Event Management
- SQLite Database Integration using SQLAlchemy
- Open-source LLM Integration Design (Hugging Face)
- Minimal UI for backend and AI feature demonstration
- Interactive API testing using Swagger UI

---

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication
- Hugging Face (FLAN-T5 – integration design)
- HTML (Minimal UI)

---

## Project Structure

app/
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── llm.py
templates/
├── index.html
notepad.db



## 4. Setup Instructions
1. Clone repository
2. Create and activate virtual environment
3. Install dependencies (`pip install -r requirements.txt`)
4. Run FastAPI app with `uvicorn app.main:app --reload`

## 5. API Endpoints
| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| /register | POST | Register a new user | username, password | JWT token |
| /login | POST | User login | username, password | JWT token |
| /tasks | GET/POST/PUT/DELETE | Task CRUD | JSON | Task info |
| /calendar | GET/POST/PUT/DELETE | Calendar CRUD | JSON | Event info |
| /ai/summarize | POST | AI text processing (integration) | text | summarized text |

## 6. Features Implemented
- JWT Authentication
- Tasks CRUD + History
- Calendar Events CRUD
- Database Integration
- LLM Integration design
- Minimal HTML UI
- Swagger UI interactive testing

## 7. LLM Integration
- Researched open-source Hugging Face models: FLAN-T5
- Designed backend integration endpoint `/ai/summarize`
- Local execution deferred due to PyTorch DLL issues on Windows
- Modular backend function ready for future inference

## 8. Pending Work / Future Enhancements
- Complete verification and testing of all features  
- Enhance UI for better usability  
- Enable full LLM inference execution




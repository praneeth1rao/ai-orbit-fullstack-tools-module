# Backend — Tools API

Python + FastAPI + SQLAlchemy + SQLite.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

The app will create/use a local SQLite database on startup.

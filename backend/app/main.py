import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend root is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import ensure_db_initialized, SessionLocal
from app.routers import tools, categories, tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure database tables and demo seed exist on startup."""
    ensure_db_initialized()
    yield


app = FastAPI(
    title="AI Orbit Tools API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(tags.router, prefix="/api", tags=["tags"])
app.include_router(tools.router, prefix="/api", tags=["tools"])


@app.get("/")
def root():
    return {"message": "AI Orbit Tools API is online", "status": "ok"}


@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "ok"}


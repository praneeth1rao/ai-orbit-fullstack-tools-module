from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.models import Category, Tag, Tool, ToolTag
from app.routers import tools, categories, tags

app = FastAPI(title="AI Orbit Tools API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(tags.router, prefix="/api", tags=["tags"])
app.include_router(tools.router, prefix="/api", tags=["tools"])


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    create_tables()

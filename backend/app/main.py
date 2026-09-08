import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables, SessionLocal
from app.models import Category, Tag, Tool, ToolTag
from app.routers import tools, categories, tags

app = FastAPI(title="AI Orbit Tools API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://*.vercel.app"],
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    _seed_if_needed()
    yield


def _seed_if_needed() -> None:
    """Seed demo data on startup if the database is empty.

    This ensures the demo tools are available on Vercel deployment
    where the SQLite database is ephemeral.
    """
    if os.environ.get("VERCEL_ENV"):
        db = SessionLocal()
        try:
            from sqlalchemy import select as sa_select
            count = db.execute(sa_select(Tool)).scalars().all()
            if len(count) == 0:
                from seed import seed
                seed()
        finally:
            db.close()

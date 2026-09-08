from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tag
from app.schemas.tools import TagOut

router = APIRouter()


@router.get("/tags", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    rows = db.execute(select(Tag).order_by(Tag.name)).scalars().all()
    return [TagOut.model_validate(row) for row in rows]

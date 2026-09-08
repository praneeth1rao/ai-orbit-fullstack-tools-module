from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Category, Tag, Tool, ToolTag
from app.schemas.tools import ToolCreate, ToolOut, ToolUpdate, ToolsResponse
from app.services.helpers import list_to_platforms, paginate, to_slug

router = APIRouter()

PLATFORM_LIKE_PATTERNS = {
    "web": "%web%",
    "windows": "%windows%",
    "macos": "%macos%",
    "mac": "%macos%",
    "desktop": "%desktop%",
    "ios": "%ios%",
    "android": "%android%",
    "api": "%api%",
}

VALID_PRICING = {"free", "freemium", "paid"}
VALID_STATUS = {"draft", "published", "archived"}
VALID_SORT = {"newest", "oldest", "name_asc", "name_desc"}


def _normalize_platform_token(token: str) -> str:
    token = token.strip().lower()
    if token in PLATFORM_LIKE_PATTERNS:
        return token
    if token == "mac":
        return "macos"
    return token


def _platform_filter_clauses(wanted: list[str]):
    clauses = []
    seen = set()
    for token in wanted:
        key = _normalize_platform_token(token)
        if not key:
            continue
        normalized = key if key != "mac" else "macos"
        if key == "mac":
            key = "macos"
        if key in seen:
            continue
        seen.add(key)
        pattern = "%" + key + "%"
        clauses.append(func.lower(Tool.platforms).like(func.lower(pattern)))
    return clauses


def _platform_filter_for_request(platform: str | None):
    if not platform:
        return None
    tokens = [t.strip() for t in platform.split(",") if t.strip()]
    if not tokens:
        return None
    return _platform_filter_clauses(tokens)


@router.get("/tools", response_model=ToolsResponse)
def list_tools(
    q: Annotated[str | None, Query(max_length=500)] = None,
    category: Annotated[str | None, Query(max_length=255)] = None,
    pricing: Annotated[str | None, Query(max_length=64)] = None,
    platform: Annotated[str | None, Query(max_length=500)] = None,
    sort: Annotated[str | None, Query(max_length=64)] = "newest",
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Session = Depends(get_db),
):
    if sort not in VALID_SORT:
        sort = "newest"

    if pricing is not None:
        pricing_norm = pricing.strip().lower()
        if pricing_norm not in VALID_PRICING:
            return ToolsResponse(tools=[], pagination=paginate(0, page, limit))

    category_id = None
    if category:
        cat = db.execute(
            select(Category).where(Category.slug == category.strip())
        ).scalar_one_or_none()
        if cat is None:
            return ToolsResponse(tools=[], pagination=paginate(0, page, limit))
        category_id = cat.id

    base = select(Tool).options(selectinload(Tool.tags))

    count = select(func.count()).select_from(Tool)

    if category_id is not None:
        base = base.where(Tool.category_id == category_id)
        count = count.where(Tool.category_id == category_id)

    if pricing is not None:
        base = base.where(Tool.pricing == pricing.strip().lower())
        count = count.where(Tool.pricing == pricing.strip().lower())

    platform_clauses = _platform_filter_for_request(platform)
    if platform_clauses:
        base = base.where(or_(*platform_clauses))
        count = count.where(or_(*platform_clauses))

    if q:
        q_norm = f"%{q.strip()}%"
        base = base.where(
            or_(
                func.lower(Tool.title).like(func.lower(q_norm)),
                func.lower(Tool.description).like(func.lower(q_norm)),
            )
        )
        count = count.where(
            or_(
                func.lower(Tool.title).like(func.lower(q_norm)),
                func.lower(Tool.description).like(func.lower(q_norm)),
            )
        )

    if sort == "newest":
        base = base.order_by(Tool.created_at.desc())
    elif sort == "oldest":
        base = base.order_by(Tool.created_at.asc())
    elif sort == "name_asc":
        base = base.order_by(Tool.title.asc())
    elif sort == "name_desc":
        base = base.order_by(Tool.title.desc())

    total = db.execute(count).scalar() or 0
    pagination = paginate(total, page, limit)
    offset = (pagination["page"] - 1) * pagination["limit"]
    rows = db.execute(base.offset(offset).limit(pagination["limit"])).scalars().unique().all()
    tools = [ToolOut.model_validate(row) for row in rows]
    return ToolsResponse(tools=tools, pagination=pagination)


@router.get("/tools/{tool_id}", response_model=ToolOut)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    stmt = select(Tool).options(selectinload(Tool.tags)).where(Tool.id == tool_id)
    tool = db.execute(stmt).scalars().unique().one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    return ToolOut.model_validate(tool)


def _resolve_category_id(db: Session, category_slug: str | None):
    if not category_slug:
        return None
    cat = db.execute(
        select(Category).where(Category.slug == category_slug.strip())
    ).scalar_one_or_none()
    if cat is None:
        raise HTTPException(status_code=400, detail="category not found")
    return cat.id


def _prepare_platforms(value) -> str:
    if value is None:
        return "web"
    return list_to_platforms(value)


@router.post("/tools", response_model=ToolOut, status_code=201)
def create_tool(payload: ToolCreate, db: Session = Depends(get_db)):
    category_id = _resolve_category_id(db, payload.category_slug)

    slug = to_slug(payload.title)
    base_slug = slug
    counter = 1
    while db.execute(select(Tool).where(Tool.slug == slug)).scalar_one_or_none() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1

    tool = Tool(
        title=payload.title.strip(),
        slug=slug,
        description=payload.description.strip(),
        long_description=payload.long_description.strip() if payload.long_description else None,
        category_id=category_id,
        pricing=payload.pricing,
        website_url=payload.website_url,
        logo_url=payload.logo_url,
        platforms=_prepare_platforms(payload.platforms),
        status=payload.status,
    )
    db.add(tool)
    db.flush()

    tag_names = payload.tags or []
    for tag_name in tag_names:
        if not tag_name.strip():
            continue
        tag_slug = to_slug(tag_name)
        tag = db.execute(select(Tag).where(Tag.slug == tag_slug)).scalar_one_or_none()
        if tag is None:
            tag = Tag(name=tag_name.strip(), slug=tag_slug)
            db.add(tag)
            db.flush()
        exists = db.execute(
            select(ToolTag).where(ToolTag.tool_id == tool.id, ToolTag.tag_id == tag.id)
        ).scalar_one_or_none()
        if exists is None:
            db.add(ToolTag(tool_id=tool.id, tag_id=tag.id))

    tool = db.execute(
        select(Tool).options(selectinload(Tool.tags)).where(Tool.id == tool.id)
    ).scalars().unique().one()
    return ToolOut.model_validate(tool)


@router.put("/tools/{tool_id}", response_model=ToolOut)
def update_tool(tool_id: int, payload: ToolUpdate, db: Session = Depends(get_db)):
    tool = db.execute(select(Tool).where(Tool.id == tool_id)).scalars().one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")

    if payload.title is not None:
        tool.title = payload.title.strip()
    if payload.description is not None:
        tool.description = payload.description.strip()
    if payload.long_description is not None:
        tool.long_description = (
            payload.long_description.strip() if payload.long_description else None
        )
    if payload.category_slug is not None:
        tool.category_id = _resolve_category_id(db, payload.category_slug)
    if payload.pricing is not None:
        tool.pricing = payload.pricing
    if payload.website_url is not None:
        tool.website_url = payload.website_url
    if payload.logo_url is not None:
        tool.logo_url = payload.logo_url
    if payload.platforms is not None:
        tool.platforms = _prepare_platforms(payload.platforms)
    if payload.status is not None:
        tool.status = payload.status

    conflicting = db.execute(
        select(Tool).where(Tool.slug == tool.slug, Tool.id != tool.id)
    ).scalar_one_or_none()
    if conflicting is not None:
        raise HTTPException(status_code=400, detail="slug already in use")

    db.add(tool)
    db.flush()

    tag_names = payload.tags
    if tag_names is not None:
        db.execute(ToolTag.__table__.delete().where(ToolTag.tool_id == tool.id))
        for tag_name in tag_names:
            if not tag_name.strip():
                continue
            tag_slug = to_slug(tag_name)
            tag = db.execute(select(Tag).where(Tag.slug == tag_slug)).scalar_one_or_none()
            if tag is None:
                tag = Tag(name=tag_name.strip(), slug=tag_slug)
                db.add(tag)
                db.flush()
            exists = db.execute(
                select(ToolTag).where(ToolTag.tool_id == tool.id, ToolTag.tag_id == tag.id)
            ).scalar_one_or_none()
            if exists is None:
                db.add(ToolTag(tool_id=tool.id, tag_id=tag.id))

    tool = db.execute(
        select(Tool).options(selectinload(Tool.tags)).where(Tool.id == tool.id)
    ).scalars().unique().one()
    return ToolOut.model_validate(tool)


@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.execute(select(Tool).where(Tool.id == tool_id)).scalars().one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    db.delete(tool)
    db.commit()
    return {"deleted": True, "id": tool_id}

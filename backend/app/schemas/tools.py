from datetime import datetime
from typing import Any

from pydantic import BaseModel, HttpUrl, field_validator


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TagOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class ToolBase(BaseModel):
    title: str
    description: str
    long_description: str | None = None
    category_slug: str | None = None
    pricing: str = "free"
    website_url: str | None = None
    logo_url: str | None = None
    platforms: list[str] | None = None
    status: str = "published"
    tags: list[str] | None = None


class ToolCreate(ToolBase):
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("title must not be empty")
        return value.strip()

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("description must not be empty")
        return value.strip()

    @field_validator("pricing")
    @classmethod
    def pricing_allowed(cls, value: str) -> str:
        allowed = {"free", "freemium", "paid"}
        if value.lower() not in allowed:
            raise ValueError(f"pricing must be one of: {', '.join(sorted(allowed))}")
        return value.lower()

    @field_validator("status")
    @classmethod
    def status_allowed(cls, value: str) -> str:
        allowed = {"draft", "published", "archived"}
        if value.lower() not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
        return value.lower()

    @field_validator("website_url")
    @classmethod
    def website_url_valid(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if value:
            HttpUrl(value)
        return value


class ToolUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    long_description: str | None = None
    category_slug: str | None = None
    pricing: str | None = None
    website_url: str | None = None
    logo_url: str | None = None
    platforms: list[str] | None = None
    status: str | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("title must not be empty")
        return value.strip()

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("description must not be empty")
        return value.strip()

    @field_validator("pricing")
    @classmethod
    def pricing_allowed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        allowed = {"free", "freemium", "paid"}
        if value.lower() not in allowed:
            raise ValueError(f"pricing must be one of: {', '.join(sorted(allowed))}")
        return value.lower()

    @field_validator("status")
    @classmethod
    def status_allowed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        allowed = {"draft", "published", "archived"}
        if value.lower() not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
        return value.lower()

    @field_validator("website_url")
    @classmethod
    def website_url_valid(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if value:
            HttpUrl(value)
        return value


class ToolOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    long_description: str | None
    category: CategoryOut | None
    pricing: str
    website_url: str | None
    logo_url: str | None
    platforms: list[str]
    status: str
    created_at: datetime
    updated_at: datetime
    tags: list[TagOut]

    @field_validator("platforms", mode="before")
    @classmethod
    def normalize_platforms(cls, value):
        if isinstance(value, list):
            return [str(p).strip() for p in value if str(p).strip()]
        if isinstance(value, str):
            return [p.strip() for p in value.split(",") if p.strip()]
        return []

    model_config = {"from_attributes": True}


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int


class ToolsResponse(BaseModel):
    tools: list[ToolOut]
    pagination: PaginationMeta

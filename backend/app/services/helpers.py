import re
from math import ceil
from typing import Any

from pydantic import HttpUrl


def to_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s\-_]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def platforms_to_list(value: str) -> list[str]:
    if not value:
        return ["web"]
    return [p.strip() for p in value.split(",") if p.strip()]


def list_to_platforms(value: list[str] | None) -> str:
    if not value:
        return "web"
    normalized: list[str] = []
    mapping = {
        "web": "web",
        "windows": "windows",
        "macos": "macos",
        "mac": "macos",
        "desktop": "desktop",
        "ios": "ios",
        "iphone": "ios",
        "android": "android",
        "api": "api",
    }
    for raw in value:
        key = raw.strip().lower()
        chosen = mapping.get(key, key)
        if chosen not in normalized:
            normalized.append(chosen)
    return ",".join(normalized) if normalized else "web"


def validate_url_string(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    HttpUrl(value)
    return value


def paginate(total: int, page: int, limit: int) -> dict[str, Any]:
    if limit < 1:
        limit = 20
    if page < 1:
        page = 1
    total_pages = max(1, ceil(total / limit))
    page = min(page, total_pages)
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }

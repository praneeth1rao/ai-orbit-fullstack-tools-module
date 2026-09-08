from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    tools: Mapped[list["Tool"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    tools: Mapped[list["Tool"]] = relationship(
        secondary="tool_tags",
        back_populates="tags",
        lazy="selectin",
    )


class ToolTag(Base):
    __tablename__ = "tool_tags"

    tool_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tools.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    long_description: Mapped[str] = mapped_column(Text, nullable=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    pricing: Mapped[str] = mapped_column(String(64), nullable=False, default="free")
    website_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(2048), nullable=True)
    platforms: Mapped[str] = mapped_column(Text, nullable=False, default="web")
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="published")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    category: Mapped["Category | None"] = relationship(back_populates="tools")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="tool_tags",
        back_populates="tools",
        lazy="selectin",
    )

    __table_args__ = (
        Index("ix_tools_slug", "slug"),
        Index("ix_tools_category_id", "category_id"),
        Index("ix_tools_pricing", "pricing"),
        Index("ix_tools_status", "status"),
        Index("ix_tools_title", "title"),
    )

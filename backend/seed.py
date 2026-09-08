"""
Seed script for the AI Orbit Tools demo module.

All seeded data is DUMMY/DEMO data intended for local development and
presentation only. It is not verified real-world information about real
products, companies, users, ratings, revenue, or rankings.
"""

from datetime import datetime, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Category, Tag, Tool, ToolTag


def _now() -> datetime:
    return datetime.now(timezone.utc)


DEMO_CATEGORIES = [
    {
        "name": "Writing & Content",
        "slug": "writing-content",
        "description": "Demo category for writing, editing, and content creation tools.",
    },
    {
        "name": "Code & Development",
        "slug": "code-development",
        "description": "Demo category for coding assistants, dev tools, and APIs.",
    },
    {
        "name": "Design & Creative",
        "slug": "design-creative",
        "description": "Demo category for design, image, video, and creative tools.",
    },
    {
        "name": "Research & Knowledge",
        "slug": "research-knowledge",
        "description": "Demo category for search, summarization, and knowledge tools.",
    },
    {
        "name": "Productivity & Automation",
        "slug": "productivity-automation",
        "description": "Demo category for workflow, automation, and productivity tools.",
    },
    {
        "name": "Audio & Voice",
        "slug": "audio-voice",
        "description": "Demo category for speech, audio, and voice tools.",
    },
    {
        "name": "Data & Analytics",
        "slug": "data-analytics",
        "description": "Demo category for datasets, analytics, and data tooling.",
    },
]


DEMO_TAGS = [
    "text generation",
    " summarization",
    " code assistant",
    " image generation",
    " video",
    " transcription",
    " translation",
    " search",
    " automation",
    " api",
    " desktop",
    " mobile",
    " free",
    " enterprise",
    " chatbot",
    " editing",
    " prototyping",
    " notes",
    " spreadsheets",
    " privacy",
]


DEMO_TOOLS = [
    {
        "title": "OmniWrite Demo",
        "slug": "omniwrite-demo",
        "description": "A demo writing assistant for drafting articles, emails, and short-form copy.",
        "long_description": (
            "OmniWrite Demo is a fictional writing assistant created for this demo "
            "directory. It illustrates how a modern writing tool listing might look in "
            "an AI Orbit-style interface. It includes a short description, longer "
            "description, category, tags, pricing, and platform details. All information "
            "here is demo data only and does not describe a real product."
        ),
        "category_slug": "writing-content",
        "pricing": "freemium",
        "website_url": "https://example.com/omniwrite-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=OW",
        "platforms": ["web"],
        "tags": ["text generation", "editing", "notes"],
        "status": "published",
    },
    {
        "title": "QuickDraft Studio",
        "slug": "quickdraft-studio",
        "description": "Demo tool for rapid drafting of blog posts and internal memos.",
        "long_description": (
            "QuickDraft Studio demonstrates a content drafting tool listing. It is a demo "
            "entry used to populate the directory with realistic-looking fields such as "
            "category, pricing, platforms, and tags. This is not a real product and should "
            "not be treated as verified information."
        ),
        "category_slug": "writing-content",
        "pricing": "free",
        "website_url": "https://example.com/quickdraft-studio",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=QD",
        "platforms": ["web"],
        "tags": ["text generation", "editing", "free"],
        "status": "published",
    },
    {
        "title": "EditFlow AI",
        "slug": "editflow-ai",
        "description": "Demo assistant for editing tone, grammar, and clarity.",
        "long_description": (
            "EditFlow AI is included as a demo editing tool. It shows how editing-focused "
            "tools can be presented with category metadata, tags, and platform support in a "
            "dark, minimal directory UI. All fields are demo data."
        ),
        "category_slug": "writing-content",
        "pricing": "freemium",
        "website_url": "https://example.com/editflow-ai",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=EF",
        "platforms": ["web", "desktop"],
        "tags": ["editing", "transcription", "privacy"],
        "status": "published",
    },
    {
        "title": "PromptForge",
        "slug": "promptforge",
        "description": "Demo prompt builder and manager for experimenting with prompts.",
        "long_description": (
            "PromptForge is a demo prompt-management tool created for this directory. It is "
            "useful for showing how category and tag filters behave when multiple tools share "
            "similar metadata. This is demo data only."
        ),
        "category_slug": "code-development",
        "pricing": "free",
        "website_url": "https://example.com/promptforge",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=PF",
        "platforms": ["web"],
        "tags": ["code assistant", "chatbot", "free", "automation"],
        "status": "published",
    },
    {
        "title": "SnippetLab Demo",
        "slug": "snippetlab-demo",
        "description": "Demo snippet manager for code samples and reusable patterns.",
        "long_description": (
            "SnippetLab Demo illustrates a developer-tool listing with code-focused tags and "
            "a free pricing tier. It is one of several demo entries designed to exercise "
            "filtering, pagination, and detail views in this module."
        ),
        "category_slug": "code-development",
        "pricing": "free",
        "website_url": "https://example.com/snippetlab-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=SL",
        "platforms": ["web", "desktop"],
        "tags": ["code assistant", "api", "desktop", "free"],
        "status": "published",
    },
    {
        "title": "RepoScanner Demo",
        "slug": "reposcanner-demo",
        "description": "Demo repository scanning tool for summarizing codebases.",
        "long_description": (
            "RepoScanner Demo is a fictional code-analysis tool included to demonstrate "
            "search and category filtering across developer tools. It is demo data and not "
            "a real offering."
        ),
        "category_slug": "code-development",
        "pricing": "freemium",
        "website_url": "https://example.com/reposcanner-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=RS",
        "platforms": ["web", "api"],
        "tags": ["code assistant", "search", "api", "enterprise"],
        "status": "published",
    },
    {
        "title": "BuildBench",
        "slug": "buildbench",
        "description": "Demo benchmarking helper for comparing build and deploy workflows.",
        "long_description": (
            "BuildBench is a demo developer-tool example focused on workflow comparison. It "
            "shows paid-tier presentation in the directory alongside free and freemium "
            "entries. All metadata is demo data."
        ),
        "category_slug": "code-development",
        "pricing": "paid",
        "website_url": "https://example.com/buildbench",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=BB",
        "platforms": ["web", "api", "desktop"],
        "tags": ["automation", "api", "enterprise", "privacy"],
        "status": "published",
    },
    {
        "title": "CanvasGen Demo",
        "slug": "canvasgen-demo",
        "description": "Demo image generation workspace for visual experiments.",
        "long_description": (
            "CanvasGen Demo is a fictional image-generation tool created to populate the "
            "Design & Creative category. It demonstrates how visual tools can be listed with "
            "platform and pricing metadata in a dark directory UI."
        ),
        "category_slug": "design-creative",
        "pricing": "freemium",
        "website_url": "https://example.com/canvasgen-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=CG",
        "platforms": ["web"],
        "tags": ["image generation", "prototyping", "free"],
        "status": "published",
    },
    {
        "title": "VectorIllustrator Demo",
        "slug": "vectorillustrator-demo",
        "description": "Demo vector illustration helper for icons and layouts.",
        "long_description": (
            "VectorIllustrator Demo shows how a design tool listing might present categories, "
            "tags, and platform support. This is demo data only and does not describe a real "
            "product."
        ),
        "category_slug": "design-creative",
        "pricing": "paid",
        "website_url": "https://example.com/vectorillustrator-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=VI",
        "platforms": ["web", "desktop"],
        "tags": ["image generation", "editing", "desktop", "enterprise"],
        "status": "published",
    },
    {
        "title": "MotionMockup Studio",
        "slug": "motionmockup-studio",
        "description": "Demo motion mockup tool for quick prototype animations.",
        "long_description": (
            "MotionMockup Studio is a demo creative tool for prototype animations. It helps "
            "demonstrate video and animation-adjacent tags in the directory. All information "
            "is demo data."
        ),
        "category_slug": "design-creative",
        "pricing": "free",
        "website_url": "https://example.com/motionmockup-studio",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=MM",
        "platforms": ["web", "desktop"],
        "tags": ["video", "prototyping", "free", "editing"],
        "status": "published",
    },
    {
        "title": "PaletteLab Demo",
        "slug": "palettelab-demo",
        "description": "Demo color and theme exploration tool for design projects.",
        "long_description": (
            "PaletteLab Demo is a fictional design-exploration tool included to round out the "
            "creative category. It is demo data intended for UI demonstration only."
        ),
        "category_slug": "design-creative",
        "pricing": "free",
        "website_url": "https://example.com/palettelab-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=PL",
        "platforms": ["web", "mobile"],
        "tags": ["image generation", "mobile", "free", "prototyping"],
        "status": "published",
    },
    {
        "title": "BriefMind",
        "slug": "briefmind",
        "description": "Demo research brief generator for project scoping.",
        "long_description": (
            "BriefMind is a demo research tool that illustrates how knowledge-oriented tools "
            "can be categorized and tagged. All descriptions and metadata are demo data."
        ),
        "category_slug": "research-knowledge",
        "pricing": "freemium",
        "website_url": "https://example.com/briefmind",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=BM",
        "platforms": ["web"],
        "tags": ["search", "summarization", "notes", "free"],
        "status": "published",
    },
    {
        "title": "SummaryLens Demo",
        "slug": "summarylens-demo",
        "description": "Demo document summarization tool for long reports.",
        "long_description": (
            "SummaryLens Demo shows a summarization-focused tool listing. It is one of several "
            "demo entries created to demonstrate category and tag filtering in the directory."
        ),
        "category_slug": "research-knowledge",
        "pricing": "free",
        "website_url": "https://example.com/summarylens-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=SL",
        "platforms": ["web"],
        "tags": ["summarization", "notes", "free", "privacy"],
        "status": "published",
    },
    {
        "title": "RecallBase Demo",
        "slug": "recallbase-demo",
        "description": "Demo knowledge base tool for notes and retrieval practice.",
        "long_description": (
            "RecallBase Demo is a fictional knowledge-management tool. It demonstrates how "
            "notes-oriented tools can appear alongside more obviously AI-centric entries."
        ),
        "category_slug": "research-knowledge",
        "pricing": "freemium",
        "website_url": "https://example.com/recallbase-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=RB",
        "platforms": ["web", "mobile", "desktop"],
        "tags": ["notes", "search", "mobile", "enterprise"],
        "status": "published",
    },
    {
        "title": "DeepDive Research",
        "slug": "deepdive-research",
        "description": "Demo research exploration tool for topic discovery.",
        "long_description": (
            "DeepDive Research is a demo exploration tool created to populate the research "
            "category. It is demo data and should not be interpreted as a real product or "
            "verified recommendation."
        ),
        "category_slug": "research-knowledge",
        "pricing": "paid",
        "website_url": "https://example.com/deepdive-research",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=DD",
        "platforms": ["web", "api"],
        "tags": ["search", "summarization", "api", "enterprise"],
        "status": "published",
    },
    {
        "title": "FlowAutomate Demo",
        "slug": "flowautomate-demo",
        "description": "Demo workflow automation builder for routine tasks.",
        "long_description": (
            "FlowAutomate Demo illustrates a productivity and automation tool listing. It is "
            "included to show how automation tools can be presented with multiple platform "
            "options and varied pricing."
        ),
        "category_slug": "productivity-automation",
        "pricing": "freemium",
        "website_url": "https://example.com/flowautomate-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=FA",
        "platforms": ["web", "api"],
        "tags": ["automation", "api", "chatbot", "free"],
        "status": "published",
    },
    {
        "title": "TaskTriage",
        "slug": "tasktriage",
        "description": "Demo task prioritization tool for planning sessions.",
        "long_description": (
            "TaskTriage is a demo productivity tool that helps show how filtering by pricing "
            "and platform can work across a directory. All data here is demo data only."
        ),
        "category_slug": "productivity-automation",
        "pricing": "free",
        "website_url": "https://example.com/tasktriage",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=TT",
        "platforms": ["web", "mobile"],
        "tags": ["automation", "notes", "mobile", "free"],
        "status": "published",
    },
    {
        "title": "SheetMind Demo",
        "slug": "sheetmind-demo",
        "description": "Demo spreadsheet helper for formulas, cleanup, and summaries.",
        "long_description": (
            "SheetMind Demo is a fictional spreadsheet assistant created to demonstrate tools "
            "that blend productivity with analytics-style metadata. It is demo data only."
        ),
        "category_slug": "productivity-automation",
        "pricing": "freemium",
        "website_url": "https://example.com/sheetmind-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=SM",
        "platforms": ["web"],
        "tags": ["spreadsheets", "automation", "free", "privacy"],
        "status": "published",
    },
    {
        "title": "MeetingMosaic Demo",
        "slug": "meetingmosaic-demo",
        "description": "Demo meeting note organizer for action items and summaries.",
        "long_description": (
            "MeetingMosaic Demo shows how a meeting-focused productivity tool can be listed "
            "with category, tags, and platform metadata. All information is demo data."
        ),
        "category_slug": "productivity-automation",
        "pricing": "paid",
        "website_url": "https://example.com/meetingmosaic-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=MM",
        "platforms": ["web", "desktop", "mobile"],
        "tags": ["notes", "summarization", "mobile", "enterprise"],
        "status": "published",
    },
    {
        "title": "VoiceDraft Studio",
        "slug": "voicedraft-studio",
        "description": "Demo voice drafting tool for spoken notes and dictation.",
        "long_description": (
            "VoiceDraft Studio is a demo audio-oriented tool included to populate the Audio & "
            "Voice category. It is demo data intended for UI demonstration."
        ),
        "category_slug": "audio-voice",
        "pricing": "free",
        "website_url": "https://example.com/voicedraft-studio",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=VD",
        "platforms": ["web", "mobile", "desktop"],
        "tags": ["transcription", "mobile", "desktop", "free"],
        "status": "published",
    },
    {
        "title": "ClearSpeak Demo",
        "slug": "clearspeak-demo",
        "description": "Demo voice cleanup and emphasis tool for narration.",
        "long_description": (
            "ClearSpeak Demo illustrates a voice-enhancement tool listing. It is included to "
            "show variety across audio tools in the directory. All fields are demo data."
        ),
        "category_slug": "audio-voice",
        "pricing": "freemium",
        "website_url": "https://example.com/clearspeak-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=CS",
        "platforms": ["web", "desktop"],
        "tags": ["transcription", "editing", "desktop", "privacy"],
        "status": "published",
    },
    {
        "title": "TalkBridge Demo",
        "slug": "talkbridge-demo",
        "description": "Demo translation and conversation helper for multilingual calls.",
        "long_description": (
            "TalkBridge Demo is a fictional voice/translation tool created to demonstrate how "
            "audio and language-oriented tools can appear in the directory. Demo data only."
        ),
        "category_slug": "audio-voice",
        "pricing": "freemium",
        "website_url": "https://example.com/talkbridge-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=TB",
        "platforms": ["web", "mobile"],
        "tags": ["translation", "chatbot", "mobile", "free"],
        "status": "published",
    },
    {
        "title": "MetricMiner Demo",
        "slug": "metricminer-demo",
        "description": "Demo dataset exploration tool for quick metric checks.",
        "long_description": (
            "MetricMiner Demo is a demo analytics tool designed to populate the Data & "
            "Analytics category. It highlights spreadsheets, search, and automation tags."
        ),
        "category_slug": "data-analytics",
        "pricing": "freemium",
        "website_url": "https://example.com/metricminer-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=MM",
        "platforms": ["web", "api"],
        "tags": ["spreadsheets", "search", "api", "free"],
        "status": "published",
    },
    {
        "title": "ChartCraft Demo",
        "slug": "chartcraft-demo",
        "description": "Demo charting helper for quick visual summaries.",
        "long_description": (
            "ChartCraft Demo is a fictional charting tool included to show analytics-adjacent "
            "tools in the directory. All metadata is demo data and not verified."
        ),
        "category_slug": "data-analytics",
        "pricing": "free",
        "website_url": "https://example.com/chartcraft-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=CC",
        "platforms": ["web"],
        "tags": ["spreadsheets", "image generation", "prototyping", "free"],
        "status": "published",
    },
    {
        "title": "DatasetLens",
        "slug": "datasetlens",
        "description": "Demo dataset viewer for sampling and quick profiling.",
        "long_description": (
            "DatasetLens is a demo data tooling entry that demonstrates how data tools can be "
            "listed with API and platform metadata. It is demo data only."
        ),
        "category_slug": "data-analytics",
        "pricing": "paid",
        "website_url": "https://example.com/datasetlens",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=DL",
        "platforms": ["web", "api", "desktop"],
        "tags": ["api", "search", "enterprise", "privacy"],
        "status": "published",
    },
    {
        "title": "SemantiSearch Demo",
        "slug": "semantisearch-demo",
        "description": "Demo semantic search helper for finding related concepts.",
        "long_description": (
            "SemantiSearch Demo is a fictional search tool created to demonstrate how a "
            "research/knowledge tool can be presented alongside productivity and creativity "
            "tools. It is demo data only."
        ),
        "category_slug": "research-knowledge",
        "pricing": "freemium",
        "website_url": "https://example.com/semantisearch-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=SS",
        "platforms": ["web", "api"],
        "tags": ["search", "summarization", "api", "enterprise"],
        "status": "published",
    },
    {
        "title": "NoteNest",
        "slug": "notenest",
        "description": "Demo note-taking tool with tagging and quick capture.",
        "long_description": (
            "NoteNest is a demo notes tool used to populate the directory with a simple, "
            "mobile-friendly productivity entry. All data is demo data only."
        ),
        "category_slug": "productivity-automation",
        "pricing": "free",
        "website_url": "https://example.com/notenest",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=NN",
        "platforms": ["web", "mobile"],
        "tags": ["notes", "mobile", "free", "privacy"],
        "status": "published",
    },
    {
        "title": "DraftCompass",
        "slug": "draftcompass",
        "description": "Demo planning aid for outlining articles and reports.",
        "long_description": (
            "DraftCompass is a demo writing-planning tool included to show how outline-focused "
            "tools can appear in the directory. This is demo data only."
        ),
        "category_slug": "writing-content",
        "pricing": "free",
        "website_url": "https://example.com/draftcompass",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=DC",
        "platforms": ["web"],
        "tags": ["text generation", "notes", "free"],
        "status": "published",
    },
    {
        "title": "CodeGenie Demo",
        "slug": "codegenie-demo",
        "description": "Demo code explanation helper for learning unfamiliar code.",
        "long_description": (
            "CodeGenie Demo is a fictional code-explanation tool created for this directory. "
            "It is intended to demonstrate developer-tool variety within a single category."
        ),
        "category_slug": "code-development",
        "pricing": "freemium",
        "website_url": "https://example.com/codegenie-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=CG",
        "platforms": ["web"],
        "tags": ["code assistant", "chatbot", "free", "privacy"],
        "status": "published",
    },
    {
        "title": "TestForge Demo",
        "slug": "testforge-demo",
        "description": "Demo test-generation helper for sample cases and checks.",
        "long_description": (
            "TestForge Demo illustrates an authoring tool for test cases. It is demo data "
            "and not a real product recommendation or verified tool."
        ),
        "category_slug": "code-development",
        "pricing": "free",
        "website_url": "https://example.com/testforge-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=TF",
        "platforms": ["web", "api"],
        "tags": ["code assistant", " api", "automation", "free"],
        "status": "published",
    },
    {
        "title": "LayoutLab Demo",
        "slug": "layoutlab-demo",
        "description": "Demo UI layout sketching tool for rapid wireframing.",
        "long_description": (
            "LayoutLab Demo is a fictional wireframing tool included to populate the Design & "
            "Creative category. All metadata is demo data only."
        ),
        "category_slug": "design-creative",
        "pricing": "freemium",
        "website_url": "https://example.com/layoutlab-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=LL",
        "platforms": ["web", "desktop"],
        "tags": ["prototyping", "image generation", "desktop", "free"],
        "status": "published",
    },
    {
        "title": "ClipWhisper Demo",
        "slug": "clipwhisper-demo",
        "description": "Demo short-clip transcription helper for spoken snippets.",
        "long_description": (
            "ClipWhisper Demo is a fictional transcription tool used to show audio-related "
            "entries in the directory. It is demo data only."
        ),
        "category_slug": "audio-voice",
        "pricing": "free",
        "website_url": "https://example.com/clipwhisper-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=CW",
        "platforms": ["web", "mobile"],
        "tags": ["transcription", "mobile", "free"],
        "status": "published",
    },
    {
        "title": "InsightTable Demo",
        "slug": "insighttable-demo",
        "description": "Demo tabular insight tool for spotting trends.",
        "long_description": (
            "InsightTable Demo is a demo analytics helper for tables and trends. It is "
            "included to show how spreadsheet and analytics tags can coexist. Demo data only."
        ),
        "category_slug": "data-analytics",
        "pricing": "freemium",
        "website_url": "https://example.com/insighttable-demo",
        "logo_url": "https://placehold.co/120x120/121216/ffffff?text=IT",
        "platforms": ["web"],
        "tags": ["spreadsheets", "search", "free", "privacy"],
        "status": "published",
    },
]


def _slug(text: str) -> str:
    base = text.strip().lower()
    out: list[str] = []
    for ch in base:
        if ch.isalnum() or ch == "-":
            out.append(ch)
        elif ch in {" ", "_", ".", "/"}:
            out.append("-")
        else:
            continue
    return "-".join("".join(out).split("-")).strip("-")


def _normalize_platforms(platforms) -> str:
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
    seen: list[str] = []
    for raw in platforms:
        key = raw.strip().lower()
        chosen = mapping.get(key, key)
        if chosen not in seen:
            seen.append(chosen)
    return ",".join(seen)


def _ensure_category(session, slug: str, payload: dict) -> Category:
    category = session.execute(
        select(Category).where(Category.slug == slug)
    ).scalar_one_or_none()
    if category is None:
        category = Category(
            name=payload["name"],
            slug=slug,
            description=payload.get("description"),
            created_at=_now(),
        )
        session.add(category)
        session.flush()
    return category


def _ensure_tag(session, name: str) -> Tag:
    slug = _slug(name)
    tag = session.execute(select(Tag).where(Tag.slug == slug)).scalar_one_or_none()
    if tag is None:
        tag = Tag(name=name.strip(), slug=slug)
        session.add(tag)
    return tag


def _ensure_tool(session, tool_payload: dict) -> Tool:
    tool = session.execute(
        select(Tool).where(Tool.slug == tool_payload["slug"])
    ).scalar_one_or_none()
    if tool is not None:
        return tool

    category_slug = tool_payload.get("category_slug")
    category = None
    if category_slug:
        category = _ensure_category(session, category_slug, {
            "name": "",
            "description": "",
        })

    tool = Tool(
        title=tool_payload["title"],
        slug=tool_payload["slug"],
        description=tool_payload["description"],
        long_description=tool_payload.get("long_description"),
        category_id=category.id if category else None,
        pricing=tool_payload.get("pricing", "free"),
        website_url=tool_payload.get("website_url"),
        logo_url=tool_payload.get("logo_url"),
        platforms=_normalize_platforms(tool_payload.get("platforms", ["web"])),
        status=tool_payload.get("status", "published"),
        created_at=_now(),
        updated_at=_now(),
    )
    session.add(tool)
    return tool


def seed() -> None:
    from app.database import create_tables

    create_tables()

    session = SessionLocal()
    try:
        for category_payload in DEMO_CATEGORIES:
            _ensure_category(session, category_payload["slug"], category_payload)

        for tag_name in DEMO_TAGS:
            _ensure_tag(session, tag_name)

        for tool_payload in DEMO_TOOLS:
            tool = _ensure_tool(session, tool_payload)
            if tool.id is None:
                session.flush()

            tag_names = tool_payload.get("tags", [])
            for tag_name in tag_names:
                tag = _ensure_tag(session, tag_name)
                exists = session.execute(
                    select(ToolTag).where(
                        ToolTag.tool_id == tool.id,
                        ToolTag.tag_id == tag.id,
                    )
                ).scalar_one_or_none()
                if exists is None:
                    session.add(ToolTag(tool_id=tool.id, tag_id=tag.id))

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
    print("Seed complete.")

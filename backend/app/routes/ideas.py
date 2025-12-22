"""Bulk idea generation API routes."""
from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel

from ..services.nlp.idea_generator import IdeaGenerator

router = APIRouter()
idea_generator = IdeaGenerator()


class IdeaItem(BaseModel):
    phrase: str
    category: str
    niche: str
    score: int
    word_count: int
    char_count: int
    source: Optional[str] = None


class GenerateIdeasResponse(BaseModel):
    total: int
    generated_at: str
    ideas: List[IdeaItem]
    by_category: dict
    by_niche: dict
    stats: dict


class QuickGenerateRequest(BaseModel):
    topic: str
    count: int = 50


@router.post("/generate", response_model=GenerateIdeasResponse)
async def generate_ideas(
    count: int = Query(200, ge=10, le=500),
    niches: Optional[str] = Query(None, description="Comma-separated niches"),
    include_classics: bool = Query(True),
    include_generated: bool = Query(True),
    include_variations: bool = Query(True),
    creativity: str = Query("medium", regex="^(low|medium|high)$"),
):
    """
    Generate hundreds of merch phrase ideas.

    This is the main endpoint for bulk idea generation. It combines:
    - Classic bestseller phrases (proven winners)
    - Template-generated phrases (patterns + topics)
    - Variations of top phrases
    - Trending combinations

    Parameters:
    - count: Number of ideas to generate (10-500)
    - niches: Comma-separated list of niches to focus on
    - include_classics: Include proven bestseller phrases
    - include_generated: Include pattern-generated phrases
    - include_variations: Include variations of top phrases
    - creativity: How experimental to be (low/medium/high)
    """
    niche_list = None
    if niches:
        niche_list = [n.strip() for n in niches.split(",") if n.strip()]

    result = idea_generator.generate_ideas(
        count=count,
        niches=niche_list,
        include_classics=include_classics,
        include_generated=include_generated,
        include_variations=include_variations,
        creativity_level=creativity,
    )

    return result


@router.post("/quick")
async def quick_generate(request: QuickGenerateRequest):
    """
    Quickly generate ideas for a single topic.

    Takes a topic (like "hiking", "coffee", "nursing") and generates
    phrase ideas using proven templates.
    """
    ideas = idea_generator.quick_generate(request.topic, request.count)
    return {
        "topic": request.topic,
        "count": len(ideas),
        "ideas": ideas
    }


@router.get("/bestsellers")
async def get_bestsellers(
    niche: Optional[str] = None,
    limit: int = Query(100, ge=10, le=500)
):
    """
    Get classic bestseller phrases.

    These are proven phrases that have sold well across merch platforms.
    """
    from ..services.nlp.bestseller_patterns import (
        CLASSIC_BESTSELLERS,
        NICHE_BESTSELLERS,
    )

    phrases = list(CLASSIC_BESTSELLERS)

    if niche and niche.lower() in NICHE_BESTSELLERS:
        niche_phrases = NICHE_BESTSELLERS[niche.lower()]
        # Put niche-specific at the top
        phrases = niche_phrases + [p for p in phrases if p not in niche_phrases]
    else:
        # Add all niche phrases
        for niche_phrases in NICHE_BESTSELLERS.values():
            phrases.extend(niche_phrases)

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for p in phrases:
        if p.lower() not in seen:
            seen.add(p.lower())
            unique.append(p)

    return {
        "total": len(unique[:limit]),
        "phrases": unique[:limit]
    }


@router.get("/niches")
async def get_available_niches():
    """Get list of available niches with phrase counts."""
    from ..services.nlp.bestseller_patterns import NICHE_BESTSELLERS

    return {
        "niches": [
            {"name": niche, "count": len(phrases)}
            for niche, phrases in sorted(
                NICHE_BESTSELLERS.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )
        ]
    }


@router.get("/templates")
async def get_templates(limit: int = Query(50, ge=10, le=200)):
    """Get available phrase templates."""
    from ..services.nlp.bestseller_patterns import BESTSELLER_TEMPLATES

    return {
        "total": len(BESTSELLER_TEMPLATES),
        "templates": BESTSELLER_TEMPLATES[:limit]
    }


@router.get("/topics")
async def get_topics():
    """Get available trending topics."""
    from ..services.nlp.bestseller_patterns import TRENDING_TOPICS

    return {
        "total": len(TRENDING_TOPICS),
        "topics": TRENDING_TOPICS
    }

"""Pattern management API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List

from ..database import get_db
from ..models import Pattern, Phrase
from ..schemas import PatternResponse, PatternCreate

router = APIRouter()


@router.get("", response_model=List[PatternResponse])
async def list_patterns(
    limit: int = Query(50, ge=1, le=200),
    sort_by: str = Query("popularity_score", regex="^(popularity_score|usage_count|created_at)$"),
    db: Session = Depends(get_db)
):
    """List all detected patterns."""
    sort_column = getattr(Pattern, sort_by)
    patterns = db.query(Pattern).order_by(desc(sort_column)).limit(limit).all()
    return [PatternResponse.model_validate(p) for p in patterns]


@router.get("/popular")
async def get_popular_patterns(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get most popular patterns."""
    patterns = db.query(Pattern).order_by(
        desc(Pattern.popularity_score)
    ).limit(limit).all()

    return [
        {
            "id": p.id,
            "template": p.template,
            "description": p.description,
            "popularity_score": p.popularity_score,
            "usage_count": p.usage_count,
            "examples": p.example_phrases
        }
        for p in patterns
    ]


@router.get("/{pattern_id}", response_model=PatternResponse)
async def get_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """Get a specific pattern."""
    pattern = db.query(Pattern).filter(Pattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return PatternResponse.model_validate(pattern)


@router.get("/{pattern_id}/phrases")
async def get_pattern_phrases(
    pattern_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get phrases that match a pattern."""
    pattern = db.query(Pattern).filter(Pattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Find phrases with this pattern
    phrases = db.query(Phrase).filter(
        Phrase.is_pattern == True,
        Phrase.pattern_template == pattern.template,
        Phrase.is_safe == True
    ).order_by(desc(Phrase.trend_score)).limit(limit).all()

    return {
        "pattern": pattern.template,
        "phrases": [
            {
                "id": p.id,
                "text": p.text,
                "trend_score": p.trend_score,
                "niche": p.niche
            }
            for p in phrases
        ]
    }


@router.post("/generate")
async def generate_from_pattern(
    pattern_id: int,
    variables: List[str],
    db: Session = Depends(get_db)
):
    """Generate a phrase from a pattern template."""
    from ..services.nlp.pattern_detector import PatternDetector
    from ..services.trademark.checker import TrademarkChecker

    pattern = db.query(Pattern).filter(Pattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    detector = PatternDetector()
    generated = detector.fill_pattern(pattern.template, variables)

    # Check safety
    checker = TrademarkChecker()
    safety = checker.check_phrase(generated, db)

    return {
        "pattern": pattern.template,
        "variables": variables,
        "generated": generated,
        "is_safe": safety["is_safe"],
        "risk_score": safety["risk_score"]
    }


@router.post("", response_model=PatternResponse)
async def create_pattern(
    pattern: PatternCreate,
    db: Session = Depends(get_db)
):
    """Manually add a pattern."""
    import json

    existing = db.query(Pattern).filter(
        Pattern.template == pattern.template
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Pattern already exists")

    # Count variables in template
    variable_count = pattern.template.count("{")

    db_pattern = Pattern(
        template=pattern.template,
        description=pattern.description,
        example_phrases=json.dumps(pattern.example_phrases) if pattern.example_phrases else None,
        variable_count=variable_count
    )

    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)

    return PatternResponse.model_validate(db_pattern)


@router.delete("/{pattern_id}")
async def delete_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """Delete a pattern."""
    pattern = db.query(Pattern).filter(Pattern.id == pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    db.delete(pattern)
    db.commit()
    return {"status": "deleted", "id": pattern_id}

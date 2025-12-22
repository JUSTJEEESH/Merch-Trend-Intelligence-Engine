"""Phrase management API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional, List

from ..database import get_db
from ..models import Phrase, PhraseMetrics
from ..schemas import (
    PhraseResponse, PhraseListResponse, PhraseCreate,
    PhraseFilter, VariationRequest, VariationResponse
)
from ..services.nlp.extractor import NLPExtractor
from ..services.trademark.checker import TrademarkChecker
from ..services.scoring.trend_scorer import TrendScorer

router = APIRouter()
nlp_extractor = NLPExtractor()
trademark_checker = TrademarkChecker()
trend_scorer = TrendScorer()


@router.get("", response_model=PhraseListResponse)
async def list_phrases(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    niche: Optional[str] = None,
    min_trend_score: Optional[float] = None,
    max_risk_score: Optional[float] = None,
    min_word_count: Optional[int] = None,
    max_word_count: Optional[int] = None,
    is_safe: Optional[bool] = True,
    is_pattern: Optional[bool] = None,
    sort_by: str = Query("trend_score", regex="^(trend_score|frequency|first_seen|risk_score)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """List phrases with filtering and pagination."""
    query = db.query(Phrase)

    # Apply filters
    if niche:
        query = query.filter(Phrase.niche == niche)
    if min_trend_score is not None:
        query = query.filter(Phrase.trend_score >= min_trend_score)
    if max_risk_score is not None:
        query = query.filter(Phrase.risk_score <= max_risk_score)
    if min_word_count is not None:
        query = query.filter(Phrase.word_count >= min_word_count)
    if max_word_count is not None:
        query = query.filter(Phrase.word_count <= max_word_count)
    if is_safe is not None:
        query = query.filter(Phrase.is_safe == is_safe)
    if is_pattern is not None:
        query = query.filter(Phrase.is_pattern == is_pattern)

    # Get total count
    total = query.count()

    # Apply sorting
    sort_column = getattr(Phrase, sort_by)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Apply pagination
    offset = (page - 1) * page_size
    phrases = query.offset(offset).limit(page_size).all()

    return PhraseListResponse(
        phrases=[PhraseResponse.model_validate(p) for p in phrases],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/trending")
async def get_trending_phrases(
    limit: int = Query(20, ge=1, le=100),
    niche: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get top trending safe phrases."""
    query = db.query(Phrase).filter(Phrase.is_safe == True)

    if niche:
        query = query.filter(Phrase.niche == niche)

    phrases = query.order_by(desc(Phrase.trend_score)).limit(limit).all()

    return [PhraseResponse.model_validate(p) for p in phrases]


@router.get("/emerging")
async def get_emerging_phrases(
    limit: int = Query(20, ge=1, le=100),
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get recently emerged phrases with high velocity."""
    from datetime import datetime, timedelta

    cutoff = datetime.utcnow() - timedelta(days=days)

    phrases = db.query(Phrase).join(PhraseMetrics).filter(
        Phrase.is_safe == True,
        Phrase.first_seen >= cutoff
    ).order_by(desc(PhraseMetrics.velocity)).limit(limit).all()

    return [PhraseResponse.model_validate(p) for p in phrases]


@router.get("/niches")
async def get_niches(db: Session = Depends(get_db)):
    """Get list of all niches with counts."""
    from sqlalchemy import func

    results = db.query(
        Phrase.niche,
        func.count(Phrase.id).label("count")
    ).filter(
        Phrase.niche.isnot(None)
    ).group_by(Phrase.niche).order_by(desc("count")).all()

    return [{"niche": niche, "count": count} for niche, count in results]


@router.get("/{phrase_id}", response_model=PhraseResponse)
async def get_phrase(phrase_id: int, db: Session = Depends(get_db)):
    """Get a specific phrase by ID."""
    phrase = db.query(Phrase).filter(Phrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")
    return PhraseResponse.model_validate(phrase)


@router.get("/{phrase_id}/history")
async def get_phrase_history(
    phrase_id: int,
    days: int = Query(30, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Get historical data for a phrase."""
    from ..models import PhraseHistory
    from datetime import datetime, timedelta

    phrase = db.query(Phrase).filter(Phrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")

    cutoff = datetime.utcnow() - timedelta(days=days)

    history = db.query(PhraseHistory).filter(
        PhraseHistory.phrase_id == phrase_id,
        PhraseHistory.date >= cutoff
    ).order_by(PhraseHistory.date).all()

    return {
        "phrase": phrase.text,
        "history": [
            {
                "date": h.date.isoformat(),
                "frequency": h.frequency,
                "trend_score": h.trend_score,
                "velocity": h.velocity
            }
            for h in history
        ]
    }


@router.post("/analyze")
async def analyze_phrase(text: str, db: Session = Depends(get_db)):
    """Analyze a phrase for trends and safety."""
    # Check trademark safety
    safety_result = trademark_checker.check_phrase(text, db)

    # Calculate trend score
    trend_result = trend_scorer.calculate_score(text, db)

    # Extract pattern if applicable
    pattern = nlp_extractor.extract_pattern(text)

    return {
        "text": text,
        "normalized": nlp_extractor.normalize_text(text),
        "word_count": len(text.split()),
        "is_safe": safety_result["is_safe"],
        "risk_score": safety_result["risk_score"],
        "risk_details": safety_result.get("matches", []),
        "trend_score": trend_result.get("score", 0),
        "trend_details": trend_result,
        "pattern": pattern
    }


@router.post("/variations", response_model=VariationResponse)
async def generate_variations(
    request: VariationRequest,
    db: Session = Depends(get_db)
):
    """Generate variations of a phrase."""
    from ..services.nlp.variation_generator import VariationGenerator

    generator = VariationGenerator()
    variations = generator.generate(
        request.phrase,
        variation_type=request.variation_type,
        count=request.count
    )

    # Check each variation for safety
    safe_variations = []
    for var in variations:
        safety = trademark_checker.check_phrase(var["text"], db)
        var["is_safe"] = safety["is_safe"]
        var["risk_score"] = safety["risk_score"]
        safe_variations.append(var)

    return VariationResponse(
        original=request.phrase,
        variations=safe_variations,
        all_safe=all(v["is_safe"] for v in safe_variations)
    )


@router.delete("/{phrase_id}")
async def delete_phrase(phrase_id: int, db: Session = Depends(get_db)):
    """Delete a phrase."""
    phrase = db.query(Phrase).filter(Phrase.id == phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")

    db.delete(phrase)
    db.commit()
    return {"status": "deleted", "id": phrase_id}

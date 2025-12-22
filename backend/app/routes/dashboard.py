"""Dashboard API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Phrase, Pattern, Trademark, ScrapingLog
from ..schemas import DashboardStats

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    # Total phrases
    total_phrases = db.query(func.count(Phrase.id)).scalar() or 0

    # Safe phrases
    safe_phrases = db.query(func.count(Phrase.id)).filter(
        Phrase.is_safe == True
    ).scalar() or 0

    # Trending phrases (trend_score > 50)
    trending_phrases = db.query(func.count(Phrase.id)).filter(
        Phrase.trend_score > 50,
        Phrase.is_safe == True
    ).scalar() or 0

    # Patterns detected
    patterns_detected = db.query(func.count(Pattern.id)).scalar() or 0

    # Total trademarks
    total_trademarks = db.query(func.count(Trademark.id)).scalar() or 0

    # Last scrape time
    last_log = db.query(ScrapingLog).order_by(
        desc(ScrapingLog.completed_at)
    ).first()
    last_scrape = last_log.completed_at if last_log else None

    # Top niches
    niche_counts = db.query(
        Phrase.niche,
        func.count(Phrase.id).label("count")
    ).filter(
        Phrase.niche.isnot(None),
        Phrase.is_safe == True
    ).group_by(Phrase.niche).order_by(
        desc("count")
    ).limit(5).all()

    top_niches = [
        {"niche": niche, "count": count}
        for niche, count in niche_counts
    ]

    # Recent trends (top 10 by trend score in last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent = db.query(Phrase).filter(
        Phrase.first_seen >= week_ago,
        Phrase.is_safe == True
    ).order_by(desc(Phrase.trend_score)).limit(10).all()

    recent_trends = [
        {
            "id": p.id,
            "text": p.text,
            "trend_score": p.trend_score,
            "first_seen": p.first_seen.isoformat() if p.first_seen else None
        }
        for p in recent
    ]

    return DashboardStats(
        total_phrases=total_phrases,
        safe_phrases=safe_phrases,
        trending_phrases=trending_phrases,
        patterns_detected=patterns_detected,
        total_trademarks=total_trademarks,
        last_scrape=last_scrape,
        top_niches=top_niches,
        recent_trends=recent_trends
    )


@router.get("/activity")
async def get_recent_activity(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get recent scraping activity."""
    logs = db.query(ScrapingLog).order_by(
        desc(ScrapingLog.started_at)
    ).limit(limit).all()

    return [
        {
            "id": log.id,
            "source": log.source_name,
            "status": log.status,
            "items_collected": log.items_collected,
            "phrases_extracted": log.phrases_extracted,
            "started_at": log.started_at.isoformat() if log.started_at else None,
            "completed_at": log.completed_at.isoformat() if log.completed_at else None,
            "error": log.error_message
        }
        for log in logs
    ]

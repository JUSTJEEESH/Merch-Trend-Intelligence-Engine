"""Scraping API routes."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import Source, ScrapingLog
from ..schemas import ScrapeRequest, ScrapeResponse
from ..services.scraper.reddit_scraper import RedditScraper
from ..services.scraper.google_trends_scraper import GoogleTrendsScraper
from ..services.scraper.amazon_scraper import AmazonScraper
from ..services.scraper.etsy_scraper import EtsyScraper
from ..services.nlp.extractor import NLPExtractor

router = APIRouter()
nlp_extractor = NLPExtractor()


async def run_scrape_job(
    source_type: str,
    target: Optional[str],
    limit: int,
    db: Session,
    log_id: int
):
    """Background task for running scrape jobs."""
    log = db.query(ScrapingLog).filter(ScrapingLog.id == log_id).first()

    try:
        items = []

        if source_type == "reddit":
            scraper = RedditScraper()
            items = await scraper.scrape(subreddit=target, limit=limit)
        elif source_type == "google_trends":
            scraper = GoogleTrendsScraper()
            items = await scraper.scrape(keyword=target)
        elif source_type == "amazon":
            scraper = AmazonScraper()
            items = await scraper.scrape(search_term=target, limit=limit)
        elif source_type == "etsy":
            scraper = EtsyScraper()
            items = await scraper.scrape(search_term=target, limit=limit)
        else:
            raise ValueError(f"Unknown source type: {source_type}")

        # Extract phrases from collected items
        phrases_extracted = 0
        for item in items:
            extracted = nlp_extractor.extract_phrases(
                item.get("text", ""),
                source_type=source_type,
                source_context=item.get("context", ""),
                db=db
            )
            phrases_extracted += len(extracted)

        # Update log
        log.status = "completed"
        log.items_collected = len(items)
        log.phrases_extracted = phrases_extracted
        log.completed_at = datetime.utcnow()

        # Update source last_scraped
        source = db.query(Source).filter(Source.name == source_type).first()
        if source:
            source.last_scraped = datetime.utcnow()

        db.commit()

    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.utcnow()
        db.commit()
        raise


@router.post("/start", response_model=ScrapeResponse)
async def start_scrape(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a scraping job."""
    # Ensure source exists
    source = db.query(Source).filter(Source.name == request.source_type).first()
    if not source:
        source = Source(
            name=request.source_type,
            source_type=request.source_type,
            is_active=True
        )
        db.add(source)
        db.commit()

    # Create scraping log
    log = ScrapingLog(
        source_name=request.source_type,
        started_at=datetime.utcnow(),
        status="running"
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # Start background task
    background_tasks.add_task(
        run_scrape_job,
        request.source_type,
        request.target,
        request.limit,
        db,
        log.id
    )

    return ScrapeResponse(
        source=request.source_type,
        status="started",
        items_collected=0,
        phrases_extracted=0,
        started_at=log.started_at
    )


@router.get("/status/{log_id}")
async def get_scrape_status(log_id: int, db: Session = Depends(get_db)):
    """Get status of a scraping job."""
    log = db.query(ScrapingLog).filter(ScrapingLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Scraping log not found")

    return {
        "id": log.id,
        "source": log.source_name,
        "status": log.status,
        "items_collected": log.items_collected,
        "phrases_extracted": log.phrases_extracted,
        "started_at": log.started_at.isoformat() if log.started_at else None,
        "completed_at": log.completed_at.isoformat() if log.completed_at else None,
        "error": log.error_message
    }


@router.get("/sources")
async def list_sources(db: Session = Depends(get_db)):
    """List all data sources."""
    sources = db.query(Source).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "type": s.source_type,
            "url": s.url,
            "last_scraped": s.last_scraped.isoformat() if s.last_scraped else None,
            "is_active": s.is_active
        }
        for s in sources
    ]


@router.get("/logs")
async def list_scraping_logs(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List recent scraping logs."""
    from sqlalchemy import desc

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


@router.post("/reddit")
async def scrape_reddit(
    subreddit: str = "memes",
    limit: int = 100,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Scrape a specific subreddit."""
    request = ScrapeRequest(
        source_type="reddit",
        target=subreddit,
        limit=limit
    )
    return await start_scrape(request, background_tasks, db)


@router.post("/google-trends")
async def scrape_google_trends(
    keyword: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Scrape Google Trends."""
    request = ScrapeRequest(
        source_type="google_trends",
        target=keyword,
        limit=100
    )
    return await start_scrape(request, background_tasks, db)


@router.post("/amazon")
async def scrape_amazon(
    search_term: str,
    limit: int = 50,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Scrape Amazon search results."""
    request = ScrapeRequest(
        source_type="amazon",
        target=search_term,
        limit=limit
    )
    return await start_scrape(request, background_tasks, db)

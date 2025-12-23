"""Advanced tools API routes - trending, AI generation, analytics, design, and more."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

# Import all services
from ..services.trending import social_trends_service
from ..services.seasonal import seasonal_calendar
from ..services.ai import ai_phrase_generator
from ..services.analytics import bsr_tracker, profitability_calculator
from ..services.design import design_generator
from ..services.listing import listing_optimizer

router = APIRouter(prefix="/api/tools", tags=["tools"])


# ============ Request Models ============

class AIPhraseRequest(BaseModel):
    topic: str
    tone: str = "funny"
    count: int = 20


class ListingRequest(BaseModel):
    phrase: str
    niche: str = "general"
    product: str = "T-Shirt"
    tone: str = "funny"


class DesignRequest(BaseModel):
    phrase: str
    style: str = "funny"


class ROIRequest(BaseModel):
    design_cost: float = 0
    time_invested_hours: float = 1
    hourly_value: float = 25
    estimated_monthly_sales: int = 5
    royalty: float = 4.51


class PortfolioRequest(BaseModel):
    designs_count: int
    avg_sales_per_design: float
    product: str = "standard_tee"


# ============ Trending Routes ============

@router.get("/trending/all")
async def get_all_trends(limit_per_platform: int = Query(15, ge=5, le=50)):
    """Get trending topics from TikTok, Twitter, and Reddit."""
    try:
        trends = await social_trends_service.get_all_trends(limit_per_platform)
        return {"success": True, "data": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/tiktok")
async def get_tiktok_trends(limit: int = Query(25, ge=5, le=50)):
    """Get trending topics from TikTok."""
    try:
        trends = await social_trends_service.get_tiktok_trends(limit)
        return {"success": True, "platform": "tiktok", "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/twitter")
async def get_twitter_trends(limit: int = Query(20, ge=5, le=50)):
    """Get trending topics from Twitter/X."""
    try:
        trends = await social_trends_service.get_twitter_trends(limit)
        return {"success": True, "platform": "twitter", "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/reddit")
async def get_reddit_trends(limit: int = Query(10, ge=5, le=25)):
    """Get trending topics from Reddit."""
    try:
        trends = await social_trends_service.get_reddit_trends(limit)
        return {"success": True, "platform": "reddit", "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/niche/{niche}")
async def get_trending_for_niche(niche: str):
    """Get trending phrases filtered by niche."""
    try:
        trends = await social_trends_service.get_trending_phrases_for_niche(niche)
        return {"success": True, "niche": niche, "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trending/refresh")
async def refresh_trends():
    """Clear trends cache and fetch fresh data from all sources."""
    try:
        social_trends_service.clear_cache()
        # Fetch fresh data
        trends = await social_trends_service.get_all_trends(15)
        return {
            "success": True,
            "message": "Cache cleared and fresh trends fetched",
            "data": trends,
            "refreshed_at": trends.get("fetched_at")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ Seasonal Calendar Routes ============

@router.get("/calendar/upcoming")
async def get_upcoming_events(days: int = Query(90, ge=7, le=365)):
    """Get upcoming holidays and events."""
    try:
        events = seasonal_calendar.get_upcoming_events(days)
        return {"success": True, "days_ahead": days, "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/overview")
async def get_calendar_overview():
    """Get complete calendar overview with urgency flags."""
    try:
        overview = seasonal_calendar.get_calendar_overview()
        return {"success": True, "data": overview}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/niche/{niche}")
async def get_events_for_niche(niche: str):
    """Get events relevant to a specific niche."""
    try:
        events = seasonal_calendar.get_events_for_niche(niche)
        return {"success": True, "niche": niche, "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/event/{event_name}/phrases")
async def get_event_phrases(event_name: str):
    """Get suggested phrases for a specific event."""
    try:
        phrases = seasonal_calendar.get_suggested_phrases_for_event(event_name)
        return {"success": True, "event": event_name, "phrases": phrases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ AI Phrase Generator Routes ============

@router.post("/ai/generate")
async def generate_ai_phrases(request: AIPhraseRequest):
    """Generate phrases using AI with tone control."""
    try:
        phrases = ai_phrase_generator.generate_phrases(
            topic=request.topic,
            tone=request.tone,
            count=request.count,
        )
        return {"success": True, "phrases": phrases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/generate-bulk")
async def generate_bulk_phrases(topic: str, count_per_tone: int = Query(10, ge=5, le=25)):
    """Generate phrases in all available tones."""
    try:
        results = ai_phrase_generator.generate_bulk(topic, count_per_tone=count_per_tone)
        return {"success": True, "topic": topic, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai/tones")
async def get_available_tones():
    """Get list of available tones for phrase generation."""
    tones = ai_phrase_generator.get_available_tones()
    topics = ai_phrase_generator.get_available_topics()
    return {"tones": tones, "topics_with_vocabulary": topics}


@router.get("/ai/suggest-tones/{topic}")
async def suggest_tones_for_topic(topic: str):
    """Get suggested tones for a topic."""
    suggestions = ai_phrase_generator.suggest_tones_for_topic(topic)
    return {"topic": topic, "suggested_tones": suggestions}


# ============ BSR Tracker Routes ============

@router.get("/bsr/estimate/{bsr}")
async def estimate_sales_from_bsr(bsr: int):
    """Estimate sales and revenue from a BSR value."""
    try:
        estimate = bsr_tracker.estimate_sales_from_bsr(bsr)
        return {"success": True, "data": estimate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bsr/niche/{niche}")
async def get_niche_bsr_data(niche: str):
    """Get BSR statistics for a niche."""
    try:
        data = bsr_tracker.get_niche_bsr_data(niche)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bsr/history/{keyword}")
async def get_bsr_history(keyword: str, days: int = Query(30, ge=7, le=90)):
    """Get simulated BSR history for a keyword."""
    try:
        history = bsr_tracker.simulate_bsr_history(keyword, days)
        analysis = bsr_tracker.analyze_bsr_trend(history)
        return {"success": True, "keyword": keyword, "history": history, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bsr/opportunities")
async def get_bsr_opportunities():
    """Get niches with good BSR opportunity."""
    try:
        opportunities = bsr_tracker.get_bsr_opportunities()
        return {"success": True, "opportunities": opportunities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ Profitability Routes ============

@router.get("/profitability/niche/{niche}")
async def calculate_niche_profitability(niche: str):
    """Calculate profitability score for a niche."""
    try:
        data = profitability_calculator.calculate_niche_profitability(niche)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profitability/best-niches")
async def get_best_niches(count: int = Query(10, ge=5, le=25)):
    """Get the most profitable niches."""
    try:
        niches = profitability_calculator.get_best_niches(count)
        return {"success": True, "niches": niches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profitability/compare")
async def compare_niches(niches: List[str]):
    """Compare profitability across multiple niches."""
    try:
        comparison = profitability_calculator.compare_niches(niches)
        return {"success": True, "comparison": comparison}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profitability/projection")
async def calculate_revenue_projection(
    monthly_sales: int = Query(..., ge=1),
    product: str = Query("standard_tee"),
    months: int = Query(12, ge=1, le=24),
):
    """Project revenue based on estimated sales."""
    try:
        projection = profitability_calculator.calculate_revenue_projection(
            monthly_sales, product, months
        )
        return {"success": True, "projection": projection}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profitability/roi")
async def calculate_design_roi(request: ROIRequest):
    """Calculate ROI for a design."""
    try:
        roi = profitability_calculator.calculate_design_roi(
            design_cost=request.design_cost,
            time_invested_hours=request.time_invested_hours,
            hourly_value=request.hourly_value,
            estimated_monthly_sales=request.estimated_monthly_sales,
            royalty=request.royalty,
        )
        return {"success": True, "roi": roi}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profitability/portfolio")
async def calculate_portfolio_metrics(request: PortfolioRequest):
    """Calculate metrics for entire design portfolio."""
    try:
        metrics = profitability_calculator.calculate_portfolio_metrics(
            designs_count=request.designs_count,
            avg_sales_per_design=request.avg_sales_per_design,
            product=request.product,
        )
        return {"success": True, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ Design Generator Routes ============

@router.post("/design/concept")
async def generate_design_concept(request: DesignRequest):
    """Generate a design concept for a phrase."""
    try:
        concept = design_generator.generate_concept(request.phrase, request.style)
        return {"success": True, "concept": concept}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/design/concepts/{phrase}")
async def get_multiple_concepts(phrase: str, count: int = Query(3, ge=1, le=5)):
    """Generate multiple design concepts for a phrase."""
    try:
        concepts = design_generator.get_concepts_for_phrase(phrase, count)
        return {"success": True, "phrase": phrase, "concepts": concepts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/design/colors/{niche}")
async def get_color_palettes_for_niche(niche: str):
    """Get recommended color palettes for a niche."""
    try:
        palettes = design_generator.get_color_palette_for_niche(niche)
        return {"success": True, "data": palettes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ Listing Optimizer Routes ============

@router.post("/listing/optimize")
async def generate_optimized_listing(request: ListingRequest):
    """Generate a complete optimized Amazon listing."""
    try:
        listing = listing_optimizer.generate_full_listing(
            phrase=request.phrase,
            niche=request.niche,
            product=request.product,
            tone=request.tone,
        )
        return {"success": True, "listing": listing}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/listing/title")
async def generate_title(request: ListingRequest):
    """Generate an optimized title."""
    try:
        title = listing_optimizer.generate_title(
            phrase=request.phrase,
            niche=request.niche,
            product=request.product,
            tone=request.tone,
        )
        return {"success": True, "title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/listing/keywords")
async def generate_keywords(phrase: str, niche: str = "general"):
    """Generate backend keywords."""
    try:
        keywords = listing_optimizer.generate_keywords(phrase, niche)
        return {"success": True, "keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""SEO generation API routes - Amazon TOS compliant."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import SEOListing, Phrase
from ..schemas import (
    SEOListingResponse, SEOListingCreate,
    SEOGenerateRequest, SEOGenerateResponse,
    SEOFieldResponse, SEODescriptionFieldResponse,
    SEOKeywordsFieldResponse, SEOValidationResponse
)
from ..services.seo.generator import SEOGenerator
from ..services.trademark.checker import TrademarkChecker

router = APIRouter()
seo_generator = SEOGenerator()
trademark_checker = TrademarkChecker()


@router.post("/generate", response_model=SEOGenerateResponse)
async def generate_seo_listing(
    request: SEOGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate Amazon TOS-compliant listing content.

    Returns structured response with:
    - Title (60 chars max)
    - Brand (50 chars max)
    - Bullet 1 (256 chars max)
    - Bullet 2 (256 chars max)
    - Description (75-2000 chars)
    - Keywords (250 bytes max)
    """
    # First check if phrase is safe
    safety = trademark_checker.check_phrase(request.phrase, db)
    if not safety["is_safe"]:
        # Return empty but structured response for unsafe phrases
        return SEOGenerateResponse(
            phrase=request.phrase,
            niche="general",
            style=request.tone or "funny",
            title=SEOFieldResponse(text="", length=0, limit=60, compliant=False),
            brand=SEOFieldResponse(text="", length=0, limit=50, compliant=False),
            bullet_1=SEOFieldResponse(text="", length=0, limit=256, compliant=False),
            bullet_2=SEOFieldResponse(text="", length=0, limit=256, compliant=False),
            description=SEODescriptionFieldResponse(text="", length=0, limit_min=75, limit_max=2000, compliant=False),
            keywords=SEOKeywordsFieldResponse(text="", byte_count=0, limit=250, compliant=False),
            validation=SEOValidationResponse(is_compliant=False, issues=["Phrase failed trademark check"], checks_passed=0, total_checks=7),
            warnings=["Phrase failed trademark check"] + safety.get("warnings", [])
        )

    # Generate SEO content (tone maps to style in new generator)
    result = seo_generator.generate(
        phrase=request.phrase,
        niche=request.niche,
        style=request.tone or "funny"
    )

    return SEOGenerateResponse(
        phrase=result["phrase"],
        niche=result["niche"],
        style=result["style"],
        title=SEOFieldResponse(**result["title"]),
        brand=SEOFieldResponse(**result["brand"]),
        bullet_1=SEOFieldResponse(**result["bullet_1"]),
        bullet_2=SEOFieldResponse(**result["bullet_2"]),
        description=SEODescriptionFieldResponse(**result["description"]),
        keywords=SEOKeywordsFieldResponse(**result["keywords"]),
        validation=SEOValidationResponse(**result["validation"]),
        warnings=result["validation"].get("issues", [])
    )


@router.post("/generate-batch")
async def generate_seo_batch(
    phrases: List[str],
    niche: str = None,
    tone: str = "funny",
    db: Session = Depends(get_db)
):
    """Generate SEO content for multiple phrases."""
    results = []

    for phrase in phrases:
        # Check safety
        safety = trademark_checker.check_phrase(phrase, db)
        if not safety["is_safe"]:
            results.append({
                "phrase": phrase,
                "is_compliant": False,
                "error": "Failed trademark check"
            })
            continue

        # Generate content (tone maps to style)
        result = seo_generator.generate(
            phrase=phrase,
            niche=niche,
            style=tone
        )
        # Flatten for batch response (extract text from nested dicts)
        results.append({
            "phrase": result["phrase"],
            "niche": result["niche"],
            "style": result["style"],
            "title": result["title"]["text"],
            "brand": result["brand"]["text"],
            "bullet_1": result["bullet_1"]["text"],
            "bullet_2": result["bullet_2"]["text"],
            "description": result["description"]["text"],
            "keywords": result["keywords"]["text"],
            "is_compliant": result["validation"]["is_compliant"],
            "issues": result["validation"]["issues"],
        })

    return results


@router.get("/listings", response_model=List[SEOListingResponse])
async def list_seo_listings(
    limit: int = 50,
    phrase_id: int = None,
    db: Session = Depends(get_db)
):
    """List saved SEO listings."""
    query = db.query(SEOListing)

    if phrase_id:
        query = query.filter(SEOListing.phrase_id == phrase_id)

    listings = query.order_by(SEOListing.created_at.desc()).limit(limit).all()
    return [SEOListingResponse.model_validate(l) for l in listings]


@router.get("/listings/{listing_id}", response_model=SEOListingResponse)
async def get_seo_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a specific SEO listing."""
    listing = db.query(SEOListing).filter(SEOListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return SEOListingResponse.model_validate(listing)


@router.post("/listings", response_model=SEOListingResponse)
async def save_seo_listing(
    listing: SEOListingCreate,
    db: Session = Depends(get_db)
):
    """Save an SEO listing."""
    # Verify phrase exists
    phrase = db.query(Phrase).filter(Phrase.id == listing.phrase_id).first()
    if not phrase:
        raise HTTPException(status_code=404, detail="Phrase not found")

    # Validate content
    validation = seo_generator.validate_listing(
        title=listing.title,
        bullet_1=listing.bullet_1,
        bullet_2=listing.bullet_2,
        description=listing.description,
        backend_keywords=listing.backend_keywords
    )

    db_listing = SEOListing(
        phrase_id=listing.phrase_id,
        title=listing.title,
        bullet_1=listing.bullet_1,
        bullet_2=listing.bullet_2,
        description=listing.description,
        backend_keywords=listing.backend_keywords,
        is_compliant=validation["is_compliant"]
    )

    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)

    return SEOListingResponse.model_validate(db_listing)


@router.delete("/listings/{listing_id}")
async def delete_seo_listing(listing_id: int, db: Session = Depends(get_db)):
    """Delete an SEO listing."""
    listing = db.query(SEOListing).filter(SEOListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(listing)
    db.commit()
    return {"status": "deleted", "id": listing_id}


@router.post("/validate")
async def validate_listing(
    title: str,
    bullet_1: str = None,
    bullet_2: str = None,
    description: str = None,
    backend_keywords: str = None
):
    """Validate SEO listing content against Amazon Merch guidelines."""
    result = seo_generator.validate_listing(
        title=title,
        bullet_1=bullet_1,
        bullet_2=bullet_2,
        description=description,
        backend_keywords=backend_keywords
    )
    return result


@router.get("/forbidden-words")
async def get_forbidden_words():
    """Get list of forbidden words in Amazon Merch listings."""
    return {
        "forbidden": seo_generator.FORBIDDEN_TERMS,
        "limits": seo_generator.LIMITS,
        "available_niches": seo_generator.get_available_niches(),
        "available_styles": seo_generator.get_available_styles(),
        "note": "These terms are forbidden by Amazon TOS - content must describe the design only"
    }

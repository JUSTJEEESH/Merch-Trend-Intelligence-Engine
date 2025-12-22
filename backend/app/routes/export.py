"""Export API routes."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
import json
import csv
import os
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..models import Phrase, PhraseMetrics, SEOListing
from ..schemas import ExportRequest, ExportResponse, PhraseFilter
from ..config import settings

router = APIRouter()


def apply_phrase_filters(query, filters: PhraseFilter):
    """Apply filters to phrase query."""
    if filters.niche:
        query = query.filter(Phrase.niche == filters.niche)
    if filters.min_trend_score is not None:
        query = query.filter(Phrase.trend_score >= filters.min_trend_score)
    if filters.max_risk_score is not None:
        query = query.filter(Phrase.risk_score <= filters.max_risk_score)
    if filters.min_word_count is not None:
        query = query.filter(Phrase.word_count >= filters.min_word_count)
    if filters.max_word_count is not None:
        query = query.filter(Phrase.word_count <= filters.max_word_count)
    if filters.is_safe is not None:
        query = query.filter(Phrase.is_safe == filters.is_safe)
    if filters.is_pattern is not None:
        query = query.filter(Phrase.is_pattern == filters.is_pattern)
    return query


@router.post("/phrases", response_model=ExportResponse)
async def export_phrases(
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """Export phrases to CSV or JSON."""
    query = db.query(Phrase)

    # Apply filters
    if request.filters:
        query = apply_phrase_filters(query, request.filters)

    # Default to safe phrases only
    query = query.filter(Phrase.is_safe == True)
    query = query.order_by(desc(Phrase.trend_score))

    phrases = query.all()

    # Generate filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"phrases_export_{timestamp}.{request.format}"
    filepath = settings.PROCESSED_DATA_DIR / filename

    if request.format == "csv":
        await export_to_csv(phrases, filepath, request.include_metrics)
    else:
        await export_to_json(phrases, filepath, request.include_metrics)

    return ExportResponse(
        filename=filename,
        format=request.format,
        record_count=len(phrases),
        file_path=str(filepath)
    )


async def export_to_csv(phrases, filepath, include_metrics=True):
    """Export phrases to CSV file."""
    headers = [
        "id", "text", "normalized_text", "niche", "frequency",
        "trend_score", "risk_score", "is_safe", "word_count",
        "is_pattern", "pattern_template", "first_seen", "last_seen"
    ]

    if include_metrics:
        headers.extend([
            "velocity", "novelty_score", "saturation_score",
            "cross_platform_score", "amazon_results", "etsy_results"
        ])

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for phrase in phrases:
            row = [
                phrase.id,
                phrase.text,
                phrase.normalized_text,
                phrase.niche,
                phrase.frequency,
                phrase.trend_score,
                phrase.risk_score,
                phrase.is_safe,
                phrase.word_count,
                phrase.is_pattern,
                phrase.pattern_template,
                phrase.first_seen.isoformat() if phrase.first_seen else "",
                phrase.last_seen.isoformat() if phrase.last_seen else ""
            ]

            if include_metrics and phrase.metrics:
                row.extend([
                    phrase.metrics.velocity,
                    phrase.metrics.novelty_score,
                    phrase.metrics.saturation_score,
                    phrase.metrics.cross_platform_score,
                    phrase.metrics.amazon_results,
                    phrase.metrics.etsy_results
                ])
            elif include_metrics:
                row.extend([0, 0, 0, 0, 0, 0])

            writer.writerow(row)


async def export_to_json(phrases, filepath, include_metrics=True):
    """Export phrases to JSON file."""
    data = []

    for phrase in phrases:
        item = {
            "id": phrase.id,
            "text": phrase.text,
            "normalized_text": phrase.normalized_text,
            "niche": phrase.niche,
            "frequency": phrase.frequency,
            "trend_score": phrase.trend_score,
            "risk_score": phrase.risk_score,
            "is_safe": phrase.is_safe,
            "word_count": phrase.word_count,
            "is_pattern": phrase.is_pattern,
            "pattern_template": phrase.pattern_template,
            "first_seen": phrase.first_seen.isoformat() if phrase.first_seen else None,
            "last_seen": phrase.last_seen.isoformat() if phrase.last_seen else None
        }

        if include_metrics and phrase.metrics:
            item["metrics"] = {
                "velocity": phrase.metrics.velocity,
                "novelty_score": phrase.metrics.novelty_score,
                "saturation_score": phrase.metrics.saturation_score,
                "cross_platform_score": phrase.metrics.cross_platform_score,
                "amazon_results": phrase.metrics.amazon_results,
                "etsy_results": phrase.metrics.etsy_results
            }

        data.append(item)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@router.post("/seo")
async def export_seo_listings(
    phrase_ids: list = None,
    format: str = "csv",
    db: Session = Depends(get_db)
):
    """Export SEO listings."""
    query = db.query(SEOListing).filter(SEOListing.is_compliant == True)

    if phrase_ids:
        query = query.filter(SEOListing.phrase_id.in_(phrase_ids))

    listings = query.all()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"seo_export_{timestamp}.{format}"
    filepath = settings.PROCESSED_DATA_DIR / filename

    if format == "csv":
        headers = ["phrase_id", "title", "bullet_1", "bullet_2", "description", "backend_keywords"]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for listing in listings:
                writer.writerow([
                    listing.phrase_id,
                    listing.title,
                    listing.bullet_1,
                    listing.bullet_2,
                    listing.description,
                    listing.backend_keywords
                ])
    else:
        data = [
            {
                "phrase_id": l.phrase_id,
                "title": l.title,
                "bullet_1": l.bullet_1,
                "bullet_2": l.bullet_2,
                "description": l.description,
                "backend_keywords": l.backend_keywords
            }
            for l in listings
        ]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    return {
        "filename": filename,
        "format": format,
        "record_count": len(listings),
        "file_path": str(filepath)
    }


@router.get("/download/{filename}")
async def download_export(filename: str):
    """Download an exported file."""
    filepath = settings.PROCESSED_DATA_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    media_type = "text/csv" if filename.endswith(".csv") else "application/json"
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type=media_type
    )


@router.get("/files")
async def list_export_files():
    """List available export files."""
    files = []
    for f in settings.PROCESSED_DATA_DIR.iterdir():
        if f.is_file() and (f.suffix == '.csv' or f.suffix == '.json'):
            stats = f.stat()
            files.append({
                "filename": f.name,
                "size": stats.st_size,
                "created": datetime.fromtimestamp(stats.st_ctime).isoformat()
            })

    return sorted(files, key=lambda x: x["created"], reverse=True)


@router.delete("/files/{filename}")
async def delete_export_file(filename: str):
    """Delete an export file."""
    filepath = settings.PROCESSED_DATA_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(filepath)
    return {"status": "deleted", "filename": filename}

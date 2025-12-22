"""Trademark and safety API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io

from ..database import get_db
from ..models import Trademark, BlockedTerm
from ..schemas import (
    TrademarkResponse, TrademarkCreate,
    TrademarkCheckRequest, TrademarkCheckResponse
)
from ..services.trademark.checker import TrademarkChecker

router = APIRouter()
checker = TrademarkChecker()


@router.get("", response_model=List[TrademarkResponse])
async def list_trademarks(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    search: str = None,
    db: Session = Depends(get_db)
):
    """List trademarks with optional search."""
    query = db.query(Trademark)

    if search:
        normalized_search = checker.normalize_text(search)
        query = query.filter(
            Trademark.normalized_term.contains(normalized_search)
        )

    offset = (page - 1) * page_size
    trademarks = query.offset(offset).limit(page_size).all()

    return [TrademarkResponse.model_validate(t) for t in trademarks]


@router.post("/check", response_model=TrademarkCheckResponse)
async def check_phrase(
    request: TrademarkCheckRequest,
    db: Session = Depends(get_db)
):
    """Check a phrase for trademark conflicts."""
    result = checker.check_phrase(request.phrase, db)

    return TrademarkCheckResponse(
        phrase=request.phrase,
        is_safe=result["is_safe"],
        risk_score=result["risk_score"],
        matches=result.get("matches", []),
        warnings=result.get("warnings", [])
    )


@router.post("/check-batch")
async def check_phrases_batch(
    phrases: List[str],
    db: Session = Depends(get_db)
):
    """Check multiple phrases for trademark conflicts."""
    results = []
    for phrase in phrases:
        result = checker.check_phrase(phrase, db)
        results.append({
            "phrase": phrase,
            "is_safe": result["is_safe"],
            "risk_score": result["risk_score"],
            "matches": result.get("matches", [])
        })
    return results


@router.post("/import")
async def import_trademarks(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import trademarks from CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV")

    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))

    imported = 0
    skipped = 0

    for row in reader:
        term = row.get('mark_text') or row.get('term') or row.get('trademark')
        if not term:
            skipped += 1
            continue

        normalized = checker.normalize_text(term)

        # Check if already exists
        existing = db.query(Trademark).filter(
            Trademark.normalized_term == normalized
        ).first()

        if existing:
            skipped += 1
            continue

        trademark = Trademark(
            term=term,
            normalized_term=normalized,
            source="csv_import",
            registration_number=row.get('registration_number'),
            status=row.get('status', 'UNKNOWN'),
            goods_services=row.get('goods_services')
        )
        db.add(trademark)
        imported += 1

    db.commit()

    return {
        "status": "completed",
        "imported": imported,
        "skipped": skipped
    }


@router.post("", response_model=TrademarkResponse)
async def add_trademark(
    trademark: TrademarkCreate,
    db: Session = Depends(get_db)
):
    """Manually add a trademark."""
    normalized = checker.normalize_text(trademark.term)

    existing = db.query(Trademark).filter(
        Trademark.normalized_term == normalized
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Trademark already exists")

    db_trademark = Trademark(
        term=trademark.term,
        normalized_term=normalized,
        source=trademark.source or "manual",
        registration_number=trademark.registration_number,
        status=trademark.status,
        goods_services=trademark.goods_services
    )

    db.add(db_trademark)
    db.commit()
    db.refresh(db_trademark)

    return TrademarkResponse.model_validate(db_trademark)


@router.delete("/{trademark_id}")
async def delete_trademark(trademark_id: int, db: Session = Depends(get_db)):
    """Delete a trademark."""
    trademark = db.query(Trademark).filter(Trademark.id == trademark_id).first()
    if not trademark:
        raise HTTPException(status_code=404, detail="Trademark not found")

    db.delete(trademark)
    db.commit()
    return {"status": "deleted", "id": trademark_id}


# Blocked terms endpoints
@router.get("/blocked")
async def list_blocked_terms(db: Session = Depends(get_db)):
    """List all manually blocked terms."""
    terms = db.query(BlockedTerm).all()
    return [
        {
            "id": t.id,
            "term": t.term,
            "reason": t.reason,
            "created_at": t.created_at.isoformat()
        }
        for t in terms
    ]


@router.post("/blocked")
async def add_blocked_term(
    term: str,
    reason: str = "manual",
    db: Session = Depends(get_db)
):
    """Add a term to the blocklist."""
    normalized = checker.normalize_text(term)

    existing = db.query(BlockedTerm).filter(
        BlockedTerm.normalized_term == normalized
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Term already blocked")

    blocked = BlockedTerm(
        term=term,
        normalized_term=normalized,
        reason=reason
    )

    db.add(blocked)
    db.commit()

    return {"status": "blocked", "term": term, "id": blocked.id}


@router.delete("/blocked/{term_id}")
async def remove_blocked_term(term_id: int, db: Session = Depends(get_db)):
    """Remove a term from the blocklist."""
    term = db.query(BlockedTerm).filter(BlockedTerm.id == term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Blocked term not found")

    db.delete(term)
    db.commit()
    return {"status": "unblocked", "id": term_id}

"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Source schemas
class SourceBase(BaseModel):
    name: str
    url: Optional[str] = None
    source_type: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int
    last_scraped: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Phrase schemas
class PhraseBase(BaseModel):
    text: str
    niche: Optional[str] = None


class PhraseCreate(PhraseBase):
    source_id: Optional[int] = None
    source_context: Optional[str] = None


class PhraseMetricsResponse(BaseModel):
    velocity: float = 0.0
    velocity_7d: float = 0.0
    velocity_30d: float = 0.0
    novelty_score: float = 0.0
    saturation_score: float = 0.0
    cross_platform_score: float = 0.0
    length_score: float = 0.0
    amazon_results: int = 0
    etsy_results: int = 0

    class Config:
        from_attributes = True


class PhraseResponse(PhraseBase):
    id: int
    normalized_text: str
    frequency: int
    trend_score: float
    risk_score: float
    is_safe: bool
    word_count: Optional[int] = None
    is_pattern: bool
    pattern_template: Optional[str] = None
    first_seen: datetime
    last_seen: datetime
    metrics: Optional[PhraseMetricsResponse] = None

    class Config:
        from_attributes = True


class PhraseListResponse(BaseModel):
    phrases: List[PhraseResponse]
    total: int
    page: int
    page_size: int


class PhraseFilter(BaseModel):
    niche: Optional[str] = None
    min_trend_score: Optional[float] = None
    max_risk_score: Optional[float] = None
    min_word_count: Optional[int] = None
    max_word_count: Optional[int] = None
    is_safe: Optional[bool] = True
    is_pattern: Optional[bool] = None
    source_type: Optional[str] = None


# Pattern schemas
class PatternBase(BaseModel):
    template: str
    description: Optional[str] = None


class PatternCreate(PatternBase):
    example_phrases: Optional[List[str]] = None


class PatternResponse(PatternBase):
    id: int
    variable_count: int
    popularity_score: float
    usage_count: int
    example_phrases: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Trademark schemas
class TrademarkBase(BaseModel):
    term: str
    source: Optional[str] = None


class TrademarkCreate(TrademarkBase):
    registration_number: Optional[str] = None
    status: Optional[str] = None
    goods_services: Optional[str] = None


class TrademarkResponse(TrademarkBase):
    id: int
    normalized_term: str
    registration_number: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TrademarkCheckRequest(BaseModel):
    phrase: str


class TrademarkCheckResponse(BaseModel):
    phrase: str
    is_safe: bool
    risk_score: float
    matches: List[dict] = []
    warnings: List[str] = []


# SEO schemas
class SEOListingBase(BaseModel):
    title: str
    bullet_1: Optional[str] = None
    bullet_2: Optional[str] = None
    description: Optional[str] = None
    backend_keywords: Optional[str] = None


class SEOListingCreate(SEOListingBase):
    phrase_id: int


class SEOListingResponse(SEOListingBase):
    id: int
    phrase_id: int
    is_compliant: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SEOGenerateRequest(BaseModel):
    phrase: str
    niche: Optional[str] = None
    tone: Optional[str] = "neutral"  # neutral, funny, sarcastic, proud


class SEOFieldResponse(BaseModel):
    text: str
    length: int
    limit: int
    compliant: bool


class SEODescriptionFieldResponse(BaseModel):
    text: str
    length: int
    limit_min: int
    limit_max: int
    compliant: bool


class SEOKeywordsFieldResponse(BaseModel):
    text: str
    byte_count: int
    limit: int
    compliant: bool


class SEOValidationResponse(BaseModel):
    is_compliant: bool
    issues: List[str] = []
    checks_passed: int
    total_checks: int


class SEOGenerateResponse(BaseModel):
    phrase: str
    niche: str
    style: str
    title: SEOFieldResponse
    brand: SEOFieldResponse
    bullet_1: SEOFieldResponse
    bullet_2: SEOFieldResponse
    description: SEODescriptionFieldResponse
    keywords: SEOKeywordsFieldResponse
    validation: SEOValidationResponse
    warnings: List[str] = []


# Scraping schemas
class ScrapeRequest(BaseModel):
    source_type: str  # reddit, google_trends, amazon, etc.
    target: Optional[str] = None  # subreddit name, search term, etc.
    limit: int = Field(default=100, le=500)


class ScrapeResponse(BaseModel):
    source: str
    status: str
    items_collected: int
    phrases_extracted: int
    started_at: datetime
    completed_at: Optional[datetime] = None


# Export schemas
class ExportRequest(BaseModel):
    format: str = "csv"  # csv, json
    filters: Optional[PhraseFilter] = None
    include_metrics: bool = True
    include_seo: bool = False


class ExportResponse(BaseModel):
    filename: str
    format: str
    record_count: int
    file_path: str


# Dashboard stats schemas
class DashboardStats(BaseModel):
    total_phrases: int
    safe_phrases: int
    trending_phrases: int  # trend_score > 50
    patterns_detected: int
    total_trademarks: int
    last_scrape: Optional[datetime] = None
    top_niches: List[dict] = []
    recent_trends: List[dict] = []


# Phrase variation schemas
class VariationRequest(BaseModel):
    phrase: str
    variation_type: str = "all"  # synonym, tone, structure, all
    count: int = Field(default=5, le=20)


class VariationResponse(BaseModel):
    original: str
    variations: List[dict]
    all_safe: bool

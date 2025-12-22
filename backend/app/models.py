"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text,
    ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .database import Base


class Source(Base):
    """Data source tracking table."""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(500))
    source_type = Column(String(50))  # reddit, google_trends, amazon, etsy, etc.
    last_scraped = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    phrases = relationship("Phrase", back_populates="source_rel")


class Phrase(Base):
    """Main phrase storage table."""
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    normalized_text = Column(String(500), nullable=False, index=True)
    niche = Column(String(100), index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    source_context = Column(Text)  # Original context where phrase was found

    # Timestamps
    first_seen = Column(DateTime, default=datetime.utcnow, index=True)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # Frequency tracking
    frequency = Column(Integer, default=1)
    daily_frequency = Column(Integer, default=1)

    # Scoring
    trend_score = Column(Float, default=0.0, index=True)
    risk_score = Column(Float, default=0.0)
    is_safe = Column(Boolean, default=True, index=True)

    # Metadata
    word_count = Column(Integer)
    is_pattern = Column(Boolean, default=False)
    pattern_template = Column(String(500))  # e.g., "I'm not ___, I'm ___"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_rel = relationship("Source", back_populates="phrases")
    metrics = relationship("PhraseMetrics", back_populates="phrase", uselist=False)
    history = relationship("PhraseHistory", back_populates="phrase")
    seo_listings = relationship("SEOListing", back_populates="phrase")

    __table_args__ = (
        Index("idx_phrase_safe_score", "is_safe", "trend_score"),
        UniqueConstraint("normalized_text", "source_id", name="uq_phrase_source"),
    )


class PhraseMetrics(Base):
    """Detailed metrics for phrase scoring."""
    __tablename__ = "phrase_metrics"

    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("phrases.id"), unique=True)

    # Velocity - growth rate
    velocity = Column(Float, default=0.0)
    velocity_7d = Column(Float, default=0.0)  # 7-day velocity
    velocity_30d = Column(Float, default=0.0)  # 30-day velocity

    # Novelty - how new/unique
    novelty_score = Column(Float, default=0.0)

    # Saturation - market saturation
    saturation_score = Column(Float, default=0.0)
    amazon_results = Column(Integer, default=0)
    etsy_results = Column(Integer, default=0)

    # Cross-platform presence
    cross_platform_score = Column(Float, default=0.0)
    platforms_found = Column(String(500))  # JSON list of platforms

    # Length suitability for merch
    length_score = Column(Float, default=0.0)

    # Engagement metrics
    total_engagement = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    phrase = relationship("Phrase", back_populates="metrics")


class PhraseHistory(Base):
    """Historical tracking for phrase metrics over time."""
    __tablename__ = "phrase_history"

    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("phrases.id"))
    date = Column(DateTime, default=datetime.utcnow, index=True)

    frequency = Column(Integer, default=0)
    trend_score = Column(Float, default=0.0)
    velocity = Column(Float, default=0.0)

    # Relationships
    phrase = relationship("Phrase", back_populates="history")

    __table_args__ = (
        Index("idx_history_phrase_date", "phrase_id", "date"),
    )


class Trademark(Base):
    """Trademark database for safety checking."""
    __tablename__ = "trademarks"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(500), nullable=False)
    normalized_term = Column(String(500), nullable=False, index=True)
    source = Column(String(100))  # USPTO, manual, etc.
    registration_number = Column(String(50))
    status = Column(String(50))  # LIVE, DEAD, etc.
    goods_services = Column(Text)  # Description of goods/services
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_trademark_normalized", "normalized_term"),
    )


class BlockedTerm(Base):
    """Manually blocked terms and brand names."""
    __tablename__ = "blocked_terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(500), nullable=False)
    normalized_term = Column(String(500), nullable=False, index=True)
    reason = Column(String(200))  # trademark, brand, offensive, etc.
    created_at = Column(DateTime, default=datetime.utcnow)


class Pattern(Base):
    """Reusable phrase patterns/frameworks."""
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    template = Column(String(500), nullable=False, unique=True)
    # e.g., "I'm not {NOUN}, I'm {NOUN}"
    description = Column(Text)
    example_phrases = Column(Text)  # JSON list of example phrases
    variable_count = Column(Integer, default=1)
    popularity_score = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SEOListing(Base):
    """Generated SEO listings for Amazon Merch."""
    __tablename__ = "seo_listings"

    id = Column(Integer, primary_key=True, index=True)
    phrase_id = Column(Integer, ForeignKey("phrases.id"))

    title = Column(String(500), nullable=False)
    bullet_1 = Column(String(500))
    bullet_2 = Column(String(500))
    description = Column(Text)
    backend_keywords = Column(String(500))

    is_compliant = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    phrase = relationship("Phrase", back_populates="seo_listings")


class ScrapingLog(Base):
    """Log of scraping activities."""
    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(100))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    status = Column(String(50))  # running, completed, failed
    items_collected = Column(Integer, default=0)
    phrases_extracted = Column(Integer, default=0)
    error_message = Column(Text)

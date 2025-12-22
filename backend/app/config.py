"""Application configuration settings."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Merch Trend Intelligence Engine"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./data/merch_trends.db"

    # Reddit API (free tier)
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "MerchTrendEngine/1.0"

    # Scraping settings
    SCRAPE_DELAY_SECONDS: int = 2
    MAX_PAGES_PER_SOURCE: int = 10

    # NLP settings
    SPACY_MODEL: str = "en_core_web_sm"
    MIN_PHRASE_LENGTH: int = 2
    MAX_PHRASE_LENGTH: int = 6

    # Trend scoring weights
    WEIGHT_VELOCITY: float = 0.30
    WEIGHT_NOVELTY: float = 0.25
    WEIGHT_SATURATION: float = 0.25
    WEIGHT_CROSS_PLATFORM: float = 0.10
    WEIGHT_LENGTH: float = 0.10

    # Trademark safety
    FUZZY_MATCH_THRESHOLD: int = 85

    # Paths
    DATA_DIR: Path = Path("./data")
    RAW_DATA_DIR: Path = Path("./data/raw")
    PROCESSED_DATA_DIR: Path = Path("./data/processed")
    TRADEMARKS_DIR: Path = Path("./data/trademarks")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Create data directories if they don't exist
for dir_path in [settings.DATA_DIR, settings.RAW_DATA_DIR,
                 settings.PROCESSED_DATA_DIR, settings.TRADEMARKS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

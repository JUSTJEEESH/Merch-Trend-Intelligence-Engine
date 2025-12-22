"""Base scraper class."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
import logging

from ...config import settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self):
        self.delay = settings.SCRAPE_DELAY_SECONDS
        self.max_pages = settings.MAX_PAGES_PER_SOURCE

    @abstractmethod
    async def scrape(self, **kwargs) -> List[Dict[str, Any]]:
        """Scrape data from the source."""
        pass

    async def rate_limit(self):
        """Apply rate limiting between requests."""
        await asyncio.sleep(self.delay)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters but keep basic punctuation
        import re
        text = re.sub(r'[^\w\s\'\"\!\?\.\,\-]', '', text)
        return text.strip()

    def extract_context(self, item: Dict[str, Any]) -> str:
        """Extract context information from scraped item."""
        context_parts = []
        for key in ['subreddit', 'category', 'source', 'url']:
            if key in item and item[key]:
                context_parts.append(f"{key}:{item[key]}")
        return "; ".join(context_parts)

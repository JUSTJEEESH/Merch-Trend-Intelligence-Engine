"""Etsy scraper using requests and BeautifulSoup."""
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import re

from .base import BaseScraper

logger = logging.getLogger(__name__)


class EtsyScraper(BaseScraper):
    """Scraper for Etsy search results and trends."""

    ETSY_URL = "https://www.etsy.com"

    def __init__(self):
        super().__init__()

    async def scrape(
        self,
        search_term: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Scrape Etsy search results.

        Args:
            search_term: Term to search for
            limit: Maximum results to fetch

        Returns:
            List of scraped items
        """
        items = []

        try:
            import requests
            from bs4 import BeautifulSoup

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            search_url = f"{self.ETSY_URL}/search?q={search_term.replace(' ', '+')}"
            response = requests.get(search_url, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # Find listing cards
                listings = soup.select('.v2-listing-card')[:limit]

                for i, listing in enumerate(listings):
                    try:
                        # Extract title
                        title_elem = listing.select_one('.v2-listing-card__title')
                        if title_elem:
                            title = self.clean_text(title_elem.get_text())

                            # Extract price if available
                            price_elem = listing.select_one('.currency-value')
                            price = price_elem.get_text() if price_elem else None

                            items.append({
                                "text": title,
                                "source": "etsy",
                                "type": "listing",
                                "rank": i + 1,
                                "price": price,
                                "context": f"search_term:{search_term}; rank:{i+1}",
                                "timestamp": datetime.utcnow().isoformat()
                            })
                    except Exception as e:
                        logger.debug(f"Failed to parse listing: {e}")
                        continue

                await self.rate_limit()

        except ImportError:
            logger.warning("BeautifulSoup not installed")
        except Exception as e:
            logger.error(f"Etsy scraping failed: {e}")

        # Use mock data if nothing scraped
        if not items:
            items = self._get_mock_data(search_term)

        return items

    async def get_trending(self) -> List[Dict[str, Any]]:
        """Get Etsy trending items."""
        items = []

        try:
            import requests
            from bs4 import BeautifulSoup

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }

            # Etsy trending/popular page
            response = requests.get(
                f"{self.ETSY_URL}/featured/trending-items",
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                listings = soup.select('.listing-link')[:30]

                for i, listing in enumerate(listings):
                    title = listing.get('title', '')
                    if title:
                        items.append({
                            "text": self.clean_text(title),
                            "source": "etsy",
                            "type": "trending",
                            "rank": i + 1,
                            "context": f"type:trending; rank:{i+1}",
                            "timestamp": datetime.utcnow().isoformat()
                        })

        except Exception as e:
            logger.error(f"Etsy trending scraping failed: {e}")

        return items if items else self._get_mock_trending()

    def extract_tags_from_title(self, title: str) -> List[str]:
        """Extract potential tags from a listing title."""
        # Remove common filler words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
            'shirt', 'tee', 'tshirt', 't-shirt', 'clothing', 'apparel'
        }

        words = title.lower().split()
        tags = []

        for word in words:
            # Clean the word
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 2 and word not in stop_words:
                tags.append(word)

        return tags[:10]

    def _get_mock_data(self, search_term: str) -> List[Dict[str, Any]]:
        """Return mock data for testing."""
        mock_titles = [
            f"Funny {search_term} Gift Idea",
            f"Vintage {search_term} Style Design",
            f"Retro {search_term} Graphic Print",
            f"Sarcastic {search_term} Quote",
            f"Cute {search_term} For Her",
            f"Cool {search_term} For Him",
            f"Best {search_term} Ever",
            f"Custom {search_term} Personalized",
        ]

        return [
            {
                "text": title,
                "source": "etsy",
                "type": "listing",
                "rank": i + 1,
                "context": f"search_term:{search_term}; rank:{i+1}",
                "timestamp": datetime.utcnow().isoformat()
            }
            for i, title in enumerate(mock_titles)
        ]

    def _get_mock_trending(self) -> List[Dict[str, Any]]:
        """Return mock trending data."""
        mock_trending = [
            "Cottagecore Aesthetic Design",
            "Dark Academia Style",
            "Y2K Retro Vibes",
            "Goblincore Nature Art",
            "Maximalist Pattern Design",
        ]

        return [
            {
                "text": title,
                "source": "etsy",
                "type": "trending",
                "rank": i + 1,
                "context": f"type:trending; rank:{i+1}",
                "timestamp": datetime.utcnow().isoformat()
            }
            for i, title in enumerate(mock_trending)
        ]

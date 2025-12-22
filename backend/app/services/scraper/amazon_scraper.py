"""Amazon search scraper using Playwright."""
from typing import List, Dict, Any, Optional
import logging
import asyncio
from datetime import datetime

from .base import BaseScraper

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    """Scraper for Amazon search suggestions and results."""

    AMAZON_URL = "https://www.amazon.com"
    AUTOCOMPLETE_URL = "https://completion.amazon.com/api/2017/suggestions"

    def __init__(self):
        super().__init__()
        self.browser = None

    async def _init_browser(self):
        """Initialize Playwright browser."""
        try:
            from playwright.async_api import async_playwright
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            logger.info("Playwright browser initialized")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")

    async def scrape(
        self,
        search_term: str,
        limit: int = 50,
        category: str = "fashion"
    ) -> List[Dict[str, Any]]:
        """
        Scrape Amazon search suggestions and results.

        Args:
            search_term: Term to search for
            limit: Maximum results to fetch
            category: Product category

        Returns:
            List of scraped items
        """
        items = []

        # Get autocomplete suggestions
        suggestions = await self._get_autocomplete(search_term)
        items.extend(suggestions)

        # Get search results (if browser available)
        if self.browser is None:
            await self._init_browser()

        if self.browser:
            try:
                results = await self._scrape_search_results(search_term, limit)
                items.extend(results)
            except Exception as e:
                logger.error(f"Failed to scrape search results: {e}")

        # Use mock data if nothing scraped
        if not items:
            items = self._get_mock_data(search_term)

        return items

    async def _get_autocomplete(self, search_term: str) -> List[Dict[str, Any]]:
        """Get Amazon autocomplete suggestions."""
        items = []

        try:
            import requests

            params = {
                "mid": "ATVPDKIKX0DER",
                "alias": "aps",
                "prefix": search_term,
                "event": "onKeyPress",
                "limit": 10,
                "fb": 1,
                "suggestion-type": "KEYWORD"
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(
                self.AUTOCOMPLETE_URL,
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                suggestions = data.get("suggestions", [])

                for suggestion in suggestions:
                    value = suggestion.get("value", "")
                    if value:
                        items.append({
                            "text": self.clean_text(value),
                            "source": "amazon",
                            "type": "autocomplete",
                            "context": f"search_term:{search_term}",
                            "timestamp": datetime.utcnow().isoformat()
                        })

        except Exception as e:
            logger.error(f"Autocomplete fetch failed: {e}")

        await self.rate_limit()
        return items

    async def _scrape_search_results(
        self,
        search_term: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Scrape Amazon search results page."""
        items = []

        try:
            page = await self.browser.new_page()
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            search_url = f"{self.AMAZON_URL}/s?k={search_term.replace(' ', '+')}&i=fashion"
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

            await asyncio.sleep(2)  # Wait for dynamic content

            # Extract product titles
            titles = await page.query_selector_all('[data-component-type="s-search-result"] h2 span')

            for i, title_elem in enumerate(titles[:limit]):
                try:
                    title_text = await title_elem.inner_text()
                    if title_text:
                        items.append({
                            "text": self.clean_text(title_text),
                            "source": "amazon",
                            "type": "search_result",
                            "rank": i + 1,
                            "context": f"search_term:{search_term}; rank:{i+1}",
                            "timestamp": datetime.utcnow().isoformat()
                        })
                except Exception:
                    continue

            await page.close()

        except Exception as e:
            logger.error(f"Search results scraping failed: {e}")

        return items

    async def get_bestsellers(self, category: str = "fashion") -> List[Dict[str, Any]]:
        """Scrape Amazon bestsellers in a category."""
        items = []

        if self.browser is None:
            await self._init_browser()

        if not self.browser:
            return self._get_mock_bestsellers()

        try:
            page = await self.browser.new_page()
            bestseller_url = f"{self.AMAZON_URL}/Best-Sellers-Clothing/zgbs/fashion"
            await page.goto(bestseller_url, wait_until="domcontentloaded", timeout=30000)

            await asyncio.sleep(2)

            titles = await page.query_selector_all('.zg-item-immersion .p13n-sc-truncate')

            for i, title_elem in enumerate(titles[:50]):
                try:
                    title_text = await title_elem.inner_text()
                    if title_text:
                        items.append({
                            "text": self.clean_text(title_text),
                            "source": "amazon",
                            "type": "bestseller",
                            "rank": i + 1,
                            "category": category,
                            "context": f"type:bestseller; category:{category}; rank:{i+1}",
                            "timestamp": datetime.utcnow().isoformat()
                        })
                except Exception:
                    continue

            await page.close()

        except Exception as e:
            logger.error(f"Bestsellers scraping failed: {e}")

        return items if items else self._get_mock_bestsellers()

    def _get_mock_data(self, search_term: str) -> List[Dict[str, Any]]:
        """Return mock data for testing."""
        mock_suggestions = [
            f"{search_term} funny",
            f"{search_term} for men",
            f"{search_term} for women",
            f"{search_term} vintage",
            f"{search_term} retro",
            f"best {search_term}",
            f"cool {search_term}",
            f"cute {search_term}",
        ]

        return [
            {
                "text": suggestion,
                "source": "amazon",
                "type": "autocomplete",
                "context": f"search_term:{search_term}",
                "timestamp": datetime.utcnow().isoformat()
            }
            for suggestion in mock_suggestions
        ]

    def _get_mock_bestsellers(self) -> List[Dict[str, Any]]:
        """Return mock bestseller data."""
        mock_titles = [
            "Funny Vintage Graphic Tee",
            "Retro 80s Style Design",
            "Sarcastic Quote For Adults",
            "Dad Joke Loading Please Wait",
            "Mom Life Best Life",
        ]

        return [
            {
                "text": title,
                "source": "amazon",
                "type": "bestseller",
                "rank": i + 1,
                "context": f"type:bestseller; rank:{i+1}",
                "timestamp": datetime.utcnow().isoformat()
            }
            for i, title in enumerate(mock_titles)
        ]

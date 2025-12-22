"""Google Trends scraper using pytrends."""
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from .base import BaseScraper

logger = logging.getLogger(__name__)


class GoogleTrendsScraper(BaseScraper):
    """Scraper for Google Trends data."""

    # Categories relevant to merch
    MERCH_CATEGORIES = {
        "general": 0,
        "arts_entertainment": 3,
        "games": 8,
        "hobbies": 64,
        "sports": 20,
        "shopping": 18,
    }

    def __init__(self):
        super().__init__()
        self.pytrends = None
        self._init_pytrends()

    def _init_pytrends(self):
        """Initialize pytrends client."""
        try:
            from pytrends.request import TrendReq
            self.pytrends = TrendReq(hl='en-US', tz=360)
            logger.info("pytrends client initialized")
        except ImportError:
            logger.warning("pytrends not installed")
        except Exception as e:
            logger.error(f"Failed to initialize pytrends: {e}")

    async def scrape(
        self,
        keyword: Optional[str] = None,
        geo: str = "US",
        timeframe: str = "today 1-m"
    ) -> List[Dict[str, Any]]:
        """
        Scrape Google Trends data.

        Args:
            keyword: Specific keyword to get related queries for
            geo: Geographic location (default US)
            timeframe: Time range (today 1-m, today 3-m, today 12-m)

        Returns:
            List of trending terms with metadata
        """
        items = []

        if not self.pytrends:
            logger.warning("pytrends not available, using mock data")
            return self._get_mock_data()

        try:
            # Get trending searches (daily)
            trending = self.pytrends.trending_searches(pn='united_states')
            for term in trending[0].tolist()[:20]:
                items.append({
                    "text": self.clean_text(term),
                    "source": "google_trends",
                    "trend_type": "daily_trending",
                    "context": "type:daily_trending; geo:US",
                    "timestamp": datetime.utcnow().isoformat()
                })

            await self.rate_limit()

            # Get related queries if keyword provided
            if keyword:
                self.pytrends.build_payload([keyword], geo=geo, timeframe=timeframe)

                related = self.pytrends.related_queries()
                if keyword in related:
                    # Rising queries
                    rising = related[keyword].get('rising')
                    if rising is not None and not rising.empty:
                        for _, row in rising.head(15).iterrows():
                            items.append({
                                "text": self.clean_text(row['query']),
                                "source": "google_trends",
                                "trend_type": "rising",
                                "value": row.get('value', 0),
                                "context": f"type:rising; keyword:{keyword}",
                                "timestamp": datetime.utcnow().isoformat()
                            })

                    # Top queries
                    top = related[keyword].get('top')
                    if top is not None and not top.empty:
                        for _, row in top.head(15).iterrows():
                            items.append({
                                "text": self.clean_text(row['query']),
                                "source": "google_trends",
                                "trend_type": "top",
                                "value": row.get('value', 0),
                                "context": f"type:top; keyword:{keyword}",
                                "timestamp": datetime.utcnow().isoformat()
                            })

                await self.rate_limit()

                # Get related topics
                topics = self.pytrends.related_topics()
                if keyword in topics:
                    rising_topics = topics[keyword].get('rising')
                    if rising_topics is not None and not rising_topics.empty:
                        for _, row in rising_topics.head(10).iterrows():
                            title = row.get('topic_title', '')
                            if title:
                                items.append({
                                    "text": self.clean_text(title),
                                    "source": "google_trends",
                                    "trend_type": "rising_topic",
                                    "context": f"type:rising_topic; keyword:{keyword}",
                                    "timestamp": datetime.utcnow().isoformat()
                                })

        except Exception as e:
            logger.error(f"Google Trends scraping failed: {e}")

        return items

    async def get_interest_over_time(
        self,
        keywords: List[str],
        timeframe: str = "today 3-m"
    ) -> Dict[str, Any]:
        """Get interest over time for keywords."""
        if not self.pytrends:
            return {}

        try:
            self.pytrends.build_payload(keywords[:5], timeframe=timeframe)
            interest = self.pytrends.interest_over_time()

            if interest.empty:
                return {}

            return {
                "keywords": keywords,
                "data": interest.to_dict(),
                "timeframe": timeframe
            }
        except Exception as e:
            logger.error(f"Failed to get interest over time: {e}")
            return {}

    def _get_mock_data(self) -> List[Dict[str, Any]]:
        """Return mock data for testing."""
        mock_trends = [
            {"text": "quiet quitting", "type": "rising"},
            {"text": "girl dinner", "type": "rising"},
            {"text": "roman empire", "type": "rising"},
            {"text": "hot girl walk", "type": "rising"},
            {"text": "soft life", "type": "rising"},
            {"text": "de-influencing", "type": "rising"},
            {"text": "coastal grandmother", "type": "top"},
            {"text": "clean girl aesthetic", "type": "top"},
            {"text": "that girl", "type": "top"},
            {"text": "main character energy", "type": "top"},
        ]

        return [
            {
                "text": trend["text"],
                "source": "google_trends",
                "trend_type": trend["type"],
                "value": 100 if trend["type"] == "rising" else 75,
                "context": f"type:{trend['type']}; source:mock",
                "timestamp": datetime.utcnow().isoformat()
            }
            for trend in mock_trends
        ]

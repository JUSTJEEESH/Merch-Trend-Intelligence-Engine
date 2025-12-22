"""Reddit scraper using PRAW (Python Reddit API Wrapper)."""
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from .base import BaseScraper
from ...config import settings

logger = logging.getLogger(__name__)


class RedditScraper(BaseScraper):
    """Scraper for Reddit content using the free API tier."""

    # Popular subreddits for merch trends
    DEFAULT_SUBREDDITS = [
        "memes", "funny", "tshirts", "entrepreneur",
        "daddit", "nursing", "teachers", "gaming",
        "fishing", "hiking", "dogs", "cats",
        "fitness", "programming", "coffee"
    ]

    def __init__(self):
        super().__init__()
        self.reddit = None
        self._init_reddit()

    def _init_reddit(self):
        """Initialize Reddit API client."""
        try:
            import praw
            if settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET:
                self.reddit = praw.Reddit(
                    client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_CLIENT_SECRET,
                    user_agent=settings.REDDIT_USER_AGENT
                )
                logger.info("Reddit API client initialized")
            else:
                logger.warning("Reddit API credentials not configured")
        except ImportError:
            logger.warning("PRAW not installed")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {e}")

    async def scrape(
        self,
        subreddit: Optional[str] = None,
        limit: int = 100,
        time_filter: str = "week"
    ) -> List[Dict[str, Any]]:
        """
        Scrape Reddit posts and comments.

        Args:
            subreddit: Specific subreddit to scrape (or None for defaults)
            limit: Maximum posts to fetch
            time_filter: Time filter for top posts (hour, day, week, month, year, all)

        Returns:
            List of scraped items with text and metadata
        """
        items = []

        if not self.reddit:
            logger.warning("Reddit client not available, using mock data")
            return self._get_mock_data()

        try:
            subreddits = [subreddit] if subreddit else self.DEFAULT_SUBREDDITS[:5]

            for sub_name in subreddits:
                try:
                    sub = self.reddit.subreddit(sub_name)
                    posts_per_sub = limit // len(subreddits)

                    # Get hot posts
                    for post in sub.hot(limit=posts_per_sub // 2):
                        items.append(self._process_post(post, sub_name))
                        await self.rate_limit()

                    # Get top posts
                    for post in sub.top(time_filter=time_filter, limit=posts_per_sub // 2):
                        items.append(self._process_post(post, sub_name))
                        await self.rate_limit()

                except Exception as e:
                    logger.error(f"Error scraping r/{sub_name}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Reddit scraping failed: {e}")

        return items

    def _process_post(self, post, subreddit: str) -> Dict[str, Any]:
        """Process a Reddit post into structured data."""
        return {
            "text": self.clean_text(post.title),
            "body": self.clean_text(post.selftext) if hasattr(post, 'selftext') else "",
            "source": "reddit",
            "subreddit": subreddit,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
            "url": f"https://reddit.com{post.permalink}",
            "context": f"subreddit:r/{subreddit}; score:{post.score}"
        }

    def _get_mock_data(self) -> List[Dict[str, Any]]:
        """Return mock data for testing without API credentials."""
        mock_posts = [
            {"text": "I'm not lazy I'm on energy saving mode", "subreddit": "funny", "score": 15000},
            {"text": "Tell me you're a programmer without telling me you're a programmer", "subreddit": "programming", "score": 8000},
            {"text": "Powered by coffee and anxiety", "subreddit": "coffee", "score": 5000},
            {"text": "I used to be cool now I'm just cold", "subreddit": "daddit", "score": 3000},
            {"text": "Weekend forecast fishing with a chance of drinking", "subreddit": "fishing", "score": 4500},
            {"text": "Dog mom life is the best life", "subreddit": "dogs", "score": 7000},
            {"text": "Cat dad loading please wait", "subreddit": "cats", "score": 6000},
            {"text": "Nurses we cant fix stupid but we can sedate it", "subreddit": "nursing", "score": 12000},
            {"text": "Teacher mode activated coffee required", "subreddit": "teachers", "score": 5500},
            {"text": "I dont sweat I sparkle", "subreddit": "fitness", "score": 4000},
        ]

        return [
            {
                "text": post["text"],
                "body": "",
                "source": "reddit",
                "subreddit": post["subreddit"],
                "score": post["score"],
                "num_comments": 100,
                "created_utc": datetime.utcnow().isoformat(),
                "url": f"https://reddit.com/r/{post['subreddit']}",
                "context": f"subreddit:r/{post['subreddit']}; score:{post['score']}"
            }
            for post in mock_posts
        ]

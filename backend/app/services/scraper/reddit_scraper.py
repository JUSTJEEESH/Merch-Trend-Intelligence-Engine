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
            # Only initialize if real credentials are provided (not placeholder values)
            if (settings.REDDIT_CLIENT_ID and
                settings.REDDIT_CLIENT_SECRET and
                settings.REDDIT_CLIENT_ID != "your_client_id" and
                settings.REDDIT_CLIENT_SECRET != "your_client_secret" and
                len(settings.REDDIT_CLIENT_ID) > 10):
                self.reddit = praw.Reddit(
                    client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_CLIENT_SECRET,
                    user_agent=settings.REDDIT_USER_AGENT
                )
                logger.info("Reddit API client initialized")
            else:
                logger.info("Reddit API credentials not configured - using sample data")
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
        """Return sample trending phrases for demonstration."""
        mock_posts = [
            # Funny/General
            {"text": "I'm not lazy I'm on energy saving mode", "subreddit": "funny", "score": 15000},
            {"text": "I'm not arguing I'm explaining why I'm right", "subreddit": "funny", "score": 12000},
            {"text": "My patience is like my phone battery always low", "subreddit": "funny", "score": 9000},
            {"text": "I'm not short I'm concentrated awesome", "subreddit": "funny", "score": 8500},
            {"text": "Sarcasm is my love language", "subreddit": "funny", "score": 11000},
            {"text": "I put the pro in procrastination", "subreddit": "funny", "score": 7500},

            # Programming/Tech
            {"text": "Tell me you're a programmer without telling me you're a programmer", "subreddit": "programming", "score": 8000},
            {"text": "It works on my machine", "subreddit": "programming", "score": 14000},
            {"text": "I turn coffee into code", "subreddit": "programming", "score": 6500},
            {"text": "There's no place like 127.0.0.1", "subreddit": "programming", "score": 7200},

            # Coffee
            {"text": "Powered by coffee and anxiety", "subreddit": "coffee", "score": 5000},
            {"text": "But first coffee", "subreddit": "coffee", "score": 9500},
            {"text": "Coffee is my spirit animal", "subreddit": "coffee", "score": 4800},
            {"text": "Decaf is not an option", "subreddit": "coffee", "score": 3900},

            # Parenting
            {"text": "I used to be cool now I'm just cold", "subreddit": "daddit", "score": 3000},
            {"text": "Dad joke loading please wait", "subreddit": "daddit", "score": 8700},
            {"text": "Best dad ever just ask my kids", "subreddit": "daddit", "score": 5600},
            {"text": "Mom life is the best life", "subreddit": "moms", "score": 7800},
            {"text": "Mama needs coffee", "subreddit": "moms", "score": 6200},
            {"text": "Surviving motherhood one coffee at a time", "subreddit": "moms", "score": 5400},

            # Fishing
            {"text": "Weekend forecast fishing with a chance of drinking", "subreddit": "fishing", "score": 4500},
            {"text": "I'd rather be fishing", "subreddit": "fishing", "score": 6100},
            {"text": "Reel cool dad", "subreddit": "fishing", "score": 3800},
            {"text": "Born to fish forced to work", "subreddit": "fishing", "score": 5200},

            # Dogs
            {"text": "Dog mom life is the best life", "subreddit": "dogs", "score": 7000},
            {"text": "My dog is my valentine", "subreddit": "dogs", "score": 8900},
            {"text": "All I need is coffee and my dog", "subreddit": "dogs", "score": 6700},
            {"text": "Home is where my dog is", "subreddit": "dogs", "score": 5100},

            # Cats
            {"text": "Cat dad loading please wait", "subreddit": "cats", "score": 6000},
            {"text": "Crazy cat lady in training", "subreddit": "cats", "score": 7400},
            {"text": "My cat is judging you", "subreddit": "cats", "score": 5800},

            # Nursing
            {"text": "Nurses we cant fix stupid but we can sedate it", "subreddit": "nursing", "score": 12000},
            {"text": "Nurses call the shots", "subreddit": "nursing", "score": 6900},
            {"text": "Night shift nurse running on coffee and dry shampoo", "subreddit": "nursing", "score": 5300},
            {"text": "Saving lives one shift at a time", "subreddit": "nursing", "score": 4700},

            # Teachers
            {"text": "Teacher mode activated coffee required", "subreddit": "teachers", "score": 5500},
            {"text": "Teaching is a work of heart", "subreddit": "teachers", "score": 6300},
            {"text": "I teach whats your superpower", "subreddit": "teachers", "score": 8100},
            {"text": "Summer is my favorite subject", "subreddit": "teachers", "score": 4200},

            # Fitness
            {"text": "I dont sweat I sparkle", "subreddit": "fitness", "score": 4000},
            {"text": "Gym hair dont care", "subreddit": "fitness", "score": 5900},
            {"text": "Muscles are my cardio", "subreddit": "fitness", "score": 3500},
            {"text": "Lift heavy pet dogs", "subreddit": "fitness", "score": 6800},

            # Gaming
            {"text": "Level up in progress", "subreddit": "gaming", "score": 7600},
            {"text": "I paused my game to be here", "subreddit": "gaming", "score": 9200},
            {"text": "Eat sleep game repeat", "subreddit": "gaming", "score": 8400},
            {"text": "Insert coffee to continue", "subreddit": "gaming", "score": 5700},

            # Outdoors/Hiking
            {"text": "The mountains are calling and I must go", "subreddit": "hiking", "score": 11500},
            {"text": "Hiking is my therapy", "subreddit": "hiking", "score": 6400},
            {"text": "Take only pictures leave only footprints", "subreddit": "hiking", "score": 4900},
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

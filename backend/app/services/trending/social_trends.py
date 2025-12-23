"""Social media trending topics service for merch research."""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)


class SocialTrendsService:
    """
    Service for fetching and analyzing trending topics from social platforms.
    Converts viral trends into merch-friendly phrases.
    """

    # TikTok-style viral trends (these would come from API/scraping in production)
    TIKTOK_TRENDS = [
        # Current viral sounds/memes
        {"trend": "Very demure very mindful", "hashtag": "#demure", "views": "2.1B", "growth": "+890%", "category": "lifestyle"},
        {"trend": "Delulu is the solulu", "hashtag": "#delulu", "views": "1.8B", "growth": "+520%", "category": "humor"},
        {"trend": "Girl math", "hashtag": "#girlmath", "views": "1.5B", "growth": "+380%", "category": "humor"},
        {"trend": "Boy math", "hashtag": "#boymath", "views": "980M", "growth": "+320%", "category": "humor"},
        {"trend": "Roman Empire", "hashtag": "#romanempire", "views": "1.2B", "growth": "+275%", "category": "humor"},
        {"trend": "Brat summer", "hashtag": "#bratsummer", "views": "2.5B", "growth": "+650%", "category": "lifestyle"},
        {"trend": "Midwest princess", "hashtag": "#midwestprincess", "views": "450M", "growth": "+185%", "category": "aesthetic"},
        {"trend": "Clean girl aesthetic", "hashtag": "#cleangirl", "views": "3.2B", "growth": "+120%", "category": "aesthetic"},
        {"trend": "Mob wife aesthetic", "hashtag": "#mobwife", "views": "890M", "growth": "+340%", "category": "aesthetic"},
        {"trend": "Quiet luxury", "hashtag": "#quietluxury", "views": "1.1B", "growth": "+195%", "category": "fashion"},
        {"trend": "Cozy cardio", "hashtag": "#cozycardio", "views": "670M", "growth": "+225%", "category": "fitness"},
        {"trend": "Hot girl walk", "hashtag": "#hotgirlwalk", "views": "2.8B", "growth": "+85%", "category": "fitness"},
        {"trend": "Bed rotting", "hashtag": "#bedrotting", "views": "520M", "growth": "+290%", "category": "lifestyle"},
        {"trend": "Feral girl summer", "hashtag": "#feralgirl", "views": "380M", "growth": "+175%", "category": "lifestyle"},
        {"trend": "Soft life", "hashtag": "#softlife", "views": "1.4B", "growth": "+145%", "category": "lifestyle"},
        {"trend": "Lucky girl syndrome", "hashtag": "#luckygirl", "views": "920M", "growth": "+210%", "category": "mindset"},
        {"trend": "Main character energy", "hashtag": "#maincharacter", "views": "4.1B", "growth": "+95%", "category": "mindset"},
        {"trend": "That girl", "hashtag": "#thatgirl", "views": "5.2B", "growth": "+65%", "category": "lifestyle"},
        {"trend": "NPC streaming", "hashtag": "#npc", "views": "1.6B", "growth": "+420%", "category": "humor"},
        {"trend": "Rizz", "hashtag": "#rizz", "views": "6.8B", "growth": "+55%", "category": "slang"},
        {"trend": "Skibidi", "hashtag": "#skibidi", "views": "3.5B", "growth": "+180%", "category": "humor"},
        {"trend": "GRWM", "hashtag": "#grwm", "views": "12B", "growth": "+45%", "category": "lifestyle"},
        {"trend": "Deinfluencing", "hashtag": "#deinfluencing", "views": "780M", "growth": "+165%", "category": "lifestyle"},
        {"trend": "Underconsumption core", "hashtag": "#underconsumption", "views": "340M", "growth": "+385%", "category": "lifestyle"},
        {"trend": "Coquette", "hashtag": "#coquette", "views": "2.1B", "growth": "+135%", "category": "aesthetic"},
    ]

    # Twitter/X trending topics
    TWITTER_TRENDS = [
        {"trend": "Quiet quitting", "tweets": "2.4M", "growth": "+195%", "category": "work"},
        {"trend": "Act your wage", "tweets": "1.8M", "growth": "+420%", "category": "work"},
        {"trend": "Bare minimum Monday", "tweets": "890K", "growth": "+285%", "category": "work"},
        {"trend": "Lazy girl job", "tweets": "1.2M", "growth": "+310%", "category": "work"},
        {"trend": "Boysober", "tweets": "450K", "growth": "+520%", "category": "lifestyle"},
        {"trend": "Situationship", "tweets": "3.1M", "growth": "+125%", "category": "relationships"},
        {"trend": "Beige flag", "tweets": "680K", "growth": "+245%", "category": "relationships"},
        {"trend": "Ick", "tweets": "2.8M", "growth": "+95%", "category": "relationships"},
        {"trend": "Touch grass", "tweets": "4.2M", "growth": "+75%", "category": "humor"},
        {"trend": "Chronically online", "tweets": "1.9M", "growth": "+165%", "category": "humor"},
        {"trend": "Unalive", "tweets": "980K", "growth": "+85%", "category": "internet"},
        {"trend": "Pick me", "tweets": "5.1M", "growth": "+55%", "category": "humor"},
        {"trend": "Slay", "tweets": "8.2M", "growth": "+35%", "category": "slang"},
        {"trend": "Era", "tweets": "6.5M", "growth": "+145%", "category": "slang"},
        {"trend": "Gaslight gatekeep girlboss", "tweets": "2.1M", "growth": "+45%", "category": "humor"},
        {"trend": "No thoughts head empty", "tweets": "1.4M", "growth": "+115%", "category": "humor"},
        {"trend": "Living my best life", "tweets": "3.8M", "growth": "+65%", "category": "lifestyle"},
        {"trend": "Hot take", "tweets": "4.5M", "growth": "+85%", "category": "internet"},
        {"trend": "Rent free", "tweets": "2.9M", "growth": "+95%", "category": "internet"},
        {"trend": "Understood the assignment", "tweets": "1.7M", "growth": "+135%", "category": "slang"},
    ]

    # Reddit rising trends
    REDDIT_TRENDS = [
        {"trend": "Weaponized incompetence", "subreddit": "r/relationships", "upvotes": "45K", "growth": "+210%"},
        {"trend": "The audacity", "subreddit": "r/ChoosingBeggars", "upvotes": "32K", "growth": "+175%"},
        {"trend": "Tell me without telling me", "subreddit": "r/AskReddit", "upvotes": "28K", "growth": "+145%"},
        {"trend": "Normalize this", "subreddit": "r/unpopularopinion", "upvotes": "18K", "growth": "+195%"},
        {"trend": "This is the way", "subreddit": "r/TheMandalorian", "upvotes": "52K", "growth": "+85%"},
        {"trend": "Thanks I hate it", "subreddit": "r/TIHI", "upvotes": "38K", "growth": "+125%"},
        {"trend": "Oddly specific", "subreddit": "r/oddlyspecific", "upvotes": "22K", "growth": "+165%"},
        {"trend": "Introverts unite separately", "subreddit": "r/introvert", "upvotes": "15K", "growth": "+185%"},
        {"trend": "Anxiety has entered the chat", "subreddit": "r/anxiety", "upvotes": "29K", "growth": "+155%"},
        {"trend": "Adulting is hard", "subreddit": "r/adulting", "upvotes": "41K", "growth": "+95%"},
    ]

    # Phrase templates for converting trends to merch
    PHRASE_TEMPLATES = {
        "era": [
            "In my {trend} era",
            "{trend} era activated",
            "Currently in my {trend} era",
            "Welcome to my {trend} era",
            "{trend} is my personality now",
        ],
        "core": [
            "{trend} core",
            "Certified {trend}",
            "{trend} enthusiast",
            "Professional {trend}",
            "{trend} but make it fashion",
        ],
        "mood": [
            "{trend} is a mood",
            "{trend} energy only",
            "Big {trend} energy",
            "Channeling {trend}",
            "{trend} vibes only",
        ],
        "identity": [
            "I'm a {trend} girlie",
            "{trend} girlie",
            "Just a {trend} girl",
            "Recovering {trend}",
            "Self-diagnosed {trend}",
        ],
        "humor": [
            "{trend} but unironically",
            "My therapist said no more {trend}",
            "{trend} is my toxic trait",
            "I didn't choose {trend}, {trend} chose me",
            "{trend} runs in my family",
        ],
    }

    def __init__(self):
        self.cache = {}
        self.cache_expiry = timedelta(hours=1)

    async def get_tiktok_trends(self, limit: int = 25) -> List[Dict[str, Any]]:
        """Get trending topics from TikTok."""
        trends = sorted(
            self.TIKTOK_TRENDS,
            key=lambda x: int(x["growth"].replace("+", "").replace("%", "")),
            reverse=True
        )[:limit]

        return [{
            **trend,
            "platform": "TikTok",
            "merch_phrases": self._generate_merch_phrases(trend["trend"]),
            "shirt_potential": self._calculate_shirt_potential(trend),
            "fetched_at": datetime.utcnow().isoformat(),
        } for trend in trends]

    async def get_twitter_trends(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get trending topics from Twitter/X."""
        trends = sorted(
            self.TWITTER_TRENDS,
            key=lambda x: int(x["growth"].replace("+", "").replace("%", "")),
            reverse=True
        )[:limit]

        return [{
            **trend,
            "platform": "Twitter",
            "merch_phrases": self._generate_merch_phrases(trend["trend"]),
            "shirt_potential": self._calculate_shirt_potential(trend),
            "fetched_at": datetime.utcnow().isoformat(),
        } for trend in trends]

    async def get_reddit_trends(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending topics from Reddit."""
        trends = sorted(
            self.REDDIT_TRENDS,
            key=lambda x: int(x["growth"].replace("+", "").replace("%", "")),
            reverse=True
        )[:limit]

        return [{
            **trend,
            "platform": "Reddit",
            "merch_phrases": self._generate_merch_phrases(trend["trend"]),
            "shirt_potential": self._calculate_shirt_potential(trend),
            "fetched_at": datetime.utcnow().isoformat(),
        } for trend in trends]

    async def get_all_trends(self, limit_per_platform: int = 15) -> Dict[str, List[Dict]]:
        """Get trends from all platforms."""
        tiktok, twitter, reddit = await asyncio.gather(
            self.get_tiktok_trends(limit_per_platform),
            self.get_twitter_trends(limit_per_platform),
            self.get_reddit_trends(limit_per_platform // 2),
        )

        return {
            "tiktok": tiktok,
            "twitter": twitter,
            "reddit": reddit,
            "combined": self._combine_and_rank(tiktok + twitter + reddit),
        }

    def _generate_merch_phrases(self, trend: str) -> List[str]:
        """Generate merch-ready phrases from a trend."""
        phrases = []
        trend_clean = trend.lower().strip()

        # Direct phrase
        phrases.append(trend)

        # Apply templates
        for template_type, templates in self.PHRASE_TEMPLATES.items():
            template = random.choice(templates)
            phrase = template.format(trend=trend_clean)
            phrases.append(phrase.title())

        # Add variations
        phrases.extend([
            f"{trend} mode",
            f"Professional {trend.lower()}",
            f"{trend} loading...",
            f"Warning: {trend}",
            f"Powered by {trend.lower()}",
        ])

        return phrases[:10]  # Limit to 10 suggestions

    def _calculate_shirt_potential(self, trend: Dict) -> Dict[str, Any]:
        """Calculate how well a trend translates to merch."""
        growth = int(trend.get("growth", "+0%").replace("+", "").replace("%", ""))

        # Scoring factors
        score = 50  # Base score

        # Growth rate bonus
        if growth > 400:
            score += 30
        elif growth > 200:
            score += 20
        elif growth > 100:
            score += 10

        # Length bonus (shorter = better for shirts)
        trend_text = trend.get("trend", "")
        if len(trend_text) < 20:
            score += 15
        elif len(trend_text) < 35:
            score += 5

        # Category bonus
        high_value_categories = ["humor", "lifestyle", "mindset", "work"]
        if trend.get("category", "").lower() in high_value_categories:
            score += 10

        return {
            "score": min(score, 100),
            "rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair",
            "factors": {
                "growth_momentum": "high" if growth > 200 else "medium" if growth > 100 else "low",
                "phrase_length": "optimal" if len(trend_text) < 25 else "acceptable",
                "category_fit": trend.get("category", "general"),
            }
        }

    def _combine_and_rank(self, all_trends: List[Dict]) -> List[Dict]:
        """Combine trends from all platforms and rank by potential."""
        # Sort by shirt potential score
        ranked = sorted(
            all_trends,
            key=lambda x: x.get("shirt_potential", {}).get("score", 0),
            reverse=True
        )
        return ranked[:30]  # Top 30 across all platforms

    async def get_trending_phrases_for_niche(self, niche: str) -> List[Dict[str, Any]]:
        """Get trending phrases filtered by niche."""
        all_trends = await self.get_all_trends()

        # Map niches to categories
        niche_category_map = {
            "fitness": ["fitness", "health"],
            "work": ["work", "career"],
            "relationships": ["relationships", "dating"],
            "humor": ["humor", "meme"],
            "lifestyle": ["lifestyle", "aesthetic"],
            "fashion": ["fashion", "aesthetic"],
            "mindset": ["mindset", "motivation"],
        }

        target_categories = niche_category_map.get(niche.lower(), [])

        if not target_categories:
            return all_trends["combined"][:15]

        filtered = [
            t for t in all_trends["combined"]
            if t.get("category", "").lower() in target_categories
        ]

        return filtered[:15] if filtered else all_trends["combined"][:10]


# Singleton instance
social_trends_service = SocialTrendsService()

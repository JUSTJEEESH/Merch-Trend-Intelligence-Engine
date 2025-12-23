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

    NOTE: In production, this would connect to real APIs. Currently uses
    curated trending data that should be updated regularly.
    Last updated: December 2024
    """

    # TikTok viral trends - December 2024
    TIKTOK_TRENDS = [
        # Current viral trends (late 2024)
        {"trend": "Demure", "hashtag": "#demure", "views": "4.2B", "growth": "+125%", "category": "lifestyle"},
        {"trend": "Brat", "hashtag": "#brat", "views": "8.1B", "growth": "+95%", "category": "lifestyle"},
        {"trend": "Moo Deng", "hashtag": "#moodeng", "views": "2.8B", "growth": "+420%", "category": "humor"},
        {"trend": "Hawk Tuah", "hashtag": "#hawktuah", "views": "3.5B", "growth": "+380%", "category": "humor"},
        {"trend": "Underconsumption core", "hashtag": "#underconsumptioncore", "views": "1.2B", "growth": "+290%", "category": "lifestyle"},
        {"trend": "Brain rot", "hashtag": "#brainrot", "views": "5.4B", "growth": "+185%", "category": "humor"},
        {"trend": "Skibidi toilet", "hashtag": "#skibidi", "views": "9.2B", "growth": "+75%", "category": "humor"},
        {"trend": "Aura points", "hashtag": "#aura", "views": "2.1B", "growth": "+340%", "category": "humor"},
        {"trend": "Looksmaxxing", "hashtag": "#looksmaxxing", "views": "1.8B", "growth": "+265%", "category": "lifestyle"},
        {"trend": "Rizz", "hashtag": "#rizz", "views": "11B", "growth": "+45%", "category": "slang"},
        {"trend": "Girl dinner", "hashtag": "#girldinner", "views": "3.8B", "growth": "+65%", "category": "food"},
        {"trend": "Roman Empire", "hashtag": "#romanempire", "views": "2.9B", "growth": "+55%", "category": "humor"},
        {"trend": "Cozy cardio", "hashtag": "#cozycardio", "views": "1.5B", "growth": "+145%", "category": "fitness"},
        {"trend": "Hot girl walk", "hashtag": "#hotgirlwalk", "views": "4.2B", "growth": "+85%", "category": "fitness"},
        {"trend": "Soft life", "hashtag": "#softlife", "views": "2.4B", "growth": "+165%", "category": "lifestyle"},
        {"trend": "Unhinged", "hashtag": "#unhinged", "views": "3.1B", "growth": "+195%", "category": "humor"},
        {"trend": "Feral girl", "hashtag": "#feralgirl", "views": "890M", "growth": "+225%", "category": "lifestyle"},
        {"trend": "Coquette", "hashtag": "#coquette", "views": "4.5B", "growth": "+115%", "category": "aesthetic"},
        {"trend": "Mob wife", "hashtag": "#mobwife", "views": "1.9B", "growth": "+175%", "category": "aesthetic"},
        {"trend": "Clean girl", "hashtag": "#cleangirl", "views": "5.8B", "growth": "+65%", "category": "aesthetic"},
        {"trend": "Main character energy", "hashtag": "#maincharacter", "views": "6.2B", "growth": "+55%", "category": "mindset"},
        {"trend": "NPC", "hashtag": "#npc", "views": "4.8B", "growth": "+85%", "category": "humor"},
        {"trend": "Delulu", "hashtag": "#delulu", "views": "3.2B", "growth": "+75%", "category": "humor"},
        {"trend": "Slay", "hashtag": "#slay", "views": "12B", "growth": "+35%", "category": "slang"},
        {"trend": "Era", "hashtag": "#era", "views": "7.5B", "growth": "+95%", "category": "slang"},
    ]

    # Twitter/X trending topics - December 2024
    TWITTER_TRENDS = [
        {"trend": "Quiet quitting", "tweets": "4.2M", "growth": "+85%", "category": "work"},
        {"trend": "Act your wage", "tweets": "3.1M", "growth": "+165%", "category": "work"},
        {"trend": "Bare minimum Monday", "tweets": "1.8M", "growth": "+195%", "category": "work"},
        {"trend": "Lazy girl job", "tweets": "2.4M", "growth": "+145%", "category": "work"},
        {"trend": "Boysober", "tweets": "1.2M", "growth": "+285%", "category": "lifestyle"},
        {"trend": "Situationship", "tweets": "5.8M", "growth": "+75%", "category": "relationships"},
        {"trend": "Beige flag", "tweets": "1.5M", "growth": "+185%", "category": "relationships"},
        {"trend": "Ick", "tweets": "4.8M", "growth": "+65%", "category": "relationships"},
        {"trend": "Touch grass", "tweets": "6.2M", "growth": "+55%", "category": "humor"},
        {"trend": "Chronically online", "tweets": "3.8M", "growth": "+125%", "category": "humor"},
        {"trend": "Brain rot", "tweets": "2.9M", "growth": "+215%", "category": "humor"},
        {"trend": "Cooked", "tweets": "4.1M", "growth": "+175%", "category": "slang"},
        {"trend": "Slay", "tweets": "9.5M", "growth": "+45%", "category": "slang"},
        {"trend": "It's giving", "tweets": "3.4M", "growth": "+95%", "category": "slang"},
        {"trend": "No cap", "tweets": "7.8M", "growth": "+55%", "category": "slang"},
        {"trend": "Rent free", "tweets": "5.2M", "growth": "+85%", "category": "internet"},
        {"trend": "Understood the assignment", "tweets": "2.8M", "growth": "+115%", "category": "slang"},
        {"trend": "Living my best life", "tweets": "4.5M", "growth": "+65%", "category": "lifestyle"},
        {"trend": "Not me", "tweets": "3.2M", "growth": "+95%", "category": "humor"},
        {"trend": "Ate and left no crumbs", "tweets": "1.9M", "growth": "+165%", "category": "slang"},
    ]

    # Reddit rising trends - December 2024
    REDDIT_TRENDS = [
        {"trend": "Weaponized incompetence", "subreddit": "r/relationships", "upvotes": "85K", "growth": "+145%"},
        {"trend": "The audacity", "subreddit": "r/ChoosingBeggars", "upvotes": "72K", "growth": "+125%"},
        {"trend": "Tell me without telling me", "subreddit": "r/AskReddit", "upvotes": "58K", "growth": "+95%"},
        {"trend": "This is the way", "subreddit": "r/StarWars", "upvotes": "92K", "growth": "+65%"},
        {"trend": "Thanks I hate it", "subreddit": "r/TIHI", "upvotes": "68K", "growth": "+85%"},
        {"trend": "Oddly specific", "subreddit": "r/oddlyspecific", "upvotes": "42K", "growth": "+115%"},
        {"trend": "Introverts unite separately", "subreddit": "r/introvert", "upvotes": "35K", "growth": "+135%"},
        {"trend": "Anxiety has entered the chat", "subreddit": "r/anxiety", "upvotes": "49K", "growth": "+105%"},
        {"trend": "Adulting is hard", "subreddit": "r/adulting", "upvotes": "61K", "growth": "+75%"},
        {"trend": "Username checks out", "subreddit": "r/all", "upvotes": "78K", "growth": "+55%"},
        {"trend": "I also choose this guy", "subreddit": "r/AskReddit", "upvotes": "45K", "growth": "+85%"},
        {"trend": "My toxic trait", "subreddit": "r/meirl", "upvotes": "52K", "growth": "+145%"},
        {"trend": "Found the main character", "subreddit": "r/ImTheMainCharacter", "upvotes": "38K", "growth": "+175%"},
        {"trend": "Normalize this", "subreddit": "r/unpopularopinion", "upvotes": "28K", "growth": "+155%"},
        {"trend": "Red flag factory", "subreddit": "r/relationships", "upvotes": "32K", "growth": "+165%"},
    ]

    # Phrase templates for converting trends to merch
    PHRASE_TEMPLATES = {
        "era": [
            "In my {trend} era",
            "{trend} era",
            "Currently in my {trend} era",
            "Welcome to my {trend} era",
        ],
        "core": [
            "{trend} core",
            "Certified {trend}",
            "{trend} enthusiast",
            "Professional {trend}",
        ],
        "mood": [
            "{trend} is a mood",
            "{trend} energy only",
            "Big {trend} energy",
            "{trend} vibes",
        ],
        "identity": [
            "{trend} girlie",
            "Just a {trend} girl",
            "{trend} coded",
        ],
        "humor": [
            "{trend} is my personality",
            "My therapist said no more {trend}",
            "{trend} is my toxic trait",
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

    async def get_reddit_trends(self, limit: int = 15) -> List[Dict[str, Any]]:
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
            self.get_reddit_trends(limit_per_platform),
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
            f"In my {trend_clean} era",
            f"{trend} energy",
            f"Certified {trend_clean}",
            f"{trend} mode activated",
            f"Living that {trend_clean} life",
        ])

        return phrases[:10]

    def _calculate_shirt_potential(self, trend: Dict) -> Dict[str, Any]:
        """Calculate how well a trend translates to merch."""
        growth = int(trend.get("growth", "+0%").replace("+", "").replace("%", ""))

        score = 50

        if growth > 300:
            score += 35
        elif growth > 200:
            score += 25
        elif growth > 100:
            score += 15

        trend_text = trend.get("trend", "")
        if len(trend_text) < 15:
            score += 15
        elif len(trend_text) < 25:
            score += 8

        high_value_categories = ["humor", "lifestyle", "mindset", "work", "slang"]
        if trend.get("category", "").lower() in high_value_categories:
            score += 10

        return {
            "score": min(score, 100),
            "rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair",
            "factors": {
                "growth_momentum": "high" if growth > 200 else "medium" if growth > 100 else "low",
                "phrase_length": "optimal" if len(trend_text) < 20 else "acceptable",
                "category_fit": trend.get("category", "general"),
            }
        }

    def _combine_and_rank(self, all_trends: List[Dict]) -> List[Dict]:
        """Combine trends from all platforms and rank by potential."""
        ranked = sorted(
            all_trends,
            key=lambda x: x.get("shirt_potential", {}).get("score", 0),
            reverse=True
        )
        return ranked[:30]

    async def get_trending_phrases_for_niche(self, niche: str) -> List[Dict[str, Any]]:
        """Get trending phrases filtered by niche."""
        all_trends = await self.get_all_trends()

        niche_category_map = {
            "fitness": ["fitness", "health"],
            "work": ["work", "career"],
            "relationships": ["relationships", "dating"],
            "humor": ["humor", "meme", "slang"],
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

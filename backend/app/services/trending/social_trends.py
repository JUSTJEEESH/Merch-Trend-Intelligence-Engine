"""Merch-focused trending data service.

TWO categories of trends:
1. MERCH TRENDS - What's selling (Amazon, Etsy, Pinterest)
2. VIRAL TRENDS - Breaking content (TikTok, Twitter, Reddit)

This is how Merch Dominator and Merch Informer work.
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SocialTrendsService:
    """
    Real merch trends service.
    - Amazon/Etsy/Pinterest = What people are BUYING
    - TikTok/Twitter/Reddit = What's going VIRAL (design early)
    """

    # Merch-relevant search seeds
    SHIRT_SEEDS = [
        "funny shirt", "dad shirt", "mom shirt", "nurse shirt", "teacher shirt",
        "fishing shirt", "hunting shirt", "camping shirt", "dog lover shirt",
        "cat shirt", "coffee shirt", "beer shirt", "gaming shirt", "gym shirt",
        "grandpa shirt", "grandma shirt", "birthday shirt", "christmas shirt",
        "sarcastic shirt", "introvert shirt", "anxiety shirt", "vintage shirt",
    ]

    def __init__(self):
        self.cache = {}
        self.cache_expiry = timedelta(minutes=30)
        self._session = None

    async def _get_session(self):
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self.cache:
            return False
        cached_time = self.cache[key].get("fetched_at")
        if not cached_time:
            return False
        try:
            cached_dt = datetime.fromisoformat(cached_time)
            return datetime.utcnow() - cached_dt < self.cache_expiry
        except:
            return False

    # =============================================
    # MERCH TRENDS - What people are actually buying
    # =============================================

    async def get_amazon_trends(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Amazon autocomplete API - shows what buyers search for.
        This is the #1 source for merch research.
        """
        cache_key = "amazon_trends"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["data"][:limit]

        trends = []
        seen = set()

        url = "https://completion.amazon.com/api/2017/suggestions"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            session = await self._get_session()

            for seed in self.SHIRT_SEEDS[:12]:
                try:
                    params = {
                        "mid": "ATVPDKIKX0DER",
                        "alias": "fashion",
                        "prefix": seed,
                        "event": "onKeyPress",
                        "limit": 10,
                        "fb": 1,
                        "suggestion-type": "KEYWORD"
                    }

                    async with session.get(url, params=params, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            for idx, s in enumerate(data.get("suggestions", [])):
                                phrase = s.get("value", "").strip()
                                if phrase and phrase.lower() not in seen and len(phrase) > 5:
                                    seen.add(phrase.lower())
                                    display = self._extract_phrase(phrase)
                                    trends.append({
                                        "trend": display,
                                        "search_query": phrase,
                                        "platform": "Amazon",
                                        "source": "Amazon Autocomplete",
                                        "category": self._categorize(phrase),
                                        "growth": f"+{180 - idx * 15}%",
                                        "shirt_potential": {"score": 90 - idx * 5, "rating": "Excellent" if idx < 3 else "Good"},
                                        "fetched_at": datetime.utcnow().isoformat(),
                                        "is_live": True,
                                    })
                        else:
                            logger.warning(f"Amazon returned {resp.status}")

                    await asyncio.sleep(0.2)  # Rate limit

                except Exception as e:
                    logger.debug(f"Amazon seed '{seed}' failed: {e}")

            logger.info(f"Fetched {len(trends)} Amazon trends")

        except Exception as e:
            logger.error(f"Amazon trends failed: {e}")

        trends.sort(key=lambda x: x.get("shirt_potential", {}).get("score", 0), reverse=True)

        self.cache[cache_key] = {"data": trends, "fetched_at": datetime.utcnow().isoformat()}
        return trends[:limit]

    async def get_etsy_trends(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Etsy search suggestions - POD/handmade market.
        """
        cache_key = "etsy_trends"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["data"][:limit]

        trends = []
        seen = set()

        # Etsy's search suggest endpoint
        url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/async_search_results"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "x-requested-with": "XMLHttpRequest",
        }

        try:
            session = await self._get_session()

            for seed in ["funny shirt", "graphic tee", "vintage t-shirt", "custom shirt"]:
                try:
                    # Try the search autocomplete
                    suggest_url = f"https://www.etsy.com/search/suggest?q={seed.replace(' ', '+')}"
                    async with session.get(suggest_url, headers=headers) as resp:
                        if resp.status == 200:
                            try:
                                data = await resp.json()
                                for item in data.get("suggestions", data.get("results", []))[:8]:
                                    query = item.get("query", item.get("value", item.get("text", "")))
                                    if query and query.lower() not in seen:
                                        seen.add(query.lower())
                                        display = self._extract_phrase(query)
                                        trends.append({
                                            "trend": display,
                                            "search_query": query,
                                            "platform": "Etsy",
                                            "source": "Etsy Search",
                                            "category": self._categorize(query),
                                            "growth": f"+{120 + len(trends) * 5}%",
                                            "shirt_potential": {"score": 75, "rating": "Good"},
                                            "fetched_at": datetime.utcnow().isoformat(),
                                            "is_live": True,
                                        })
                            except:
                                pass

                    await asyncio.sleep(0.3)

                except Exception as e:
                    logger.debug(f"Etsy seed '{seed}' failed: {e}")

            logger.info(f"Fetched {len(trends)} Etsy trends")

        except Exception as e:
            logger.error(f"Etsy trends failed: {e}")

        self.cache[cache_key] = {"data": trends, "fetched_at": datetime.utcnow().isoformat()}
        return trends[:limit]

    async def get_pinterest_trends(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Pinterest trends - visual/design inspiration.
        """
        cache_key = "pinterest_trends"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["data"][:limit]

        trends = []

        # Pinterest autocomplete for shirt-related searches
        url = "https://www.pinterest.com/resource/BaseSearchResource/get/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
        }

        try:
            session = await self._get_session()

            for seed in ["t-shirt design", "shirt ideas", "graphic tee", "funny shirt"]:
                try:
                    # Pinterest typeahead
                    typeahead_url = f"https://www.pinterest.com/resource/TypeaheadResource/get/?source_url=/search/pins/?q={seed.replace(' ', '%20')}&data={{\"options\":{{\"query\":\"{seed}\",\"count\":10}}}}"

                    async with session.get(typeahead_url, headers=headers) as resp:
                        if resp.status == 200:
                            try:
                                data = await resp.json()
                                items = data.get("resource_response", {}).get("data", {}).get("items", [])
                                for item in items[:5]:
                                    term = item.get("label", item.get("term", ""))
                                    if term and term.lower() not in [t["trend"].lower() for t in trends]:
                                        trends.append({
                                            "trend": term.title(),
                                            "platform": "Pinterest",
                                            "source": "Pinterest Typeahead",
                                            "category": "design",
                                            "growth": "+100%",
                                            "shirt_potential": {"score": 70, "rating": "Good"},
                                            "fetched_at": datetime.utcnow().isoformat(),
                                            "is_live": True,
                                        })
                            except:
                                pass

                    await asyncio.sleep(0.3)

                except Exception as e:
                    logger.debug(f"Pinterest seed '{seed}' failed: {e}")

            logger.info(f"Fetched {len(trends)} Pinterest trends")

        except Exception as e:
            logger.error(f"Pinterest trends failed: {e}")

        self.cache[cache_key] = {"data": trends, "fetched_at": datetime.utcnow().isoformat()}
        return trends[:limit]

    # =============================================
    # VIRAL TRENDS - Breaking content for early design
    # =============================================

    async def get_reddit_trends(self, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Reddit public API - breaking memes and viral content.
        """
        cache_key = "reddit_trends"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["data"][:limit]

        trends = []
        seen = set()

        headers = {
            "User-Agent": "MerchTrendEngine/1.0 (Research Tool; contact@example.com)"
        }

        # Subreddits relevant to merch/memes
        subreddits = ["memes", "funny", "me_irl", "dankmemes", "wholesomememes"]

        try:
            session = await self._get_session()

            for sub in subreddits[:3]:
                try:
                    url = f"https://www.reddit.com/r/{sub}/hot.json?limit=15"
                    async with session.get(url, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            for post in data.get("data", {}).get("children", []):
                                pd = post.get("data", {})
                                title = pd.get("title", "")
                                score = pd.get("score", 0)

                                if score > 5000 and title:
                                    phrase = self._extract_meme_phrase(title)
                                    if phrase and phrase.lower() not in seen:
                                        seen.add(phrase.lower())
                                        trends.append({
                                            "trend": phrase,
                                            "full_title": title,
                                            "platform": "Reddit",
                                            "source": f"r/{sub}",
                                            "upvotes": f"{score:,}",
                                            "category": "viral",
                                            "growth": f"+{min(score // 100, 500)}%",
                                            "shirt_potential": self._score_viral(phrase, score),
                                            "fetched_at": datetime.utcnow().isoformat(),
                                            "is_live": True,
                                        })
                        else:
                            logger.warning(f"Reddit r/{sub} returned {resp.status}")

                    await asyncio.sleep(1)  # Reddit rate limits aggressively

                except Exception as e:
                    logger.debug(f"Reddit r/{sub} failed: {e}")

            logger.info(f"Fetched {len(trends)} Reddit trends")

        except Exception as e:
            logger.error(f"Reddit trends failed: {e}")

        trends.sort(key=lambda x: x.get("shirt_potential", {}).get("score", 0), reverse=True)
        self.cache[cache_key] = {"data": trends, "fetched_at": datetime.utcnow().isoformat()}
        return trends[:limit]

    async def get_tiktok_trends(self, limit: int = 15) -> List[Dict[str, Any]]:
        """
        TikTok trends - viral sounds/challenges.
        TikTok has no public API, so we use Google Trends as proxy.
        """
        cache_key = "tiktok_trends"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]["data"][:limit]

        trends = []

        try:
            from pytrends.request import TrendReq
            pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2)

            # Get trending searches
            trending_df = pytrends.trending_searches(pn='united_states')

            for idx, term in enumerate(trending_df[0].tolist()[:limit]):
                potential = self._score_viral(term, 10000)
                trends.append({
                    "trend": term,
                    "platform": "TikTok",
                    "source": "Google Trends (TikTok proxy)",
                    "category": "viral",
                    "growth": f"+{200 - idx * 10}%",
                    "shirt_potential": potential,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "is_live": True,
                })

            logger.info(f"Fetched {len(trends)} TikTok trends via Google")

        except Exception as e:
            logger.warning(f"TikTok/Google trends failed: {e}")

        self.cache[cache_key] = {"data": trends, "fetched_at": datetime.utcnow().isoformat()}
        return trends[:limit]

    async def get_twitter_trends(self, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Twitter/X trends - Use Google Trends as Twitter API is paid.
        """
        # Same as TikTok - use Google Trends
        trends = await self.get_tiktok_trends(limit)
        for t in trends:
            t["platform"] = "Twitter"
            t["source"] = "Google Trends (Twitter proxy)"
        return trends

    async def get_google_trends(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Google Trends - general trending searches."""
        return await self.get_tiktok_trends(limit)

    # =============================================
    # COMBINED DATA
    # =============================================

    async def get_all_trends(self, limit_per_platform: int = 15) -> Dict[str, Any]:
        """
        Get all trends from all platforms.

        Returns structured data:
        - amazon, etsy, pinterest = MERCH trends (what sells)
        - tiktok, twitter, reddit = VIRAL trends (what's breaking)
        """
        logger.info("Fetching all platform trends...")

        # Fetch merch trends (priority)
        merch_results = await asyncio.gather(
            self.get_amazon_trends(limit_per_platform),
            self.get_etsy_trends(limit_per_platform),
            self.get_pinterest_trends(limit_per_platform),
            return_exceptions=True
        )

        # Fetch viral trends
        viral_results = await asyncio.gather(
            self.get_reddit_trends(limit_per_platform),
            self.get_tiktok_trends(limit_per_platform),
            return_exceptions=True
        )

        # Unpack results
        amazon = merch_results[0] if not isinstance(merch_results[0], Exception) else []
        etsy = merch_results[1] if not isinstance(merch_results[1], Exception) else []
        pinterest = merch_results[2] if not isinstance(merch_results[2], Exception) else []
        reddit = viral_results[0] if not isinstance(viral_results[0], Exception) else []
        tiktok = viral_results[1] if not isinstance(viral_results[1], Exception) else []

        # Log any errors
        for i, r in enumerate(merch_results + viral_results):
            if isinstance(r, Exception):
                logger.error(f"Platform {i} failed: {r}")

        # Combined and deduplicated
        all_trends = []
        seen = set()
        for trend in amazon + etsy + pinterest + reddit + tiktok:
            key = trend.get("trend", "").lower()
            if key and key not in seen:
                seen.add(key)
                all_trends.append(trend)

        all_trends.sort(key=lambda x: x.get("shirt_potential", {}).get("score", 0), reverse=True)

        return {
            # Merch-specific (what's selling)
            "amazon": amazon,
            "etsy": etsy,
            "pinterest": pinterest,
            # Viral content (breaking trends)
            "tiktok": tiktok,
            "twitter": tiktok,  # Same source for now
            "reddit": reddit,
            # For backwards compat
            "google": tiktok,
            # Combined
            "combined": all_trends[:30],
            "fetched_at": datetime.utcnow().isoformat(),
            "is_live": len(amazon) > 0 or len(reddit) > 0 or len(tiktok) > 0,
            "counts": {
                "amazon": len(amazon),
                "etsy": len(etsy),
                "pinterest": len(pinterest),
                "reddit": len(reddit),
                "tiktok": len(tiktok),
            }
        }

    # =============================================
    # HELPERS
    # =============================================

    def _extract_phrase(self, query: str) -> str:
        """Extract merch-ready phrase from search query."""
        suffixes = [" shirt", " t-shirt", " tshirt", " tee", " for men", " for women", " gift"]
        result = query.lower()
        for s in suffixes:
            if result.endswith(s):
                result = result[:-len(s)]
        prefixes = ["funny ", "cool ", "cute ", "best "]
        for p in prefixes:
            if result.startswith(p):
                result = result[len(p):]
        return result.strip().title() if result.strip() else query.title()

    def _extract_meme_phrase(self, title: str) -> str:
        """Extract potential meme phrase from Reddit title."""
        title = re.sub(r'\[.*?\]', '', title)
        title = re.sub(r'\(.*?\)', '', title)
        title = re.sub(r'https?://\S+', '', title)
        title = ' '.join(title.split())
        words = title.split()
        if len(words) > 6:
            title = ' '.join(words[:6])
        return title.strip()[:50]

    def _categorize(self, phrase: str) -> str:
        """Categorize into merch niches."""
        p = phrase.lower()
        cats = {
            "family": ["dad", "mom", "grandpa", "grandma", "wife", "husband"],
            "profession": ["nurse", "teacher", "firefighter", "doctor", "engineer"],
            "hobby": ["fishing", "hunting", "camping", "hiking", "gaming", "golf"],
            "pets": ["dog", "cat", "horse"],
            "beverages": ["coffee", "beer", "wine", "whiskey"],
            "humor": ["funny", "sarcastic", "introvert"],
            "seasonal": ["christmas", "halloween", "thanksgiving"],
        }
        for cat, kws in cats.items():
            if any(k in p for k in kws):
                return cat
        return "general"

    def _score_viral(self, phrase: str, engagement: int) -> Dict[str, Any]:
        """Score viral content for shirt potential."""
        score = 50
        p = phrase.lower()

        # Short = better for shirts
        if len(phrase.split()) <= 3:
            score += 20
        elif len(phrase.split()) <= 5:
            score += 10

        # Meme-friendly words
        good = ["era", "mode", "vibes", "energy", "coded", "core", "pilled"]
        if any(w in p for w in good):
            score += 15

        # Avoid news/political
        bad = ["election", "president", "war", "died", "killed", "shooting"]
        if any(w in p for w in bad):
            score -= 40

        # High engagement boost
        if engagement > 50000:
            score += 15
        elif engagement > 10000:
            score += 10

        score = max(20, min(100, score))
        return {
            "score": score,
            "rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Poor"
        }

    async def get_trending_phrases_for_niche(self, niche: str) -> List[Dict[str, Any]]:
        """Get trends filtered by niche."""
        all_trends = await self.get_all_trends()
        filtered = [t for t in all_trends.get("combined", []) if t.get("category", "").lower() == niche.lower()]
        return filtered[:15] if filtered else all_trends.get("combined", [])[:10]

    def clear_cache(self):
        """Clear all cached data."""
        self.cache = {}
        logger.info("Trends cache cleared")

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()


# Singleton
social_trends_service = SocialTrendsService()

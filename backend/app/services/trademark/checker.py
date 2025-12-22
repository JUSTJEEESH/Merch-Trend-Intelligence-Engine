"""Trademark safety checking service."""
import re
import logging
from typing import List, Dict, Any, Optional
from rapidfuzz import fuzz

from ...config import settings

logger = logging.getLogger(__name__)


class TrademarkChecker:
    """Check phrases for trademark conflicts and safety issues."""

    # Known brand names to always block (partial list)
    BLOCKED_BRANDS = {
        # Tech
        "apple", "google", "microsoft", "amazon", "facebook", "meta",
        "netflix", "spotify", "twitter", "instagram", "tiktok", "youtube",
        "iphone", "ipad", "macbook", "android", "windows", "xbox", "playstation",

        # Entertainment
        "disney", "marvel", "dc comics", "star wars", "pokemon", "nintendo",
        "harry potter", "game of thrones", "lord of the rings", "netflix",
        "pixar", "dreamworks", "warner bros", "universal",

        # Sports
        "nfl", "nba", "mlb", "nhl", "fifa", "olympics", "super bowl",
        "nike", "adidas", "puma", "under armour", "reebok",

        # Fashion
        "gucci", "louis vuitton", "chanel", "prada", "versace", "armani",
        "calvin klein", "tommy hilfiger", "ralph lauren", "coach",

        # Automotive
        "tesla", "ferrari", "lamborghini", "porsche", "bmw", "mercedes",
        "ford", "chevrolet", "toyota", "honda",

        # Food & Beverage
        "coca cola", "pepsi", "starbucks", "mcdonalds", "burger king",
        "subway", "taco bell", "wendys", "dunkin", "krispy kreme",

        # Characters
        "mickey mouse", "minnie mouse", "winnie the pooh", "snoopy",
        "hello kitty", "barbie", "transformers", "power rangers",

        # Other
        "supreme", "off-white", "bape", "supreme",
    }

    # Contextual triggers that suggest infringement intent
    RISK_TRIGGERS = [
        "parody of", "inspired by", "looks like", "similar to",
        "bootleg", "knockoff", "fake", "replica", "dupe",
        "not affiliated", "unofficial", "fan made"
    ]

    def __init__(self):
        self.fuzzy_threshold = settings.FUZZY_MATCH_THRESHOLD

    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        # Lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

    def check_phrase(self, phrase: str, db=None) -> Dict[str, Any]:
        """
        Check a phrase for trademark conflicts.

        Args:
            phrase: Phrase to check
            db: Optional database session for checking stored trademarks

        Returns:
            Dictionary with safety assessment
        """
        result = {
            "is_safe": True,
            "risk_score": 0.0,
            "matches": [],
            "warnings": []
        }

        normalized = self.normalize_text(phrase)

        # Check against blocked brands
        brand_result = self._check_blocked_brands(normalized)
        if brand_result["matches"]:
            result["is_safe"] = False
            result["risk_score"] = 100.0
            result["matches"].extend(brand_result["matches"])
            return result

        # Check for risk triggers
        trigger_result = self._check_risk_triggers(normalized)
        if trigger_result["found"]:
            result["risk_score"] += 30
            result["warnings"].extend(trigger_result["warnings"])

        # Check database trademarks if available
        if db:
            db_result = self._check_database_trademarks(normalized, db)
            if db_result["matches"]:
                result["risk_score"] = max(result["risk_score"], db_result["max_score"])
                result["matches"].extend(db_result["matches"])

        # Check blocked terms in database
        if db:
            blocked_result = self._check_blocked_terms(normalized, db)
            if blocked_result["blocked"]:
                result["is_safe"] = False
                result["risk_score"] = 100.0
                result["matches"].extend(blocked_result["matches"])
                return result

        # Determine final safety
        if result["risk_score"] >= 85:
            result["is_safe"] = False
        elif result["risk_score"] >= 50:
            result["warnings"].append("Phrase has moderate risk - review carefully")

        return result

    def _check_blocked_brands(self, normalized: str) -> Dict[str, Any]:
        """Check against blocked brand list."""
        matches = []

        for brand in self.BLOCKED_BRANDS:
            # Exact match
            if brand in normalized:
                matches.append({
                    "term": brand,
                    "type": "blocked_brand",
                    "match_type": "exact",
                    "score": 100
                })
                continue

            # Fuzzy match
            words = normalized.split()
            for word in words:
                if len(word) >= 4:  # Only check words of reasonable length
                    similarity = fuzz.ratio(word, brand)
                    if similarity >= self.fuzzy_threshold:
                        matches.append({
                            "term": brand,
                            "matched_word": word,
                            "type": "blocked_brand",
                            "match_type": "fuzzy",
                            "score": similarity
                        })

        return {"matches": matches}

    def _check_risk_triggers(self, normalized: str) -> Dict[str, Any]:
        """Check for contextual risk triggers."""
        found = []
        warnings = []

        for trigger in self.RISK_TRIGGERS:
            if trigger in normalized:
                found.append(trigger)
                warnings.append(f"Contains risk trigger: '{trigger}'")

        return {
            "found": found,
            "warnings": warnings
        }

    def _check_database_trademarks(self, normalized: str, db) -> Dict[str, Any]:
        """Check against database trademarks."""
        from ...models import Trademark

        matches = []
        max_score = 0

        try:
            # Get words from phrase
            words = normalized.split()

            for word in words:
                if len(word) < 4:
                    continue

                # Search for similar trademarks
                trademarks = db.query(Trademark).filter(
                    Trademark.normalized_term.contains(word)
                ).limit(50).all()

                for tm in trademarks:
                    # Calculate similarity
                    similarity = fuzz.ratio(word, tm.normalized_term)
                    if similarity >= self.fuzzy_threshold:
                        match_data = {
                            "term": tm.term,
                            "type": "database_trademark",
                            "match_type": "fuzzy" if similarity < 100 else "exact",
                            "score": similarity,
                            "source": tm.source
                        }
                        matches.append(match_data)
                        max_score = max(max_score, similarity)

        except Exception as e:
            logger.error(f"Database trademark check failed: {e}")

        return {
            "matches": matches,
            "max_score": max_score
        }

    def _check_blocked_terms(self, normalized: str, db) -> Dict[str, Any]:
        """Check against manually blocked terms."""
        from ...models import BlockedTerm

        matches = []
        blocked = False

        try:
            blocked_terms = db.query(BlockedTerm).all()

            for term in blocked_terms:
                if term.normalized_term in normalized:
                    blocked = True
                    matches.append({
                        "term": term.term,
                        "type": "blocked_term",
                        "reason": term.reason,
                        "score": 100
                    })

        except Exception as e:
            logger.error(f"Blocked terms check failed: {e}")

        return {
            "blocked": blocked,
            "matches": matches
        }

    def batch_check(self, phrases: List[str], db=None) -> List[Dict[str, Any]]:
        """Check multiple phrases at once."""
        results = []
        for phrase in phrases:
            result = self.check_phrase(phrase, db)
            result["phrase"] = phrase
            results.append(result)
        return results

    def get_safe_phrases(self, phrases: List[str], db=None) -> List[str]:
        """Filter list to only return safe phrases."""
        safe = []
        for phrase in phrases:
            result = self.check_phrase(phrase, db)
            if result["is_safe"]:
                safe.append(phrase)
        return safe

    def suggest_alternatives(self, phrase: str) -> List[str]:
        """
        Suggest safer alternatives for a risky phrase.

        This is a basic implementation - could be enhanced with
        more sophisticated NLP.
        """
        suggestions = []
        normalized = self.normalize_text(phrase)

        # Check what brands are in the phrase
        found_brands = []
        for brand in self.BLOCKED_BRANDS:
            if brand in normalized:
                found_brands.append(brand)

        if not found_brands:
            return [phrase]  # No brands found, phrase might be safe

        # Try removing brand references
        suggestion = normalized
        for brand in found_brands:
            suggestion = suggestion.replace(brand, "")
        suggestion = ' '.join(suggestion.split())

        if suggestion and len(suggestion) > 3:
            suggestions.append(suggestion)

        # Add generic alternatives
        suggestions.append("Consider using a generic description instead of brand names")

        return suggestions

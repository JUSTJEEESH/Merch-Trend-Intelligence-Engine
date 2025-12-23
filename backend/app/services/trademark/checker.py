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

    # Famous trademarked slogans/phrases - THESE ARE NOT SAFE TO USE
    BLOCKED_SLOGANS = {
        # Nike
        "just do it",
        # McDonald's
        "im lovin it", "i'm lovin it", "im loving it", "i'm loving it",
        # Apple
        "think different",
        # L'Oreal
        "because youre worth it", "because you're worth it",
        # De Beers
        "a diamond is forever",
        # Mastercard
        "priceless", "there are some things money cant buy",
        # Verizon
        "can you hear me now",
        # Subway
        "eat fresh",
        # Burger King
        "have it your way",
        # KFC
        "finger lickin good", "finger lickin' good",
        # M&Ms
        "melts in your mouth",
        # Skittles
        "taste the rainbow",
        # Red Bull
        "gives you wings", "red bull gives you wings",
        # Gatorade
        "is it in you",
        # Las Vegas
        "what happens in vegas",
        # State Farm
        "like a good neighbor",
        # Allstate
        "youre in good hands", "you're in good hands",
        # Geico
        "15 minutes could save you",
        # Maybelline
        "maybe shes born with it", "maybe she's born with it",
        # Kay Jewelers
        "every kiss begins with kay",
        # Bounty
        "the quicker picker upper",
        # Wheaties
        "breakfast of champions",
        # Rice Krispies
        "snap crackle pop",
        # Frosted Flakes
        "theyre great", "they're great", "theyre grrreat",
        # Got Milk
        "got milk",
        # Capital One
        "whats in your wallet", "what's in your wallet",
        # BMW
        "the ultimate driving machine",
        # Audi
        "vorsprung durch technik",
        # Lexus
        "the relentless pursuit of perfection",
        # Toyota
        "lets go places", "let's go places",
        # Ford
        "built ford tough",
        # Chevy
        "find new roads",
        # Dodge
        "grab life by the horns",
        # Energizer
        "keeps going and going",
        # Duracell
        "trusted everywhere",
        # Gillette
        "the best a man can get",
        # Disneyland
        "the happiest place on earth",
        # Disney
        "where dreams come true",
        # Toys R Us
        "i dont wanna grow up",
        # Army
        "be all you can be",
        # Marines
        "the few the proud",
        # New York
        "i love ny", "i heart ny",
        # Adidas
        "impossible is nothing",
        # Reebok
        "i am what i am",
        # Under Armour
        "i will", "protect this house",
        # Taco Bell
        "think outside the bun", "live mas",
        # Wendys
        "wheres the beef", "where's the beef",
        # Arby's
        "we have the meats",
        # Chick-fil-A
        "eat mor chikin",
        # Home Depot
        "you can do it we can help",
        # Lowes
        "never stop improving",
        # Target
        "expect more pay less",
        # Walmart
        "save money live better",
        # Best Buy
        "expert service unbeatable price",
        # FedEx
        "when it absolutely positively",
        # UPS
        "what can brown do for you",
        # USPS
        "neither snow nor rain",
        # Visa
        "its everywhere you want to be",
        # American Express
        "dont leave home without it",
        # Staples
        "that was easy",
        # Office Depot
        "taking care of business",
        # General Electric
        "imagination at work",
        # 3M
        "innovation",
        # Microsoft
        "be what's next", "your potential our passion",
        # Intel
        "intel inside",
        # AMD
        "the future is fusion",
        # HP
        "invent",
        # Dell
        "the power to do more",
        # AT&T
        "rethink possible", "reach out and touch someone",
        # T-Mobile
        "get more",
        # Sprint
        "the now network",
        # Coca-Cola
        "open happiness", "taste the feeling", "its the real thing",
        # Pepsi
        "the choice of a new generation", "for those who think young",
        # Dr Pepper
        "be a pepper", "its not for women",
        # Mountain Dew
        "do the dew",
        # Sprite
        "obey your thirst",
        # 7-Up
        "the uncola",
        # Budweiser
        "king of beers", "this buds for you", "whassup",
        # Miller
        "its miller time",
        # Coors
        "the banquet beer",
        # Corona
        "find your beach",
        # Heineken
        "open your world",
        # Jack Daniels
        "old no 7",
        # Jim Beam
        "bold choice",
        # Johnnie Walker
        "keep walking",
        # Absolut
        "absolut perfection",
        # Grey Goose
        "fly beyond",
        # Patron
        "simply perfect",
        # HBO
        "its not tv its hbo",
        # Netflix
        "see whats next",
        # Amazon
        "and you're done", "work hard have fun make history",
        # Google
        "dont be evil",
        # Facebook
        "move fast and break things",
        # Twitter
        "whats happening",
        # YouTube
        "broadcast yourself",
        # TikTok
        "make your day",
        # Snapchat
        "life's more fun when you live in the moment",
        # LinkedIn
        "relationships matter",
        # Pinterest
        "the home of inspiration",
        # Reddit
        "the front page of the internet",
        # ESPN
        "the worldwide leader in sports",
        # Sports Center
        "this is sportscenter",
    }

    # Common misspellings and variations of blocked slogans
    SLOGAN_PATTERNS = [
        (r"just\s*do\s*it", "Just Do It (Nike)"),
        (r"i.?m\s*lovin.?\s*it", "I'm Lovin' It (McDonald's)"),
        (r"think\s*different", "Think Different (Apple)"),
        (r"got\s*milk", "Got Milk"),
        (r"breakfast\s*of\s*champions", "Breakfast of Champions (Wheaties)"),
        (r"the\s*happiest\s*place", "The Happiest Place (Disney)"),
        (r"whats?\s*in\s*your\s*wallet", "What's In Your Wallet (Capital One)"),
        (r"finger\s*lickin", "Finger Lickin' Good (KFC)"),
        (r"taste\s*the\s*rainbow", "Taste the Rainbow (Skittles)"),
        (r"gives?\s*you\s*wings", "Gives You Wings (Red Bull)"),
        (r"snap\s*crackle\s*pop", "Snap Crackle Pop (Rice Krispies)"),
        (r"melts?\s*in\s*your\s*mouth", "Melts In Your Mouth (M&Ms)"),
        (r"wheres?\s*the\s*beef", "Where's the Beef (Wendy's)"),
        (r"have\s*it\s*your\s*way", "Have It Your Way (Burger King)"),
        (r"eat\s*fresh", "Eat Fresh (Subway)"),
        (r"im?\s*worth\s*it", "Because You're Worth It (L'Oreal)"),
        (r"maybe\s*shes?\s*born", "Maybe She's Born With It (Maybelline)"),
        (r"king\s*of\s*beers", "King of Beers (Budweiser)"),
        (r"ultimate\s*driving\s*machine", "Ultimate Driving Machine (BMW)"),
        (r"built\s*ford\s*tough", "Built Ford Tough"),
        (r"impossible\s*is\s*nothing", "Impossible Is Nothing (Adidas)"),
        (r"the\s*few\s*the\s*proud", "The Few The Proud (Marines)"),
        (r"be\s*all\s*you\s*can\s*be", "Be All You Can Be (Army)"),
        (r"protect\s*this\s*house", "Protect This House (Under Armour)"),
        (r"we\s*have\s*the\s*meats", "We Have The Meats (Arby's)"),
        (r"save\s*money\s*live\s*better", "Save Money Live Better (Walmart)"),
        (r"that\s*was\s*easy", "That Was Easy (Staples)"),
        (r"open\s*happiness", "Open Happiness (Coca-Cola)"),
        (r"do\s*the\s*dew", "Do The Dew (Mountain Dew)"),
        (r"obey\s*your\s*thirst", "Obey Your Thirst (Sprite)"),
        (r"keep\s*walking", "Keep Walking (Johnnie Walker)"),
        (r"find\s*your\s*beach", "Find Your Beach (Corona)"),
        (r"live\s*mas", "Live Mas (Taco Bell)"),
        (r"never\s*stop\s*improving", "Never Stop Improving (Lowe's)"),
        (r"expect\s*more\s*pay\s*less", "Expect More Pay Less (Target)"),
    ]

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

        # Check against blocked slogans (exact match)
        slogan_result = self._check_blocked_slogans(normalized)
        if slogan_result["matches"]:
            result["is_safe"] = False
            result["risk_score"] = 100.0
            result["matches"].extend(slogan_result["matches"])
            return result

        # Check against slogan patterns (regex match for variations)
        pattern_result = self._check_slogan_patterns(normalized)
        if pattern_result["matches"]:
            result["is_safe"] = False
            result["risk_score"] = 100.0
            result["matches"].extend(pattern_result["matches"])
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

    def _check_blocked_slogans(self, normalized: str) -> Dict[str, Any]:
        """Check against blocked slogan list (exact and near-exact matches)."""
        matches = []

        for slogan in self.BLOCKED_SLOGANS:
            if slogan in normalized:
                matches.append({
                    "term": slogan,
                    "type": "blocked_slogan",
                    "match_type": "exact",
                    "score": 100
                })

        return {"matches": matches}

    def _check_slogan_patterns(self, normalized: str) -> Dict[str, Any]:
        """Check against regex patterns for slogan variations."""
        matches = []

        for pattern, slogan_name in self.SLOGAN_PATTERNS:
            if re.search(pattern, normalized, re.IGNORECASE):
                matches.append({
                    "term": slogan_name,
                    "type": "blocked_slogan_pattern",
                    "match_type": "pattern",
                    "score": 100
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

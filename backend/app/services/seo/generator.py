"""Amazon Merch SEO listing generator - Professional quality listings."""
import re
import random
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SEOGenerator:
    """Generate professional SEO-optimized listings for Amazon Merch on Demand."""

    # Words forbidden in Amazon Merch listings
    FORBIDDEN_WORDS = [
        "shirt", "t-shirt", "tshirt", "tee", "hoodie", "sweatshirt",
        "tank top", "tanktop", "long sleeve", "clothing", "apparel",
        "pullover", "crewneck", "raglan",
        "best seller", "bestseller", "#1", "number one", "top rated",
        "amazon", "prime", "alexa", "kindle", "echo",
        "authentic", "genuine", "official", "licensed",
        "free shipping", "discount", "sale", "cheap",
        "limited edition", "exclusive", "rare",
        "sexy", "adult", "explicit",
    ]

    PRODUCT_WORDS = [
        "shirt", "t-shirt", "tshirt", "tee", "top",
        "hoodie", "sweatshirt", "sweater", "pullover",
        "tank", "vest", "jacket", "clothing"
    ]

    # Professional title patterns (based on top sellers)
    TITLE_PATTERNS = [
        "{phrase} - Funny {niche} Gift Idea",
        "{phrase} - {niche} Lover Gift",
        "{phrase} - Cool {niche} Quote",
        "{phrase} - {niche} Saying Gift Idea",
        "Funny {niche} - {phrase}",
        "{phrase} - Hilarious {niche} Quote",
        "{phrase} - Perfect Gift For {niche} Lovers",
        "{phrase} - {niche} Humor Quote",
    ]

    # Niche-specific data
    NICHE_DATA = {
        "coffee": {
            "keywords": ["coffee lover", "caffeine", "espresso", "morning", "brew", "latte", "barista", "coffee addict"],
            "audience": ["coffee lovers", "caffeine addicts", "baristas", "morning people", "espresso enthusiasts"],
            "occasions": ["coffee dates", "morning routines", "coffee shop visits", "caffeine breaks"],
        },
        "fitness": {
            "keywords": ["gym", "workout", "gains", "lifting", "fitness", "exercise", "muscles", "training"],
            "audience": ["gym lovers", "fitness enthusiasts", "bodybuilders", "workout addicts", "gym rats"],
            "occasions": ["leg day", "gym sessions", "workout time", "training days"],
        },
        "dogs": {
            "keywords": ["dog lover", "puppy", "canine", "pet parent", "fur baby", "dog mom", "dog dad", "paw"],
            "audience": ["dog lovers", "pet parents", "dog moms", "dog dads", "puppy owners"],
            "occasions": ["dog walks", "pet adoption days", "dog park visits"],
        },
        "cats": {
            "keywords": ["cat lover", "kitten", "feline", "cat mom", "cat dad", "meow", "kitty", "whiskers"],
            "audience": ["cat lovers", "cat moms", "cat dads", "feline enthusiasts", "kitty owners"],
            "occasions": ["lazy days with cats", "kitten adoption", "cat cuddle time"],
        },
        "nursing": {
            "keywords": ["nurse", "RN", "healthcare", "medical", "scrubs", "hospital", "nursing", "patient care"],
            "audience": ["nurses", "RNs", "healthcare workers", "medical professionals", "nursing students"],
            "occasions": ["nurse appreciation", "hospital shifts", "nursing school graduation"],
        },
        "teaching": {
            "keywords": ["teacher", "educator", "classroom", "school", "teaching", "students", "education"],
            "audience": ["teachers", "educators", "professors", "teaching assistants", "school staff"],
            "occasions": ["back to school", "teacher appreciation", "end of school year", "graduation"],
        },
        "gaming": {
            "keywords": ["gamer", "gaming", "video games", "player", "console", "PC gaming", "esports"],
            "audience": ["gamers", "video game fans", "esports enthusiasts", "console players", "PC gamers"],
            "occasions": ["game night", "new game releases", "gaming marathons", "esports events"],
        },
        "fishing": {
            "keywords": ["fishing", "angler", "bass", "fisherman", "tackle", "catch", "reel", "lake", "boat"],
            "audience": ["anglers", "fishermen", "bass fishers", "fly fishing fans", "fishing enthusiasts"],
            "occasions": ["fishing trips", "lake outings", "bass tournaments", "early morning fishing"],
        },
        "parenting": {
            "keywords": ["mom", "dad", "parent", "kids", "family", "mother", "father", "mama", "papa"],
            "audience": ["moms", "dads", "parents", "new parents", "busy parents", "tired parents"],
            "occasions": ["Mother's Day", "Father's Day", "family gatherings", "parenting life"],
        },
        "beer": {
            "keywords": ["beer", "craft beer", "brewery", "hops", "IPA", "ale", "brew", "drinking"],
            "audience": ["beer lovers", "craft beer fans", "brewery enthusiasts", "IPA lovers", "beer drinkers"],
            "occasions": ["happy hour", "brewery tours", "beer tasting", "game day"],
        },
        "wine": {
            "keywords": ["wine", "vino", "winery", "grape", "merlot", "chardonnay", "rosé", "sommelier"],
            "audience": ["wine lovers", "wine enthusiasts", "sommeliers", "wine moms", "wine dads"],
            "occasions": ["wine night", "wine tasting", "vineyard visits", "girls night out"],
        },
        "hunting": {
            "keywords": ["hunting", "hunter", "deer", "duck", "bow", "rifle", "game", "outdoors", "camo"],
            "audience": ["hunters", "deer hunters", "duck hunters", "bow hunters", "outdoor enthusiasts"],
            "occasions": ["hunting season", "deer season", "duck season", "hunting trips"],
        },
        "outdoors": {
            "keywords": ["hiking", "camping", "mountains", "nature", "outdoors", "adventure", "trails", "explore"],
            "audience": ["hikers", "campers", "nature lovers", "outdoor enthusiasts", "adventure seekers"],
            "occasions": ["hiking trips", "camping weekends", "mountain adventures", "nature walks"],
        },
    }

    # Generic data for unknown niches
    GENERIC_DATA = {
        "keywords": ["funny", "humor", "quote", "saying", "gift", "idea", "present", "cool", "awesome"],
        "audience": ["men", "women", "adults", "teens", "friends", "family", "coworkers"],
        "occasions": ["birthdays", "Christmas", "holidays", "special occasions", "everyday wear"],
    }

    def generate(
        self,
        phrase: str,
        niche: Optional[str] = None,
        tone: str = "neutral"
    ) -> Dict[str, Any]:
        """Generate professional Amazon Merch listing."""
        result = {
            "title": "",
            "bullet_1": "",
            "bullet_2": "",
            "description": "",
            "backend_keywords": "",
            "is_compliant": True,
            "warnings": []
        }

        clean_phrase = self._clean_phrase(phrase)
        niche_data = self._get_niche_data(niche)

        # Generate each field
        result["title"] = self._generate_title(clean_phrase, niche, niche_data)
        result["bullet_1"] = self._generate_bullet_1(clean_phrase, niche_data)
        result["bullet_2"] = self._generate_bullet_2()
        result["description"] = self._generate_description(clean_phrase, niche, niche_data)
        result["backend_keywords"] = self._generate_backend_keywords(clean_phrase, niche_data)

        # Validate
        validation = self.validate_listing(
            result["title"],
            result["bullet_1"],
            result["bullet_2"],
            result["description"],
            result["backend_keywords"]
        )
        result["is_compliant"] = validation["is_compliant"]
        result["warnings"] = validation["issues"]

        return result

    def _clean_phrase(self, phrase: str) -> str:
        """Clean phrase for use in listings."""
        words = phrase.split()
        clean_words = [w for w in words if w.lower() not in self.PRODUCT_WORDS]
        return ' '.join(clean_words) if clean_words else phrase

    def _get_niche_data(self, niche: Optional[str]) -> Dict:
        """Get niche-specific data."""
        if niche and niche.lower() in self.NICHE_DATA:
            return self.NICHE_DATA[niche.lower()]
        return self.GENERIC_DATA

    def _generate_title(self, phrase: str, niche: Optional[str], niche_data: Dict) -> str:
        """Generate professional title (max 80 chars)."""
        # Capitalize phrase properly
        phrase_title = phrase.title()

        # Get niche display name
        niche_display = niche.title() if niche else "Gift"

        # Try different patterns until we find one that fits
        patterns = [
            f"{phrase_title} - Funny {niche_display} Gift Idea",
            f"{phrase_title} - {niche_display} Lover Quote",
            f"Funny {niche_display} - {phrase_title}",
            f"{phrase_title} - {niche_display} Humor",
            f"{phrase_title} Gift For {niche_display} Lovers",
            f"{phrase_title} - {niche_display} Saying",
            f"{phrase_title}",
        ]

        for pattern in patterns:
            if len(pattern) <= 80:
                return pattern

        # If all too long, truncate
        return phrase_title[:77] + "..."

    def _generate_bullet_1(self, phrase: str, niche_data: Dict) -> str:
        """Generate first bullet point - audience and gift occasions."""
        audience = random.sample(niche_data["audience"], min(3, len(niche_data["audience"])))
        audience_str = ", ".join(audience)

        bullet = f"Perfect gift for {audience_str}. Great for birthdays, Christmas, Mother's Day, Father's Day, and any special occasion. Makes an awesome present for friends and family."

        return bullet[:256] if len(bullet) > 256 else bullet

    def _generate_bullet_2(self) -> str:
        """Generate second bullet point - product features (Amazon standard)."""
        return "Lightweight, Classic fit, Double-needle sleeve and bottom hem"

    def _generate_description(self, phrase: str, niche: Optional[str], niche_data: Dict) -> str:
        """Generate professional product description."""
        audience = random.sample(niche_data["audience"], min(3, len(niche_data["audience"])))
        keywords = random.sample(niche_data["keywords"], min(4, len(niche_data["keywords"])))

        niche_name = niche.title() if niche else "this theme"

        description = f"""Are you looking for a fun and unique gift? This "{phrase}" design is perfect!

This eye-catching design features the saying "{phrase}" and is ideal for anyone who loves {niche_name.lower()}. Whether you're shopping for yourself or looking for that perfect gift, this is sure to be a hit.

Makes an excellent gift for {', '.join(audience)}. Perfect for birthdays, Christmas, holidays, anniversaries, or just because. Show off your personality and sense of humor with this awesome design.

Great conversation starter and a wonderful way to express yourself. Keywords: {', '.join(keywords)}."""

        return description[:2000] if len(description) > 2000 else description

    def _generate_backend_keywords(self, phrase: str, niche_data: Dict) -> str:
        """Generate backend search keywords (max 250 chars)."""
        # Phrase words
        phrase_words = [w.lower() for w in phrase.split() if len(w) > 2]

        # Niche keywords
        niche_keywords = niche_data["keywords"][:5]

        # Generic gift keywords
        gift_keywords = ["gift", "present", "birthday", "christmas", "funny", "humor", "quote", "saying"]

        # Combine and deduplicate
        all_keywords = []
        seen = set()
        for kw in phrase_words + niche_keywords + gift_keywords:
            kw_lower = kw.lower()
            if kw_lower not in seen and kw_lower not in self.PRODUCT_WORDS:
                seen.add(kw_lower)
                all_keywords.append(kw_lower)

        # Join and respect limit
        result = ' '.join(all_keywords)
        if len(result) > 250:
            result = result[:250].rsplit(' ', 1)[0]

        return result

    def validate_listing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None,
        backend_keywords: str = None
    ) -> Dict[str, Any]:
        """Validate listing against Amazon Merch guidelines."""
        issues = []

        all_content = ' '.join(filter(None, [title, bullet_1, bullet_2, description])).lower()

        for word in self.FORBIDDEN_WORDS:
            if word in all_content:
                issues.append(f"Contains forbidden word: '{word}'")

        if title and len(title) > 80:
            issues.append(f"Title too long: {len(title)}/80 characters")

        if bullet_1 and len(bullet_1) > 256:
            issues.append(f"Bullet 1 too long: {len(bullet_1)}/256 characters")

        if bullet_2 and len(bullet_2) > 256:
            issues.append(f"Bullet 2 too long: {len(bullet_2)}/256 characters")

        if description and len(description) > 2000:
            issues.append(f"Description too long: {len(description)}/2000 characters")

        if backend_keywords and len(backend_keywords) > 250:
            issues.append(f"Backend keywords too long: {len(backend_keywords)}/250 characters")

        if title:
            for word in self.PRODUCT_WORDS:
                if word in title.lower():
                    issues.append(f"Title contains product word: '{word}'")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues
        }

    def get_forbidden_words(self) -> Dict[str, List[str]]:
        """Return the forbidden words for reference."""
        return {
            "forbidden": self.FORBIDDEN_WORDS,
            "restricted_product_words": self.PRODUCT_WORDS
        }

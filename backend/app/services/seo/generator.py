"""Amazon Merch SEO listing generator."""
import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SEOGenerator:
    """Generate SEO-optimized listings for Amazon Merch on Demand."""

    # Words forbidden in Amazon Merch listings
    FORBIDDEN_WORDS = [
        # Product type words (not allowed in title)
        "shirt", "t-shirt", "tshirt", "tee", "hoodie", "sweatshirt",
        "tank top", "tanktop", "long sleeve", "clothing", "apparel",
        "pullover", "crewneck", "raglan",

        # Amazon policy violations
        "best seller", "bestseller", "#1", "number one", "top rated",
        "amazon", "prime", "alexa", "kindle", "echo",
        "authentic", "genuine", "official", "licensed",
        "free shipping", "discount", "sale", "cheap",
        "limited edition", "exclusive", "rare",

        # Potentially problematic
        "sexy", "adult", "explicit",
    ]

    # Product words to avoid in titles
    PRODUCT_WORDS = [
        "shirt", "t-shirt", "tshirt", "tee", "top",
        "hoodie", "sweatshirt", "sweater", "pullover",
        "tank", "vest", "jacket", "clothing"
    ]

    # Niche-specific keywords
    NICHE_KEYWORDS = {
        "fitness": ["gym", "workout", "gains", "lifting", "exercise", "health"],
        "coffee": ["caffeine", "espresso", "morning", "brew", "barista", "latte"],
        "dogs": ["puppy", "canine", "pet", "fur baby", "paw", "woof"],
        "cats": ["kitten", "feline", "meow", "whiskers", "purr"],
        "nursing": ["nurse", "healthcare", "hospital", "medical", "RN", "scrubs"],
        "teaching": ["teacher", "educator", "school", "classroom", "students"],
        "gaming": ["gamer", "player", "video games", "console", "PC"],
        "fishing": ["angler", "fishing", "bass", "catch", "tackle", "outdoors"],
        "parenting": ["mom", "dad", "parent", "kids", "family"],
        "programming": ["developer", "coder", "software", "tech", "debug"],
    }

    # Tone templates
    TONE_TEMPLATES = {
        "neutral": {
            "title_format": "{phrase} - {keyword} Design",
            "bullet_format": "Features the phrase '{phrase}' - {benefit}",
        },
        "funny": {
            "title_format": "Funny {phrase} - Humorous {keyword} Gift",
            "bullet_format": "Hilarious '{phrase}' design - {benefit}",
        },
        "sarcastic": {
            "title_format": "{phrase} - Sarcastic {keyword} Quote",
            "bullet_format": "Witty '{phrase}' saying - {benefit}",
        },
        "proud": {
            "title_format": "{phrase} - Proud {keyword} Statement",
            "bullet_format": "Bold '{phrase}' declaration - {benefit}",
        }
    }

    def generate(
        self,
        phrase: str,
        niche: Optional[str] = None,
        tone: str = "neutral"
    ) -> Dict[str, Any]:
        """
        Generate SEO-optimized listing content.

        Args:
            phrase: The main phrase for the design
            niche: Optional niche for keyword targeting
            tone: Tone of the listing (neutral, funny, sarcastic, proud)

        Returns:
            Dictionary with title, bullets, description, and backend keywords
        """
        result = {
            "title": "",
            "bullet_1": "",
            "bullet_2": "",
            "description": "",
            "backend_keywords": "",
            "is_compliant": True,
            "warnings": []
        }

        # Clean the phrase
        clean_phrase = self._clean_phrase(phrase)

        # Get niche keywords
        keywords = self._get_keywords(niche)

        # Generate title (max 80 characters)
        result["title"] = self._generate_title(clean_phrase, keywords, tone)

        # Generate bullet points (max 256 characters each)
        result["bullet_1"], result["bullet_2"] = self._generate_bullets(
            clean_phrase, keywords, tone
        )

        # Generate description (max 2000 characters)
        result["description"] = self._generate_description(
            clean_phrase, keywords, niche
        )

        # Generate backend keywords (max 250 characters)
        result["backend_keywords"] = self._generate_backend_keywords(
            clean_phrase, keywords, niche
        )

        # Validate compliance
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
        # Remove product words
        words = phrase.split()
        clean_words = [
            w for w in words
            if w.lower() not in self.PRODUCT_WORDS
        ]
        return ' '.join(clean_words) if clean_words else phrase

    def _get_keywords(self, niche: Optional[str]) -> List[str]:
        """Get relevant keywords for the niche."""
        if niche and niche.lower() in self.NICHE_KEYWORDS:
            return self.NICHE_KEYWORDS[niche.lower()]
        return ["gift", "present", "idea", "design", "quote", "saying"]

    def _generate_title(
        self,
        phrase: str,
        keywords: List[str],
        tone: str
    ) -> str:
        """Generate SEO-optimized title."""
        # Get tone template
        template = self.TONE_TEMPLATES.get(tone, self.TONE_TEMPLATES["neutral"])

        # Select a keyword
        keyword = keywords[0] if keywords else "Gift"

        # Generate base title
        title = template["title_format"].format(
            phrase=phrase.title(),
            keyword=keyword.title()
        )

        # Truncate if too long (max 80 chars for Merch)
        if len(title) > 80:
            title = phrase.title()[:77] + "..."

        return title

    def _generate_bullets(
        self,
        phrase: str,
        keywords: List[str],
        tone: str
    ) -> tuple:
        """Generate two bullet points."""
        benefits = [
            "Perfect gift idea for friends and family",
            "Great for birthdays, holidays, or any occasion",
            "Unique design that stands out",
            "Makes a great conversation starter",
            "Show off your personality",
        ]

        audiences = [
            "men, women, and teens",
            "adults who appreciate humor",
            "anyone with a great sense of style",
            "people who love unique designs",
        ]

        # Bullet 1: Feature + benefit
        bullet_1 = f"Features the saying '{phrase}' - {benefits[0]}"

        # Bullet 2: Audience + occasion
        bullet_2 = f"Great for {audiences[0]} - {benefits[1]}"

        # Truncate if needed (max 256 chars each)
        bullet_1 = bullet_1[:253] + "..." if len(bullet_1) > 256 else bullet_1
        bullet_2 = bullet_2[:253] + "..." if len(bullet_2) > 256 else bullet_2

        return bullet_1, bullet_2

    def _generate_description(
        self,
        phrase: str,
        keywords: List[str],
        niche: Optional[str]
    ) -> str:
        """Generate product description."""
        niche_text = f"for {niche} enthusiasts" if niche else "for anyone"

        description = f"""Looking for the perfect gift {niche_text}? This "{phrase}" design is exactly what you need!

This unique design features the phrase "{phrase}" and makes an excellent gift for birthdays, holidays, Christmas, or any special occasion.

Whether you're shopping for yourself or looking for that perfect present, this design is sure to bring a smile. It's a great way to express personality and style.

Makes a wonderful gift for {', '.join(keywords[:3]) if keywords else 'friends and family'}."""

        # Truncate if needed (max 2000 chars)
        if len(description) > 2000:
            description = description[:1997] + "..."

        return description

    def _generate_backend_keywords(
        self,
        phrase: str,
        keywords: List[str],
        niche: Optional[str]
    ) -> str:
        """Generate backend search keywords."""
        # Start with phrase words
        phrase_words = phrase.lower().split()

        # Add niche keywords
        all_keywords = list(set(phrase_words + keywords))

        # Add generic gift keywords
        gift_keywords = [
            "gift", "present", "birthday", "christmas", "holiday",
            "funny", "humor", "quote", "saying", "design"
        ]

        all_keywords.extend(gift_keywords)

        # Remove duplicates and product words
        clean_keywords = []
        seen = set()
        for kw in all_keywords:
            kw_lower = kw.lower()
            if (kw_lower not in seen and
                kw_lower not in self.PRODUCT_WORDS and
                len(kw_lower) > 1):
                seen.add(kw_lower)
                clean_keywords.append(kw_lower)

        # Join and truncate (max 250 chars)
        backend_str = ' '.join(clean_keywords)
        if len(backend_str) > 250:
            # Truncate at word boundary
            backend_str = backend_str[:250].rsplit(' ', 1)[0]

        return backend_str

    def validate_listing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None,
        backend_keywords: str = None
    ) -> Dict[str, Any]:
        """
        Validate listing content against Amazon Merch guidelines.

        Returns:
            Dictionary with is_compliant boolean and list of issues
        """
        issues = []

        all_content = ' '.join(filter(None, [
            title, bullet_1, bullet_2, description
        ])).lower()

        # Check for forbidden words
        for word in self.FORBIDDEN_WORDS:
            if word in all_content:
                issues.append(f"Contains forbidden word: '{word}'")

        # Check title length
        if title and len(title) > 80:
            issues.append(f"Title too long: {len(title)}/80 characters")

        # Check bullet lengths
        if bullet_1 and len(bullet_1) > 256:
            issues.append(f"Bullet 1 too long: {len(bullet_1)}/256 characters")
        if bullet_2 and len(bullet_2) > 256:
            issues.append(f"Bullet 2 too long: {len(bullet_2)}/256 characters")

        # Check description length
        if description and len(description) > 2000:
            issues.append(f"Description too long: {len(description)}/2000 characters")

        # Check backend keywords length
        if backend_keywords and len(backend_keywords) > 250:
            issues.append(f"Backend keywords too long: {len(backend_keywords)}/250 characters")

        # Check for product words in title
        if title:
            for word in self.PRODUCT_WORDS:
                if word in title.lower():
                    issues.append(f"Title contains product word: '{word}'")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues
        }

    def optimize_existing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """Optimize existing listing content."""
        optimized = {
            "title": title,
            "bullet_1": bullet_1,
            "bullet_2": bullet_2,
            "description": description,
            "changes": []
        }

        # Remove product words from title
        if title:
            for word in self.PRODUCT_WORDS:
                if word in title.lower():
                    title = re.sub(rf'\b{word}\b', '', title, flags=re.IGNORECASE)
                    optimized["changes"].append(f"Removed '{word}' from title")
            optimized["title"] = ' '.join(title.split())

        # Remove forbidden words from all content
        for field in ["title", "bullet_1", "bullet_2", "description"]:
            content = optimized.get(field)
            if content:
                for word in self.FORBIDDEN_WORDS:
                    if word in content.lower():
                        content = re.sub(rf'\b{word}\b', '', content, flags=re.IGNORECASE)
                        optimized["changes"].append(f"Removed '{word}' from {field}")
                optimized[field] = ' '.join(content.split())

        return optimized

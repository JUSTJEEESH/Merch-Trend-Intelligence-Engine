"""Amazon listing optimizer service for Merch titles, bullets, and keywords."""
import random
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ListingOptimizer:
    """
    Service for generating optimized Amazon Merch listings.
    Creates titles, bullet points, and backend keywords.
    """

    # Title templates by niche
    TITLE_TEMPLATES = {
        "general": [
            "{phrase} - Funny {product} for {audience}",
            "{phrase} {product} - {adjective} Gift for {audience}",
            "{adjective} {phrase} {product} for {audience}",
            "{phrase} - {adjective} {product} Gift Idea",
            "{phrase} {product} - {occasion} Gift for {audience}",
        ],
        "coffee": [
            "{phrase} - Coffee Lover {product} for {audience}",
            "{phrase} {product} - Gift for Coffee Addicts",
            "Coffee {phrase} - Funny {product} for Caffeine Lovers",
        ],
        "mom": [
            "{phrase} - Mom {product} for Mother's Day",
            "{phrase} {product} - Funny Gift for Mom",
            "Best Mom {phrase} - {product} for Mothers",
        ],
        "dad": [
            "{phrase} - Dad {product} for Father's Day",
            "{phrase} {product} - Funny Gift for Dad",
            "Best Dad {phrase} - {product} for Fathers",
        ],
        "fitness": [
            "{phrase} - Gym {product} for Fitness Lovers",
            "{phrase} {product} - Workout Gift for Athletes",
            "Fitness {phrase} - {product} for Gym Enthusiasts",
        ],
        "nurse": [
            "{phrase} - Nurse {product} for Healthcare Workers",
            "{phrase} {product} - Gift for Nurses",
            "Nursing {phrase} - Funny {product} for RN LPN",
        ],
        "teacher": [
            "{phrase} - Teacher {product} for Educators",
            "{phrase} {product} - Gift for Teachers",
            "Teaching {phrase} - {product} for School Staff",
        ],
    }

    # Adjectives by tone
    ADJECTIVES = {
        "funny": ["Funny", "Hilarious", "Humorous", "Witty", "Sarcastic", "Silly"],
        "wholesome": ["Sweet", "Loving", "Heartfelt", "Adorable", "Cute", "Lovely"],
        "motivational": ["Inspirational", "Motivational", "Empowering", "Uplifting"],
        "cool": ["Cool", "Awesome", "Epic", "Badass", "Unique", "Trendy"],
        "vintage": ["Vintage", "Retro", "Classic", "Old School", "Throwback"],
    }

    # Audience segments
    AUDIENCES = {
        "general": ["Men", "Women", "Adults", "Teens", "Everyone"],
        "family": ["Mom", "Dad", "Grandma", "Grandpa", "Sister", "Brother", "Aunt", "Uncle"],
        "profession": ["Nurses", "Teachers", "Doctors", "Engineers", "Developers"],
        "hobby": ["Coffee Lovers", "Dog Owners", "Cat Lovers", "Gamers", "Fitness Enthusiasts"],
    }

    # Product types
    PRODUCTS = [
        "T-Shirt", "Tee", "Shirt", "Tank Top", "Hoodie", "Sweatshirt",
        "Long Sleeve", "V-Neck", "Raglan", "Premium Tee"
    ]

    # Occasions
    OCCASIONS = [
        "Birthday", "Christmas", "Holiday", "Mother's Day", "Father's Day",
        "Valentine's Day", "Anniversary", "Graduation", "Thank You",
    ]

    # Bullet point templates
    BULLET_TEMPLATES = [
        "Perfect {occasion} gift for {audience} who {activity}",
        "Great for anyone who loves {topic} and {related}",
        "Makes a {adjective} present for {occasion} or any special day",
        "Ideal for {audience} who appreciate {style} humor",
        "Lightweight, classic fit, double-needle sleeve and bottom hem",
    ]

    def generate_title(
        self,
        phrase: str,
        niche: str = "general",
        product: str = "T-Shirt",
        tone: str = "funny",
    ) -> Dict[str, Any]:
        """Generate an optimized title for Amazon Merch."""
        templates = self.TITLE_TEMPLATES.get(niche, self.TITLE_TEMPLATES["general"])
        template = random.choice(templates)

        adjectives = self.ADJECTIVES.get(tone, self.ADJECTIVES["funny"])
        audiences = self.AUDIENCES.get("general", ["Adults"])

        # Generate primary title
        title = template.format(
            phrase=phrase,
            product=product,
            adjective=random.choice(adjectives),
            audience=random.choice(audiences),
            occasion=random.choice(self.OCCASIONS),
        )

        # Ensure title is under 60 characters for Amazon
        if len(title) > 60:
            title = f"{phrase} - {random.choice(adjectives)} {product}"

        # Generate alternatives
        alternatives = []
        for _ in range(3):
            alt_template = random.choice(templates)
            alt = alt_template.format(
                phrase=phrase,
                product=random.choice(self.PRODUCTS),
                adjective=random.choice(adjectives),
                audience=random.choice(audiences),
                occasion=random.choice(self.OCCASIONS),
            )
            if len(alt) <= 60 and alt != title:
                alternatives.append(alt)

        return {
            "primary": title,
            "character_count": len(title),
            "within_limit": len(title) <= 60,
            "alternatives": alternatives[:3],
            "seo_score": self._calculate_seo_score(title, phrase),
        }

    def generate_bullets(
        self,
        phrase: str,
        niche: str = "general",
        tone: str = "funny",
        count: int = 2,
    ) -> List[Dict[str, Any]]:
        """Generate bullet points for Amazon listing."""
        bullets = []

        adjectives = self.ADJECTIVES.get(tone, self.ADJECTIVES["funny"])
        audiences = self._get_audiences_for_niche(niche)

        # First bullet - gift suggestion
        bullet1 = f"Perfect gift for {random.choice(audiences)} who love {niche} - great for birthdays, holidays, or any occasion"
        bullets.append({
            "text": bullet1,
            "character_count": len(bullet1),
            "focus": "gift_occasion",
        })

        # Second bullet - product quality
        bullet2 = "Lightweight, classic fit, double-needle sleeve and bottom hem"
        bullets.append({
            "text": bullet2,
            "character_count": len(bullet2),
            "focus": "product_quality",
        })

        return bullets[:count]

    def generate_keywords(
        self,
        phrase: str,
        niche: str = "general",
        max_bytes: int = 250,
    ) -> Dict[str, Any]:
        """Generate backend keywords for Amazon."""
        keywords = []

        # Add phrase words
        phrase_words = phrase.lower().replace("-", " ").split()
        keywords.extend(phrase_words)

        # Add niche keywords
        niche_keywords = self._get_niche_keywords(niche)
        keywords.extend(niche_keywords)

        # Add general product keywords
        general = [
            "funny", "shirt", "tshirt", "gift", "present", "humor",
            "sarcastic", "trendy", "cool", "unique", "novelty",
        ]
        keywords.extend(general)

        # Add occasion keywords
        occasion_keywords = [
            "birthday", "christmas", "holiday", "gift idea",
            "mothers day", "fathers day", "valentines",
        ]
        keywords.extend(occasion_keywords)

        # Deduplicate and join
        unique = list(dict.fromkeys(keywords))

        # Build keyword string under byte limit
        keyword_string = ""
        for kw in unique:
            test = f"{keyword_string} {kw}".strip()
            if len(test.encode('utf-8')) <= max_bytes:
                keyword_string = test
            else:
                break

        return {
            "keywords": keyword_string,
            "byte_count": len(keyword_string.encode('utf-8')),
            "within_limit": len(keyword_string.encode('utf-8')) <= max_bytes,
            "word_count": len(keyword_string.split()),
            "all_keywords": unique,
        }

    def generate_full_listing(
        self,
        phrase: str,
        niche: str = "general",
        product: str = "T-Shirt",
        tone: str = "funny",
    ) -> Dict[str, Any]:
        """Generate a complete optimized listing."""
        return {
            "phrase": phrase,
            "niche": niche,
            "product": product,
            "title": self.generate_title(phrase, niche, product, tone),
            "bullets": self.generate_bullets(phrase, niche, tone),
            "keywords": self.generate_keywords(phrase, niche),
            "tips": self._get_listing_tips(phrase, niche),
        }

    def _get_niche_keywords(self, niche: str) -> List[str]:
        """Get keywords specific to a niche."""
        niche_kw = {
            "coffee": ["coffee", "caffeine", "espresso", "latte", "coffee lover", "barista", "coffee addict"],
            "dogs": ["dog", "puppy", "dog mom", "dog dad", "dog lover", "fur baby", "pet owner"],
            "cats": ["cat", "kitten", "cat mom", "cat dad", "cat lover", "fur baby", "crazy cat"],
            "fitness": ["gym", "workout", "fitness", "exercise", "lifting", "athlete", "gains"],
            "mom": ["mom", "mother", "mama", "mommy", "mothers day", "mom life", "boy mom", "girl mom"],
            "dad": ["dad", "father", "daddy", "papa", "fathers day", "dad life", "dad jokes"],
            "nurse": ["nurse", "nursing", "rn", "lpn", "healthcare", "medical", "hospital"],
            "teacher": ["teacher", "teaching", "educator", "school", "classroom", "education"],
            "gaming": ["gaming", "gamer", "video games", "controller", "level up", "respawn"],
            "beer": ["beer", "craft beer", "brewing", "hops", "ale", "lager", "beer lover"],
            "wine": ["wine", "vino", "wine lover", "sommelier", "winery", "wine mom"],
        }
        return niche_kw.get(niche.lower(), [niche])

    def _get_audiences_for_niche(self, niche: str) -> List[str]:
        """Get relevant audiences for a niche."""
        niche_audiences = {
            "coffee": ["coffee lovers", "caffeine addicts", "baristas", "morning people"],
            "dogs": ["dog moms", "dog dads", "dog owners", "pet lovers"],
            "cats": ["cat moms", "cat dads", "cat owners", "cat lovers"],
            "fitness": ["gym enthusiasts", "fitness lovers", "athletes", "workout warriors"],
            "mom": ["moms", "mothers", "mama bears", "new moms", "tired moms"],
            "dad": ["dads", "fathers", "new dads", "dad joke lovers"],
            "nurse": ["nurses", "RNs", "LPNs", "healthcare workers", "medical staff"],
            "teacher": ["teachers", "educators", "professors", "school staff"],
        }
        return niche_audiences.get(niche.lower(), ["men", "women", "adults"])

    def _calculate_seo_score(self, title: str, phrase: str) -> int:
        """Calculate SEO optimization score for a title."""
        score = 50

        # Phrase included
        if phrase.lower() in title.lower():
            score += 20

        # Length check (optimal 40-60 chars)
        if 40 <= len(title) <= 60:
            score += 15
        elif len(title) < 40:
            score += 10

        # Contains product type
        if any(p.lower() in title.lower() for p in self.PRODUCTS):
            score += 10

        # Contains gift/occasion word
        if any(w in title.lower() for w in ["gift", "present", "birthday", "holiday"]):
            score += 5

        return min(score, 100)

    def _get_listing_tips(self, phrase: str, niche: str) -> List[str]:
        """Get optimization tips for the listing."""
        tips = [
            "Use all 2 bullet points allowed on Amazon Merch",
            "Include your main phrase at the start of the title",
            "Add relevant occasions (birthday, Christmas) for seasonal search traffic",
        ]

        if len(phrase) > 25:
            tips.append("Consider shortening the phrase for better title fit")

        if niche != "general":
            tips.append(f"Target {niche}-specific keywords in your backend search terms")

        return tips


# Singleton instance
listing_optimizer = ListingOptimizer()

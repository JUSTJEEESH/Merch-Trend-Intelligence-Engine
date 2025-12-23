"""Amazon Merch SEO listing generator - Human-sounding, compliant, publishable."""
import re
import random
from typing import Dict, Any, List, Optional


class SEOGenerator:
    """
    Generate Amazon Merch listings that sound like real human sellers.

    PRIORITIES:
    1. Amazon compliance (no rejections)
    2. Natural, readable language
    3. Buyer search intent
    4. Meaning and attitude over design description

    DO NOT:
    - Describe fonts, typography, spacing, or layout
    - Sound like a graphic design analysis
    - Use promotional language
    - Mention gifts, occasions, or special uses
    """

    # Words/phrases that will get listings REJECTED
    FORBIDDEN_TERMS = [
        # Promotional/Marketing
        "gift", "present", "perfect for", "great for", "ideal for",
        "best seller", "bestseller", "top rated", "#1", "number one",
        "must have", "must-have", "limited edition", "exclusive",
        "sale", "discount", "deal", "cheap", "affordable", "bargain",
        "free shipping", "prime", "amazon",

        # Occasions (unrelated to design)
        "birthday", "christmas", "holiday", "mother's day", "father's day",
        "valentine", "anniversary", "graduation", "wedding", "baby shower",
        "thanksgiving", "easter", "halloween", "new year",

        # Textures/Materials (misleading)
        "glitter", "sparkle", "metallic", "foil", "gold", "silver",
        "neon", "glow", "glow in dark", "holographic", "embossed",
        "leather", "wood", "marble", "diamond", "sequin", "velvet",

        # Product/Quality Claims
        "high quality", "premium", "soft", "comfortable", "lightweight",
        "breathable", "cotton", "polyester", "fabric",
        "t-shirt", "tshirt", "shirt", "tee", "hoodie", "sweatshirt",

        # Typography/Design (sounds robotic - AVOID)
        "typography", "font", "lettering", "typeface", "bold text",
        "script font", "hand-drawn", "graphic design", "artwork",
        "visual composition", "text arrangement", "design elements",
        "motif", "illustration", "graphic",
    ]

    # Character limits per Amazon's requirements
    LIMITS = {
        "title": 60,
        "brand": 50,
        "bullet_1": 256,
        "bullet_2": 256,
        "description_min": 75,
        "description_max": 2000,
        "keywords": 250,
    }

    # Attitude/vibe descriptors by tone
    TONE_VIBES = {
        "funny": ["humor", "laughs", "wit", "comedy"],
        "sarcastic": ["sarcasm", "dry wit", "irony", "sass"],
        "motivational": ["motivation", "drive", "ambition", "hustle"],
        "wholesome": ["positivity", "warmth", "good vibes"],
        "edgy": ["attitude", "edge", "boldness"],
        "proud": ["pride", "confidence", "self-expression"],
        "relatable": ["real talk", "honesty", "everyday life"],
        "aesthetic": ["vibe", "mood", "energy"],
    }

    # Audience descriptors by niche
    NICHE_AUDIENCES = {
        "coffee": {
            "people": ["coffee lovers", "caffeine addicts", "morning people"],
            "contexts": ["before the first cup", "the daily grind", "caffeine dependency"],
            "mindsets": ["need coffee to function", "coffee is life", "don't talk before coffee"],
        },
        "dogs": {
            "people": ["dog owners", "dog parents", "pet lovers"],
            "contexts": ["life with dogs", "the dog parent life", "four-legged family"],
            "mindsets": ["dogs over people", "my dog is family", "rescue parent"],
        },
        "cats": {
            "people": ["cat owners", "cat lovers", "cat parents"],
            "contexts": ["life with cats", "feline chaos", "cat parent struggles"],
            "mindsets": ["cats rule", "proud cat person", "crazy cat energy"],
        },
        "fitness": {
            "people": ["gym goers", "fitness enthusiasts", "workout warriors"],
            "contexts": ["gym life", "the daily grind", "leg day"],
            "mindsets": ["no excuses", "earn it", "discipline over motivation"],
        },
        "nursing": {
            "people": ["nurses", "healthcare workers", "RNs"],
            "contexts": ["long shifts", "hospital life", "saving lives"],
            "mindsets": ["nurses run on caffeine", "night shift survivor", "scrub life"],
        },
        "teaching": {
            "people": ["teachers", "educators", "classroom warriors"],
            "contexts": ["classroom chaos", "lesson planning", "parent emails"],
            "mindsets": ["teachers change lives", "summer countdown", "coffee and patience"],
        },
        "mom": {
            "people": ["moms", "mothers", "mama bears"],
            "contexts": ["mom life", "parenting chaos", "tiny humans"],
            "mindsets": ["mom mode", "tired but blessed", "chaos coordinator"],
        },
        "dad": {
            "people": ["dads", "fathers", "dad joke enthusiasts"],
            "contexts": ["dad life", "fatherhood", "raising kids"],
            "mindsets": ["dad jokes", "grill master", "fix-it mentality"],
        },
        "gaming": {
            "people": ["gamers", "players", "gaming enthusiasts"],
            "contexts": ["gaming sessions", "respawn life", "rage quit moments"],
            "mindsets": ["one more game", "sleep is optional", "controller life"],
        },
        "introvert": {
            "people": ["introverts", "homebodies", "quiet ones"],
            "contexts": ["staying in", "social battery drained", "alone time"],
            "mindsets": ["peopled out", "recharging", "antisocial butterfly"],
        },
        "sarcasm": {
            "people": ["sarcastic souls", "witty minds", "dry humor fans"],
            "contexts": ["everyday annoyances", "unfiltered thoughts", "real talk"],
            "mindsets": ["fluent in sarcasm", "professionally petty", "allergic to stupidity"],
        },
        "work": {
            "people": ["office workers", "9-to-5ers", "remote workers"],
            "contexts": ["work life", "meeting fatigue", "email overload"],
            "mindsets": ["surviving meetings", "living for the weekend", "Friday countdown"],
        },
        "beer": {
            "people": ["beer lovers", "craft beer fans", "brew enthusiasts"],
            "contexts": ["happy hour", "weekend vibes", "cold ones"],
            "mindsets": ["beer o'clock", "hoppy thoughts", "brewery hopper"],
        },
        "wine": {
            "people": ["wine lovers", "wine enthusiasts", "vino fans"],
            "contexts": ["wine time", "unwinding", "pour decisions"],
            "mindsets": ["wine not", "sip happens", "wine is the answer"],
        },
        "fishing": {
            "people": ["anglers", "fishermen", "fishing enthusiasts"],
            "contexts": ["on the water", "early mornings", "the big catch"],
            "mindsets": ["hooked on fishing", "reel therapy", "tight lines life"],
        },
        "hunting": {
            "people": ["hunters", "outdoorsmen", "wildlife enthusiasts"],
            "contexts": ["hunting season", "the great outdoors", "early mornings"],
            "mindsets": ["hunt life", "outdoor soul", "buck fever"],
        },
        "anxiety": {
            "people": ["anxious minds", "overthinkers", "worry warriors"],
            "contexts": ["the struggle", "mental health journey", "daily battles"],
            "mindsets": ["anxious but trying", "one day at a time", "it's okay to not be okay"],
        },
    }

    GENERIC_AUDIENCE = {
        "people": ["people who get it", "like-minded individuals", "those who relate"],
        "contexts": ["everyday life", "real moments", "honest expression"],
        "mindsets": ["keeping it real", "saying what you mean", "no filter needed"],
    }

    # Brand name templates (short, neutral, scalable)
    BRAND_TEMPLATES = [
        "Statement Co",
        "Real Talk Prints",
        "Vibe Check",
        "Mood Apparel",
        "Say It Loud",
        "Attitude Wear",
        "No Filter Tees",
        "Honest Threads",
        "Word Up",
        "Express Wear",
    ]

    def generate(
        self,
        phrase: str,
        niche: Optional[str] = None,
        style: str = "funny"
    ) -> Dict[str, Any]:
        """
        Generate a complete, compliant, publishable Amazon Merch listing.

        Returns dict with title, brand, bullet_1, bullet_2, description, keywords.
        All content focuses on MEANING and ATTITUDE, not design description.
        """
        audience = self._get_audience(niche)
        vibes = self.TONE_VIBES.get(style, self.TONE_VIBES["funny"])

        result = {
            "phrase": phrase,
            "niche": niche or "general",
            "style": style,
            "title": self._generate_title(phrase, style, niche),
            "brand": self._generate_brand(),
            "bullet_1": self._generate_bullet_1(phrase, style, vibes),
            "bullet_2": self._generate_bullet_2(phrase, audience),
            "description": self._generate_description(phrase, style, audience, vibes),
            "keywords": self._generate_keywords(phrase, niche, audience),
            "validation": {},
        }

        result["validation"] = self._validate_all(result)
        return result

    def _get_audience(self, niche: Optional[str]) -> Dict:
        """Get audience info for the niche."""
        if niche and niche.lower() in self.NICHE_AUDIENCES:
            return self.NICHE_AUDIENCES[niche.lower()]
        return self.GENERIC_AUDIENCE

    def _generate_title(self, phrase: str, style: str, niche: Optional[str]) -> Dict[str, Any]:
        """
        Generate title (60 chars MAX).
        Lead with phrase, add 1-2 relevant modifiers.
        """
        clean_phrase = phrase.strip()

        # Style modifiers
        style_mods = {
            "funny": ["Funny", "Humor", "Hilarious"],
            "sarcastic": ["Sarcastic", "Sassy", "Witty"],
            "motivational": ["Motivational", "Inspiring"],
            "wholesome": ["Positive", "Uplifting"],
            "edgy": ["Bold", "Edgy"],
            "proud": ["Proud"],
            "relatable": ["Relatable", "Real"],
            "aesthetic": ["Aesthetic", "Vibe"],
        }

        mod = random.choice(style_mods.get(style, ["Funny"]))

        # Niche modifiers
        niche_mods = {
            "coffee": "Coffee Lover",
            "dogs": "Dog Owner",
            "cats": "Cat Person",
            "fitness": "Gym",
            "nursing": "Nurse",
            "teaching": "Teacher",
            "mom": "Mom",
            "dad": "Dad",
            "gaming": "Gamer",
            "work": "Office",
            "beer": "Beer Lover",
            "wine": "Wine Lover",
            "fishing": "Fishing",
            "hunting": "Hunting",
            "introvert": "Introvert",
            "sarcasm": "Sarcastic",
            "anxiety": "Anxiety",
        }

        niche_mod = niche_mods.get(niche, "") if niche else ""

        # Build title options
        options = []

        if niche_mod:
            options.append(f"{clean_phrase} - {mod} {niche_mod}")
            options.append(f"{clean_phrase} {mod} {niche_mod}")

        options.append(f"{clean_phrase} - {mod} Saying")
        options.append(f"{clean_phrase} {mod} Quote")
        options.append(f"{clean_phrase}")

        # Find first that fits
        for title in options:
            if len(title) <= self.LIMITS["title"]:
                return {
                    "text": title,
                    "length": len(title),
                    "limit": self.LIMITS["title"],
                    "compliant": True,
                }

        # Truncate if needed
        truncated = clean_phrase[:self.LIMITS["title"]]
        return {
            "text": truncated,
            "length": len(truncated),
            "limit": self.LIMITS["title"],
            "compliant": True,
        }

    def _generate_brand(self) -> Dict[str, Any]:
        """Generate short, neutral brand name."""
        brand = random.choice(self.BRAND_TEMPLATES)
        return {
            "text": brand,
            "length": len(brand),
            "limit": self.LIMITS["brand"],
            "compliant": True,
        }

    def _generate_bullet_1(self, phrase: str, style: str, vibes: List[str]) -> Dict[str, Any]:
        """
        Bullet 1: Meaning / attitude / vibe of the phrase.
        Focus on what it MEANS, not how it looks.
        """
        vibe = random.choice(vibes)
        clean = phrase.strip()

        templates = [
            f'"{clean}" — because sometimes you just have to say it. This is for anyone who appreciates a little {vibe} and isn\'t afraid to show it.',
            f'"{clean}" says it all. Pure, unfiltered {vibe} for those who get it.',
            f'Some things just need to be said out loud. "{clean}" is that energy — honest, real, and full of {vibe}.',
            f'"{clean}" — when words perfectly capture what you\'re feeling. It\'s that {vibe} we all need sometimes.',
            f'This says what everyone\'s thinking. "{clean}" is {vibe} in its purest form.',
        ]

        bullet = random.choice(templates)

        if len(bullet) > self.LIMITS["bullet_1"]:
            bullet = bullet[:self.LIMITS["bullet_1"] - 3] + "..."

        return {
            "text": bullet,
            "length": len(bullet),
            "limit": self.LIMITS["bullet_1"],
            "compliant": len(bullet) <= self.LIMITS["bullet_1"],
        }

    def _generate_bullet_2(self, phrase: str, audience: Dict) -> Dict[str, Any]:
        """
        Bullet 2: Who relates to it (job, lifestyle, personality, mindset).
        NO "perfect for" or promotional framing.
        """
        people = random.choice(audience["people"])
        mindset = random.choice(audience["mindsets"])
        context = random.choice(audience["contexts"])

        templates = [
            f"If you know, you know. {people.capitalize()} who live that {mindset} life will instantly get this.",
            f"Made for {people} who understand {context}. It's not just words — it's a whole mood.",
            f"{people.capitalize()} get it. This is {context} summed up perfectly.",
            f"Real recognizes real. {people.capitalize()} living that {mindset} lifestyle know exactly what this means.",
            f"This one's for the {people}. If {context} is your reality, you'll relate.",
        ]

        bullet = random.choice(templates)

        if len(bullet) > self.LIMITS["bullet_2"]:
            bullet = bullet[:self.LIMITS["bullet_2"] - 3] + "..."

        return {
            "text": bullet,
            "length": len(bullet),
            "limit": self.LIMITS["bullet_2"],
            "compliant": len(bullet) <= self.LIMITS["bullet_2"],
        }

    def _generate_description(
        self,
        phrase: str,
        style: str,
        audience: Dict,
        vibes: List[str]
    ) -> Dict[str, Any]:
        """
        Description (75-2000 chars).
        Expand on meaning and tone. Explain why people connect.
        Sound like a real seller, not a design analyzer.
        """
        clean = phrase.strip()
        vibe = random.choice(vibes)
        people = random.choice(audience["people"])
        mindset = random.choice(audience["mindsets"])
        context = random.choice(audience["contexts"])

        descriptions = [
            f'''"{clean}"

We've all been there. That moment when {context} hits and you just need to express yourself. This captures that feeling perfectly.

{people.capitalize()} will instantly get it. There's something satisfying about wearing something that says exactly what you're thinking. No filter, no apologies — just pure {vibe}.

Whether you say it out loud or let your clothes do the talking, this one speaks volumes. It's that {mindset} energy that connects people who just get it.''',

            f'''"{clean}" — some things don't need explaining.

If you've ever felt that {mindset} vibe, you already know. This is for {people} who aren't afraid to express what they're really thinking.

{context.capitalize()} is real, and sometimes you need a way to show it. That's what this is about — {vibe} that resonates, a message that lands.

Wear it when you mean it. The right people will get it.''',

            f'''"{clean}"

Words that just hit different. If you're one of those {people} who lives {context}, this probably made you smile — or at least nod.

There's a reason some phrases just stick. They capture something real, something relatable. This is that {vibe} energy.

It's not trying too hard. It doesn't overthink it. It just says what needs to be said. {mindset.capitalize()} is a way of life, and this fits right in.''',
        ]

        description = random.choice(descriptions)

        # Ensure within limits
        if len(description) < self.LIMITS["description_min"]:
            description += f"\n\n{people.capitalize()} everywhere relate to this."

        if len(description) > self.LIMITS["description_max"]:
            description = description[:self.LIMITS["description_max"] - 3] + "..."

        compliant = self.LIMITS["description_min"] <= len(description) <= self.LIMITS["description_max"]

        return {
            "text": description,
            "length": len(description),
            "limit_min": self.LIMITS["description_min"],
            "limit_max": self.LIMITS["description_max"],
            "compliant": compliant,
        }

    def _generate_keywords(self, phrase: str, niche: Optional[str], audience: Dict) -> Dict[str, Any]:
        """
        Backend keywords (250 bytes MAX).
        Natural keyword coverage, not stuffing.
        """
        keywords = set()

        # Add phrase words (cleaned)
        for word in phrase.lower().split():
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word and len(clean_word) > 2 and not self._is_forbidden(clean_word):
                keywords.add(clean_word)

        # Add niche keywords
        if niche:
            keywords.add(niche.lower())

        # Add audience-related keywords
        for person in audience.get("people", []):
            for word in person.lower().split():
                clean = re.sub(r'[^\w]', '', word)
                if clean and len(clean) > 2 and not self._is_forbidden(clean):
                    keywords.add(clean)

        # Add general search terms
        general_terms = [
            "funny", "saying", "quote", "humor", "sarcastic",
            "attitude", "statement", "relatable", "mood", "vibe"
        ]

        for term in general_terms:
            if not self._is_forbidden(term):
                keywords.add(term)

        # Build string within byte limit
        result = ""
        for kw in list(keywords):
            test = f"{result} {kw}".strip()
            if len(test.encode('utf-8')) <= self.LIMITS["keywords"]:
                result = test
            else:
                break

        byte_count = len(result.encode('utf-8'))
        return {
            "text": result,
            "byte_count": byte_count,
            "limit": self.LIMITS["keywords"],
            "compliant": byte_count <= self.LIMITS["keywords"],
        }

    def _is_forbidden(self, word: str) -> bool:
        """Check if a word is forbidden."""
        word_lower = word.lower()
        for term in self.FORBIDDEN_TERMS:
            if term.lower() == word_lower or term.lower() in word_lower:
                return True
        return False

    def _validate_all(self, result: Dict) -> Dict[str, Any]:
        """Validate the entire listing."""
        issues = []

        # Check limits
        if result["title"]["length"] > self.LIMITS["title"]:
            issues.append(f"Title exceeds {self.LIMITS['title']} chars")

        if result["brand"]["length"] > self.LIMITS["brand"]:
            issues.append(f"Brand exceeds {self.LIMITS['brand']} chars")

        if result["bullet_1"]["length"] > self.LIMITS["bullet_1"]:
            issues.append(f"Bullet 1 exceeds {self.LIMITS['bullet_1']} chars")

        if result["bullet_2"]["length"] > self.LIMITS["bullet_2"]:
            issues.append(f"Bullet 2 exceeds {self.LIMITS['bullet_2']} chars")

        desc_len = result["description"]["length"]
        if desc_len < self.LIMITS["description_min"]:
            issues.append(f"Description below {self.LIMITS['description_min']} chars")
        if desc_len > self.LIMITS["description_max"]:
            issues.append(f"Description exceeds {self.LIMITS['description_max']} chars")

        if result["keywords"]["byte_count"] > self.LIMITS["keywords"]:
            issues.append(f"Keywords exceed {self.LIMITS['keywords']} bytes")

        # Check for forbidden terms
        all_text = " ".join([
            result["title"]["text"],
            result["brand"]["text"],
            result["bullet_1"]["text"],
            result["bullet_2"]["text"],
            result["description"]["text"],
        ]).lower()

        for term in self.FORBIDDEN_TERMS:
            if f" {term.lower()} " in f" {all_text} ":
                issues.append(f"Contains forbidden term: '{term}'")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "checks_passed": 7 - min(len(issues), 7),
            "total_checks": 7,
        }

    def get_forbidden_terms(self) -> List[str]:
        """Return list of forbidden terms."""
        return self.FORBIDDEN_TERMS

    def get_limits(self) -> Dict[str, int]:
        """Return character/byte limits."""
        return self.LIMITS

    def get_available_niches(self) -> List[str]:
        """Return list of niches with audience data."""
        return sorted(self.NICHE_AUDIENCES.keys())

    def get_available_styles(self) -> List[str]:
        """Return list of available tones/styles."""
        return list(self.TONE_VIBES.keys())

    def validate_listing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None,
        backend_keywords: str = None
    ) -> Dict[str, Any]:
        """Validate existing listing content against Amazon rules."""
        issues = []

        if title and len(title) > self.LIMITS["title"]:
            issues.append(f"Title exceeds {self.LIMITS['title']} chars")

        if bullet_1 and len(bullet_1) > self.LIMITS["bullet_1"]:
            issues.append(f"Bullet 1 exceeds {self.LIMITS['bullet_1']} chars")

        if bullet_2 and len(bullet_2) > self.LIMITS["bullet_2"]:
            issues.append(f"Bullet 2 exceeds {self.LIMITS['bullet_2']} chars")

        if description:
            if len(description) < self.LIMITS["description_min"]:
                issues.append(f"Description below {self.LIMITS['description_min']} chars")
            if len(description) > self.LIMITS["description_max"]:
                issues.append(f"Description exceeds {self.LIMITS['description_max']} chars")

        if backend_keywords:
            byte_count = len(backend_keywords.encode('utf-8'))
            if byte_count > self.LIMITS["keywords"]:
                issues.append(f"Keywords exceed {self.LIMITS['keywords']} bytes")

        # Check forbidden terms
        all_text = " ".join(filter(None, [title, bullet_1, bullet_2, description])).lower()
        for term in self.FORBIDDEN_TERMS:
            if term.lower() in all_text:
                issues.append(f"Contains forbidden term: '{term}'")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "checks_performed": 5,
        }


# Singleton instance
seo_generator = SEOGenerator()

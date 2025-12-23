"""Amazon Merch SEO listing generator - Fully TOS compliant, design-focused only."""
import re
import random
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SEOGenerator:
    """
    Generate Amazon Merch listings that are 100% TOS compliant.

    AMAZON RULES ENFORCED:
    - NO promotional phrases (gift, perfect for, best seller, etc.)
    - NO product quality claims (lightweight, soft, comfortable)
    - NO special effects claims (glitter, metallic, glow)
    - NO texture claims (leather, wood, marble)
    - NO suggested use (birthday, Christmas, etc.)
    - Content must ONLY describe the design itself
    """

    # Words/phrases FORBIDDEN by Amazon - will cause rejection
    FORBIDDEN_TERMS = [
        # Promotional/Marketing (STRICTLY FORBIDDEN)
        "gift", "present", "perfect for", "great for", "ideal for",
        "best seller", "bestseller", "top rated", "#1", "number one",
        "popular", "trending", "hot", "new", "exclusive", "limited edition",
        "sale", "discount", "deal", "cheap", "affordable", "bargain",
        "free shipping", "fast shipping", "prime", "amazon",

        # Suggested Use/Occasions (FORBIDDEN - unrelated to design)
        "birthday", "christmas", "holiday", "mother's day", "father's day",
        "valentine", "anniversary", "graduation", "wedding", "baby shower",
        "thanksgiving", "easter", "halloween", "new year",

        # Quality Claims (FORBIDDEN - not about design)
        "high quality", "premium quality", "best quality", "top quality",
        "100%", "guaranteed", "authentic", "genuine", "official",
        "durable", "long lasting", "comfortable", "soft", "lightweight",
        "breathable", "stretchy", "fitted", "relaxed fit", "slim fit",

        # Product Terms (Amazon adds these automatically)
        "t-shirt", "tshirt", "shirt", "tee", "hoodie", "sweatshirt",
        "tank top", "long sleeve", "pullover", "apparel", "clothing",
        "cotton", "polyester", "fabric", "material",

        # Texture Claims (FORBIDDEN - misleading)
        "glitter", "sparkle", "metallic", "foil", "gold", "rose gold",
        "silver", "neon", "glow", "glow in dark", "holographic",
        "sequin", "leather", "wood", "marble", "diamond", "gem",
        "fuzzy", "furry", "velvet", "silk", "satin",

        # Other Violations
        "licensed", "trademarked", "copyright", "patent",
        "free", "bonus", "extra", "limited time",
    ]

    # Character limits per Amazon's requirements
    LIMITS = {
        "title": 60,
        "brand": 50,
        "bullet_1": 256,
        "bullet_2": 256,
        "description_min": 75,
        "description_max": 2000,
        "keywords": 250,  # bytes, not chars
    }

    # Design-focused descriptors by mood/style
    DESIGN_STYLES = {
        "funny": ["humorous", "witty", "clever", "amusing", "comedic"],
        "sarcastic": ["sardonic", "ironic", "dry humor", "satirical", "tongue-in-cheek"],
        "motivational": ["inspiring", "uplifting", "encouraging", "empowering"],
        "cute": ["adorable", "charming", "sweet", "delightful", "endearing"],
        "vintage": ["retro", "classic", "nostalgic", "old-school", "throwback"],
        "bold": ["striking", "eye-catching", "standout", "attention-grabbing"],
        "minimal": ["simple", "clean", "understated", "elegant", "sleek"],
    }

    # Niche-specific design vocabulary (describes the design, not the product)
    NICHE_VOCABULARY = {
        "coffee": {
            "design_elements": ["coffee cup graphic", "steam illustration", "coffee bean motif", "espresso imagery", "barista-themed artwork"],
            "typography": ["bold lettering", "script font", "vintage typography", "hand-drawn text"],
            "themes": ["caffeine culture", "morning routine", "coffee appreciation", "barista life"],
        },
        "dogs": {
            "design_elements": ["paw print graphic", "dog silhouette", "bone motif", "puppy illustration", "canine artwork"],
            "typography": ["playful font", "bold text", "fun lettering"],
            "themes": ["pet ownership", "dog walking", "puppy love", "canine companionship"],
        },
        "cats": {
            "design_elements": ["cat silhouette", "paw print motif", "whisker illustration", "feline graphic"],
            "typography": ["whimsical font", "elegant script", "playful text"],
            "themes": ["cat ownership", "feline behavior", "cat appreciation"],
        },
        "fitness": {
            "design_elements": ["dumbbell graphic", "muscle illustration", "gym equipment motif"],
            "typography": ["bold athletic font", "strong lettering", "impact text"],
            "themes": ["workout culture", "gym lifestyle", "fitness dedication"],
        },
        "nursing": {
            "design_elements": ["medical symbol", "heart monitor graphic", "stethoscope illustration"],
            "typography": ["professional font", "clean text", "modern lettering"],
            "themes": ["healthcare profession", "nursing dedication", "medical field"],
        },
        "teaching": {
            "design_elements": ["apple graphic", "book illustration", "classroom motif", "pencil imagery"],
            "typography": ["chalk-style font", "educational text", "friendly lettering"],
            "themes": ["education profession", "classroom life", "teaching dedication"],
        },
        "mom": {
            "design_elements": ["heart graphic", "family illustration", "decorative text"],
            "typography": ["script font", "elegant lettering", "warm text style"],
            "themes": ["motherhood", "parenting life", "family dynamics"],
        },
        "dad": {
            "design_elements": ["tool graphic", "masculine illustration", "bold imagery"],
            "typography": ["strong font", "bold lettering", "classic text"],
            "themes": ["fatherhood", "dad humor", "parenting life"],
        },
        "gaming": {
            "design_elements": ["controller graphic", "pixel art style", "game-inspired imagery"],
            "typography": ["digital font", "pixel text", "arcade lettering"],
            "themes": ["gamer culture", "video game lifestyle", "gaming humor"],
        },
        "fishing": {
            "design_elements": ["fish graphic", "hook illustration", "rod motif", "water imagery"],
            "typography": ["outdoor font", "rustic text", "natural lettering"],
            "themes": ["angler lifestyle", "fishing culture", "outdoor activity"],
        },
        "hunting": {
            "design_elements": ["deer silhouette", "antler graphic", "outdoor motif"],
            "typography": ["rugged font", "wilderness text", "bold lettering"],
            "themes": ["hunter lifestyle", "outdoor tradition", "wildlife appreciation"],
        },
        "beer": {
            "design_elements": ["hop graphic", "mug illustration", "brewery motif"],
            "typography": ["vintage font", "pub-style text", "bold lettering"],
            "themes": ["craft beer culture", "brewing appreciation", "beer enthusiasm"],
        },
        "wine": {
            "design_elements": ["wine glass graphic", "grape illustration", "vineyard motif"],
            "typography": ["elegant script", "sophisticated font", "refined text"],
            "themes": ["wine appreciation", "vineyard culture", "sommelier lifestyle"],
        },
        "anxiety": {
            "design_elements": ["heart graphic", "brain illustration", "awareness ribbon"],
            "typography": ["gentle font", "supportive text", "warm lettering"],
            "themes": ["mental health awareness", "self-care", "emotional wellbeing"],
        },
        "introvert": {
            "design_elements": ["book graphic", "home illustration", "quiet motif"],
            "typography": ["understated font", "simple text", "minimal lettering"],
            "themes": ["introvert lifestyle", "solitude appreciation", "quiet personality"],
        },
        "sarcasm": {
            "design_elements": ["speech bubble graphic", "bold illustration", "expressive imagery"],
            "typography": ["impactful font", "statement text", "bold lettering"],
            "themes": ["dry humor", "witty commentary", "ironic expression"],
        },
    }

    GENERIC_VOCABULARY = {
        "design_elements": ["bold graphic", "eye-catching illustration", "decorative motif"],
        "typography": ["modern font", "clear text", "stylish lettering"],
        "themes": ["self-expression", "personal style", "unique statement"],
    }

    def generate(
        self,
        phrase: str,
        niche: Optional[str] = None,
        style: str = "funny"
    ) -> Dict[str, Any]:
        """
        Generate a fully TOS-compliant Amazon Merch listing.

        Returns:
            Dict with title, brand, bullet_1, bullet_2, description, keywords
            All content describes the DESIGN ONLY, no promotional language.
        """
        vocab = self._get_vocabulary(niche)
        style_words = self.DESIGN_STYLES.get(style, self.DESIGN_STYLES["funny"])

        result = {
            "phrase": phrase,
            "niche": niche or "general",
            "style": style,
            "title": self._generate_title(phrase, niche),
            "brand": self._generate_brand(niche),
            "bullet_1": self._generate_bullet_1(phrase, vocab, style_words),
            "bullet_2": self._generate_bullet_2(phrase, vocab),
            "description": self._generate_description(phrase, niche, vocab, style_words),
            "keywords": self._generate_keywords(phrase, niche, vocab),
            "validation": {},
        }

        # Validate everything
        result["validation"] = self._validate_all(result)

        return result

    def _get_vocabulary(self, niche: Optional[str]) -> Dict:
        """Get design vocabulary for the niche."""
        if niche and niche.lower() in self.NICHE_VOCABULARY:
            return self.NICHE_VOCABULARY[niche.lower()]
        return self.GENERIC_VOCABULARY

    def _generate_title(self, phrase: str, niche: Optional[str]) -> Dict[str, Any]:
        """
        Generate title (60 chars MAX).

        Format: Describes what the design says/shows.
        NO promotional language, NO product words.
        """
        # Clean the phrase
        clean = self._clean_text(phrase)

        # Build title options - just describe what the design says
        if niche:
            niche_clean = niche.title()
            options = [
                f"{clean} - {niche_clean} Design",
                f"{clean} {niche_clean} Typography",
                f"{niche_clean} Quote - {clean}",
                f"{clean} - {niche_clean} Saying",
                f"{clean}",
            ]
        else:
            options = [
                f"{clean} - Funny Quote Design",
                f"{clean} Typography Art",
                f"{clean} Statement Design",
                f"{clean}",
            ]

        # Find first option that fits
        for option in options:
            if len(option) <= self.LIMITS["title"]:
                return {
                    "text": option,
                    "length": len(option),
                    "limit": self.LIMITS["title"],
                    "compliant": True,
                }

        # Truncate if needed
        truncated = clean[:self.LIMITS["title"] - 3] + "..."
        return {
            "text": truncated,
            "length": len(truncated),
            "limit": self.LIMITS["title"],
            "compliant": True,
        }

    def _generate_brand(self, niche: Optional[str]) -> Dict[str, Any]:
        """
        Generate brand name (50 chars MAX).

        Should be a professional-sounding brand.
        """
        if niche:
            niche_title = niche.title().replace(" ", "")
            brands = [
                f"{niche_title} Quote Designs",
                f"{niche_title} Typography Co",
                f"{niche_title} Statement Art",
                f"Funny {niche_title} Quotes",
                f"{niche_title} Apparel Designs",
            ]
        else:
            brands = [
                "Quote Typography Designs",
                "Statement Art Co",
                "Witty Quote Collection",
                "Bold Statement Designs",
                "Typography Art Studio",
            ]

        # Pick one that fits
        for brand in brands:
            if len(brand) <= self.LIMITS["brand"]:
                return {
                    "text": brand,
                    "length": len(brand),
                    "limit": self.LIMITS["brand"],
                    "compliant": True,
                }

        return {
            "text": "Quote Designs",
            "length": 13,
            "limit": self.LIMITS["brand"],
            "compliant": True,
        }

    def _generate_bullet_1(self, phrase: str, vocab: Dict, style_words: List[str]) -> Dict[str, Any]:
        """
        Generate first bullet point (256 chars MAX).

        Describes WHAT the design shows - the text, style, and visual elements.
        NO promotional language.
        """
        style = random.choice(style_words)
        element = random.choice(vocab["design_elements"])
        typo = random.choice(vocab["typography"])

        bullets = [
            f"This design features the {style} phrase \"{phrase}\" displayed in {typo}. The {element} creates a bold visual statement that expresses personality and attitude.",
            f"Features the saying \"{phrase}\" in {typo} style. This {style} design uses {element} to create an expressive and memorable look.",
            f"Displays \"{phrase}\" with {typo} and {element}. This {style} artwork makes a clear statement about personal style and humor.",
        ]

        # Pick one that fits
        for bullet in bullets:
            clean = self._clean_text(bullet)
            if len(clean) <= self.LIMITS["bullet_1"]:
                return {
                    "text": clean,
                    "length": len(clean),
                    "limit": self.LIMITS["bullet_1"],
                    "compliant": True,
                }

        # Fallback
        fallback = f"This design displays the phrase \"{phrase}\" in a {style} typographic style."
        return {
            "text": fallback[:self.LIMITS["bullet_1"]],
            "length": len(fallback[:self.LIMITS["bullet_1"]]),
            "limit": self.LIMITS["bullet_1"],
            "compliant": True,
        }

    def _generate_bullet_2(self, phrase: str, vocab: Dict) -> Dict[str, Any]:
        """
        Generate second bullet point (256 chars MAX).

        Describes the design theme and who appreciates this type of humor/statement.
        NO promotional language, NO "perfect for [occasion]".
        """
        theme = random.choice(vocab["themes"])

        bullets = [
            f"The design celebrates {theme} through expressive typography. The bold text and visual composition create an attention-grabbing statement piece.",
            f"This artwork represents {theme} with its distinctive lettering style. The design composition emphasizes the message while maintaining visual appeal.",
            f"Celebrates {theme} through creative typography and thoughtful design. The visual elements work together to convey the intended message clearly.",
        ]

        for bullet in bullets:
            clean = self._clean_text(bullet)
            if len(clean) <= self.LIMITS["bullet_2"]:
                return {
                    "text": clean,
                    "length": len(clean),
                    "limit": self.LIMITS["bullet_2"],
                    "compliant": True,
                }

        fallback = f"This design represents {theme} through creative typography and bold visual elements."
        return {
            "text": fallback[:self.LIMITS["bullet_2"]],
            "length": len(fallback[:self.LIMITS["bullet_2"]]),
            "limit": self.LIMITS["bullet_2"],
            "compliant": True,
        }

    def _generate_description(
        self,
        phrase: str,
        niche: Optional[str],
        vocab: Dict,
        style_words: List[str]
    ) -> Dict[str, Any]:
        """
        Generate product description (75-2000 chars).

        Thoroughly describes the design - the text, typography, visual style,
        and theme. NO promotional language, NO suggested uses/occasions.
        """
        style = random.choice(style_words)
        element = random.choice(vocab["design_elements"])
        typo = random.choice(vocab["typography"])
        theme = random.choice(vocab["themes"])
        niche_name = niche.title() if niche else "statement"

        description = f"""This {niche_name} design prominently displays the phrase "{phrase}" as its central element.

Design Details:
The artwork features {typo} that gives the text a distinctive {style} appearance. The {element} adds visual interest and reinforces the overall theme of the design.

Typography and Style:
The lettering has been carefully crafted to maximize readability while conveying the intended tone. The text arrangement creates a balanced composition that draws the eye to the message.

Theme:
This design speaks to {theme}. The visual elements and text work together to express a specific attitude and perspective that resonates with people who appreciate this type of {style} expression.

Visual Composition:
The design uses contrast and spacing effectively to ensure the message stands out. The overall aesthetic is {style} and attention-grabbing while remaining tasteful and wearable."""

        clean = self._clean_text(description)

        # Ensure within limits
        if len(clean) < self.LIMITS["description_min"]:
            # Pad if too short (shouldn't happen with above template)
            clean += " This design makes a clear visual statement."

        if len(clean) > self.LIMITS["description_max"]:
            clean = clean[:self.LIMITS["description_max"] - 3] + "..."

        return {
            "text": clean,
            "length": len(clean),
            "limit_min": self.LIMITS["description_min"],
            "limit_max": self.LIMITS["description_max"],
            "compliant": self.LIMITS["description_min"] <= len(clean) <= self.LIMITS["description_max"],
        }

    def _generate_keywords(self, phrase: str, niche: Optional[str], vocab: Dict) -> Dict[str, Any]:
        """
        Generate backend search terms (250 bytes MAX).

        Keywords should be search terms customers would use.
        NO forbidden terms, NO duplicate words.
        """
        keywords = []
        seen = set()

        # Add phrase words (cleaned)
        phrase_words = phrase.lower().split()
        for word in phrase_words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word and len(clean_word) > 2 and clean_word not in seen:
                if not self._is_forbidden(clean_word):
                    keywords.append(clean_word)
                    seen.add(clean_word)

        # Add niche-related terms
        if niche:
            niche_words = niche.lower().split()
            for word in niche_words:
                if word not in seen and not self._is_forbidden(word):
                    keywords.append(word)
                    seen.add(word)

        # Add theme keywords (cleaned)
        for theme in vocab.get("themes", []):
            for word in theme.lower().split():
                clean_word = re.sub(r'[^\w]', '', word)
                if clean_word and len(clean_word) > 2 and clean_word not in seen:
                    if not self._is_forbidden(clean_word):
                        keywords.append(clean_word)
                        seen.add(clean_word)

        # Add safe generic terms
        safe_terms = ["quote", "saying", "design", "typography", "art", "funny", "humor", "statement"]
        for term in safe_terms:
            if term not in seen and not self._is_forbidden(term):
                keywords.append(term)
                seen.add(term)

        # Build string within byte limit
        result = ""
        for kw in keywords:
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

    def _clean_text(self, text: str) -> str:
        """Remove any forbidden terms from text."""
        result = text
        for term in self.FORBIDDEN_TERMS:
            # Case insensitive replacement
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            result = pattern.sub("", result)

        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()
        return result

    def _is_forbidden(self, word: str) -> bool:
        """Check if a word is forbidden."""
        word_lower = word.lower()
        for term in self.FORBIDDEN_TERMS:
            if term.lower() == word_lower:
                return True
        return False

    def _validate_all(self, result: Dict) -> Dict[str, Any]:
        """Validate the entire listing."""
        issues = []

        # Check title
        if result["title"]["length"] > self.LIMITS["title"]:
            issues.append(f"Title exceeds {self.LIMITS['title']} character limit")

        # Check brand
        if result["brand"]["length"] > self.LIMITS["brand"]:
            issues.append(f"Brand exceeds {self.LIMITS['brand']} character limit")

        # Check bullets
        if result["bullet_1"]["length"] > self.LIMITS["bullet_1"]:
            issues.append(f"Bullet 1 exceeds {self.LIMITS['bullet_1']} character limit")
        if result["bullet_2"]["length"] > self.LIMITS["bullet_2"]:
            issues.append(f"Bullet 2 exceeds {self.LIMITS['bullet_2']} character limit")

        # Check description
        desc_len = result["description"]["length"]
        if desc_len < self.LIMITS["description_min"]:
            issues.append(f"Description below {self.LIMITS['description_min']} character minimum")
        if desc_len > self.LIMITS["description_max"]:
            issues.append(f"Description exceeds {self.LIMITS['description_max']} character limit")

        # Check keywords
        if result["keywords"]["byte_count"] > self.LIMITS["keywords"]:
            issues.append(f"Keywords exceed {self.LIMITS['keywords']} byte limit")

        # Check for forbidden terms in all text
        all_text = " ".join([
            result["title"]["text"],
            result["brand"]["text"],
            result["bullet_1"]["text"],
            result["bullet_2"]["text"],
            result["description"]["text"],
        ]).lower()

        for term in self.FORBIDDEN_TERMS:
            if term.lower() in all_text:
                issues.append(f"Contains forbidden term: '{term}'")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "checks_passed": 7 - len(issues),
            "total_checks": 7,
        }

    def get_forbidden_terms(self) -> List[str]:
        """Return list of forbidden terms."""
        return self.FORBIDDEN_TERMS

    def get_limits(self) -> Dict[str, int]:
        """Return character/byte limits."""
        return self.LIMITS

    def get_available_niches(self) -> List[str]:
        """Return list of niches with vocabulary."""
        return sorted(self.NICHE_VOCABULARY.keys())

    def get_available_styles(self) -> List[str]:
        """Return list of available design styles."""
        return list(self.DESIGN_STYLES.keys())

    def validate_listing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None,
        backend_keywords: str = None
    ) -> Dict[str, Any]:
        """
        Validate existing listing content against Amazon TOS rules.

        Returns validation result with compliance status and issues.
        """
        issues = []

        # Check title
        if title:
            if len(title) > self.LIMITS["title"]:
                issues.append(f"Title exceeds {self.LIMITS['title']} character limit ({len(title)} chars)")
            for term in self.FORBIDDEN_TERMS:
                if term.lower() in title.lower():
                    issues.append(f"Title contains forbidden term: '{term}'")

        # Check bullet 1
        if bullet_1:
            if len(bullet_1) > self.LIMITS["bullet_1"]:
                issues.append(f"Bullet 1 exceeds {self.LIMITS['bullet_1']} character limit ({len(bullet_1)} chars)")
            for term in self.FORBIDDEN_TERMS:
                if term.lower() in bullet_1.lower():
                    issues.append(f"Bullet 1 contains forbidden term: '{term}'")

        # Check bullet 2
        if bullet_2:
            if len(bullet_2) > self.LIMITS["bullet_2"]:
                issues.append(f"Bullet 2 exceeds {self.LIMITS['bullet_2']} character limit ({len(bullet_2)} chars)")
            for term in self.FORBIDDEN_TERMS:
                if term.lower() in bullet_2.lower():
                    issues.append(f"Bullet 2 contains forbidden term: '{term}'")

        # Check description
        if description:
            if len(description) < self.LIMITS["description_min"]:
                issues.append(f"Description below {self.LIMITS['description_min']} character minimum ({len(description)} chars)")
            if len(description) > self.LIMITS["description_max"]:
                issues.append(f"Description exceeds {self.LIMITS['description_max']} character limit ({len(description)} chars)")
            for term in self.FORBIDDEN_TERMS:
                if term.lower() in description.lower():
                    issues.append(f"Description contains forbidden term: '{term}'")

        # Check keywords
        if backend_keywords:
            byte_count = len(backend_keywords.encode('utf-8'))
            if byte_count > self.LIMITS["keywords"]:
                issues.append(f"Keywords exceed {self.LIMITS['keywords']} byte limit ({byte_count} bytes)")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "checks_performed": 5,
        }


# Singleton instance
seo_generator = SEOGenerator()

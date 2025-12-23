"""Phrase variation generator - creates useful merch phrase alternatives."""
import re
import logging
from typing import List, Dict, Any, Optional
import random

logger = logging.getLogger(__name__)


class VariationGenerator:
    """Generate creative variations of phrases for merch ideation."""

    # Common phrase patterns and their variations
    PHRASE_PATTERNS = {
        r"(.+) is my therapy": [
            "{0} is cheaper than therapy",
            "I don't need therapy I need {0}",
            "My therapist says I need more {0}",
            "{0} is my happy place",
            "{0} heals the soul",
            "Forget therapy give me {0}",
        ],
        r"I love (.+)": [
            "{0} is my love language",
            "My heart belongs to {0}",
            "Obsessed with {0}",
            "Can't live without {0}",
            "{0} is life",
            "All I need is {0}",
        ],
        r"I need (.+)": [
            "Fueled by {0}",
            "Powered by {0}",
            "Running on {0}",
            "{0} is not optional",
            "Will work for {0}",
            "{0} please",
        ],
        r"(.+) mom": [
            "{0} mama",
            "Proud {0} mom",
            "{0} mom life",
            "Best {0} mom ever",
            "Living that {0} mom life",
        ],
        r"(.+) dad": [
            "{0} papa",
            "Proud {0} dad",
            "{0} dad life",
            "Best {0} dad ever",
            "Rocking the {0} dad life",
        ],
        r"powered by (.+)": [
            "Runs on {0}",
            "Fueled by {0}",
            "{0} is my fuel",
            "{0} powered",
        ],
    }

    # Word-level synonyms for common merch words
    WORD_SYNONYMS = {
        "love": ["adore", "heart", "live for", "obsessed with"],
        "need": ["require", "must have", "can't live without"],
        "coffee": ["caffeine", "espresso", "java", "brew"],
        "wine": ["vino", "grape juice", "the good stuff"],
        "beer": ["brews", "cold ones", "hops"],
        "tired": ["exhausted", "running on empty", "drained"],
        "happy": ["joyful", "blessed", "content", "thriving"],
        "crazy": ["wild", "chaotic", "unhinged", "feral"],
        "mom": ["mama", "mother", "mommy"],
        "dad": ["papa", "father", "daddy", "pops"],
        "dog": ["pup", "pupper", "fur baby", "doggo"],
        "cat": ["kitty", "feline", "fur baby", "floof"],
        "best": ["greatest", "top", "ultimate"],
        "life": ["existence", "journey", "vibe"],
    }

    # Trending phrase templates (2024 style)
    TRENDING_TEMPLATES = [
        "In my {phrase} era",
        "{phrase} era",
        "{phrase} energy",
        "{phrase} is a mood",
        "{phrase} vibes only",
        "Certified {phrase}",
        "{phrase} mode activated",
        "It's giving {phrase}",
        "{phrase} coded",
        "Living that {phrase} life",
        "{phrase} is my personality",
        "{phrase} but make it fashion",
        "Main character {phrase}",
        "{phrase} enthusiast",
        "Professional {phrase}",
        "Currently obsessed with {phrase}",
    ]

    def __init__(self):
        self.nlp = None
        self._init_nlp()

    def _init_nlp(self):
        """Initialize spaCy for POS tagging."""
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            logger.warning(f"spaCy not available: {e}")

    def generate(
        self,
        phrase: str,
        variation_type: str = "all",
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """Generate creative variations of a phrase."""
        variations = []
        phrase_clean = phrase.strip()

        # Try pattern-based variations first
        variations.extend(self._generate_pattern_variations(phrase_clean))

        # Add trending-style variations using the FULL phrase
        variations.extend(self._generate_trending_variations(phrase_clean))

        # Add word-swap variations only if we have known synonyms
        variations.extend(self._generate_word_swap_variations(phrase_clean))

        # Add structural variations
        variations.extend(self._generate_structural_variations(phrase_clean))

        # Deduplicate and clean
        seen = set()
        unique_variations = []
        original_lower = phrase_clean.lower()

        for var in variations:
            text = var["text"].strip()
            normalized = text.lower()

            # Skip if same as original or already seen
            if normalized == original_lower or normalized in seen:
                continue

            # Skip very short results
            if len(text) < 5:
                continue

            seen.add(normalized)
            var["text"] = self._clean_text(text)
            unique_variations.append(var)

        return unique_variations[:count]

    def _generate_pattern_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations based on known phrase patterns."""
        variations = []
        phrase_lower = phrase.lower()

        for pattern, templates in self.PHRASE_PATTERNS.items():
            match = re.match(pattern, phrase_lower, re.IGNORECASE)
            if match:
                groups = match.groups()
                for template in templates:
                    try:
                        new_phrase = template
                        for i, group in enumerate(groups):
                            if group:
                                new_phrase = new_phrase.replace(f"{{{i}}}", group)

                        if new_phrase != template:
                            variations.append({
                                "text": new_phrase.capitalize(),
                                "type": "pattern",
                            })
                    except Exception:
                        continue

        return variations

    def _generate_trending_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate trending-style variations using the FULL phrase."""
        variations = []
        phrase_lower = phrase.lower()

        # Use the full phrase in trending templates
        for template in self.TRENDING_TEMPLATES:
            try:
                new_phrase = template.format(phrase=phrase_lower)
                # Don't duplicate if phrase is already in that format
                if new_phrase.lower() != phrase_lower:
                    variations.append({
                        "text": new_phrase.title(),
                        "type": "trending",
                    })
            except Exception:
                continue

        return variations[:8]  # Limit trending variations

    def _generate_word_swap_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations by swapping words with synonyms."""
        variations = []
        words = phrase.lower().split()

        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word)

            # Only swap if we have a known synonym
            if clean_word in self.WORD_SYNONYMS:
                for synonym in self.WORD_SYNONYMS[clean_word][:2]:
                    new_words = words.copy()
                    new_words[i] = synonym
                    new_phrase = ' '.join(new_words)
                    variations.append({
                        "text": new_phrase.title(),
                        "type": "synonym",
                        "swap": f"{clean_word} -> {synonym}"
                    })

        return variations

    def _generate_structural_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate structural alternatives."""
        variations = []
        phrase_lower = phrase.lower()

        # "X is my Y" pattern
        match = re.match(r'(.+) is my (.+)', phrase_lower)
        if match:
            subject, object_ = match.groups()
            variations.extend([
                {"text": f"My {object_} is {subject}".title(), "type": "structure"},
                {"text": f"{subject.capitalize()}: my {object_}", "type": "structure"},
                {"text": f"All I need is {subject}".title(), "type": "structure"},
            ])

        # "I'm X" pattern
        match = re.match(r"i'?m (.+)", phrase_lower)
        if match:
            rest = match.group(1)
            variations.extend([
                {"text": f"Proud to be {rest}".title(), "type": "structure"},
                {"text": f"100% {rest}".title(), "type": "structure"},
                {"text": f"Certified {rest}".title(), "type": "structure"},
            ])

        # Add negation flip for humor
        if " not " in phrase_lower:
            # Already has negation, keep as is
            pass
        elif "don't" in phrase_lower or "can't" in phrase_lower:
            # Already has negation
            pass
        else:
            # Add sarcastic "totally not" version
            variations.append({
                "text": f"Totally not {phrase_lower}".title(),
                "type": "humor"
            })

        return variations

    def _clean_text(self, text: str) -> str:
        """Clean and format text properly."""
        # Remove extra spaces
        text = ' '.join(text.split())

        # Capitalize first letter of each word for title case
        # But keep small words lowercase
        small_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'by', 'is', 'my'}
        words = text.split()
        result = []
        for i, word in enumerate(words):
            if i == 0 or word.lower() not in small_words:
                result.append(word.capitalize())
            else:
                result.append(word.lower())

        return ' '.join(result)

    def suggest_niches(self, phrase: str) -> List[str]:
        """Suggest niches that might work well with a phrase."""
        phrase_lower = phrase.lower()

        niche_keywords = {
            "fitness": ["gym", "workout", "gains", "lift", "run", "sweat", "muscle", "fit"],
            "coffee": ["coffee", "caffeine", "espresso", "morning", "brew", "latte"],
            "parenting": ["mom", "dad", "kids", "parent", "child", "baby", "mama", "papa"],
            "pets": ["dog", "cat", "pet", "fur", "paw", "bark", "meow", "puppy", "kitty"],
            "nursing": ["nurse", "scrubs", "hospital", "patient", "shift", "rn", "healthcare"],
            "teaching": ["teacher", "school", "class", "student", "grade", "educate"],
            "gaming": ["game", "gamer", "play", "level", "quest", "xbox", "playstation"],
            "programming": ["code", "debug", "program", "developer", "software", "tech"],
            "fishing": ["fish", "catch", "bait", "reel", "lake", "boat", "angler"],
            "outdoors": ["hike", "hiking", "camp", "mountain", "trail", "nature", "outdoor"],
        }

        matching_niches = []
        for niche, keywords in niche_keywords.items():
            for keyword in keywords:
                if keyword in phrase_lower:
                    matching_niches.append(niche)
                    break

        if not matching_niches:
            matching_niches = ["humor", "lifestyle", "general"]

        return matching_niches


# Singleton instance
variation_generator = VariationGenerator()

"""Phrase variation generator."""
import re
import logging
from typing import List, Dict, Any, Optional
import random

logger = logging.getLogger(__name__)


class VariationGenerator:
    """Generate variations of phrases for ideation."""

    # Synonym mappings for common words
    SYNONYMS = {
        "love": ["adore", "heart", "obsessed with", "crazy about"],
        "hate": ["can't stand", "despise", "not a fan of"],
        "coffee": ["caffeine", "espresso", "java", "brew"],
        "tired": ["exhausted", "running on empty", "drained"],
        "happy": ["joyful", "blessed", "living my best life"],
        "crazy": ["wild", "insane", "unhinged", "chaotic"],
        "funny": ["hilarious", "comedic", "witty"],
        "cool": ["awesome", "epic", "legendary", "fire"],
        "mom": ["mama", "mother", "mommy"],
        "dad": ["papa", "father", "daddy", "old man"],
        "dog": ["pup", "pupper", "fur baby", "good boy"],
        "cat": ["kitty", "feline", "fur baby"],
        "work": ["grind", "hustle", "9-5"],
        "home": ["casa", "crib", "sanctuary"],
        "food": ["snacks", "fuel", "sustenance"],
        "sleep": ["nap", "rest", "hibernation"],
        "weekend": ["freedom", "me time", "adventure time"],
    }

    # Tone modifiers
    TONE_PREFIXES = {
        "sarcastic": [
            "Oh great,", "Apparently", "Supposedly", "As if",
            "Because obviously", "In case you were wondering"
        ],
        "proud": [
            "Proudly", "Officially", "Unapologetically",
            "100%", "Certified", "Professional"
        ],
        "ironic": [
            "Totally", "Definitely", "Absolutely",
            "Clearly", "Obviously"
        ],
        "enthusiastic": [
            "Living for", "Obsessed with", "Here for",
            "All about", "Team"
        ]
    }

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
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate variations of a phrase.

        Args:
            phrase: Original phrase
            variation_type: Type of variation (synonym, tone, structure, all)
            count: Number of variations to generate

        Returns:
            List of variation dictionaries
        """
        variations = []

        if variation_type in ["synonym", "all"]:
            variations.extend(self._generate_synonym_variations(phrase))

        if variation_type in ["tone", "all"]:
            variations.extend(self._generate_tone_variations(phrase))

        if variation_type in ["structure", "all"]:
            variations.extend(self._generate_structure_variations(phrase))

        # Deduplicate and limit
        seen = set()
        unique_variations = []
        for var in variations:
            normalized = var["text"].lower()
            if normalized not in seen and normalized != phrase.lower():
                seen.add(normalized)
                unique_variations.append(var)

        return unique_variations[:count]

    def _generate_synonym_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations by replacing words with synonyms."""
        variations = []
        words = phrase.lower().split()

        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in self.SYNONYMS:
                for synonym in self.SYNONYMS[clean_word]:
                    new_words = words.copy()
                    new_words[i] = synonym
                    new_phrase = ' '.join(new_words)
                    variations.append({
                        "text": new_phrase.capitalize(),
                        "type": "synonym",
                        "original_word": clean_word,
                        "replacement": synonym
                    })

        return variations

    def _generate_tone_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations with different tones."""
        variations = []

        for tone, prefixes in self.TONE_PREFIXES.items():
            prefix = random.choice(prefixes)
            new_phrase = f"{prefix} {phrase.lower()}"
            variations.append({
                "text": new_phrase,
                "type": "tone",
                "tone": tone
            })

        return variations

    def _generate_structure_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations with different structures."""
        variations = []

        # Convert to question
        if not phrase.endswith("?"):
            question = f"Why {phrase.lower()}?"
            variations.append({
                "text": question,
                "type": "structure",
                "structure": "question"
            })

        # Add emphasis
        words = phrase.split()
        if len(words) >= 2:
            # Repeat first word
            emphasized = f"{words[0]} {words[0].lower()} " + " ".join(words[1:])
            variations.append({
                "text": emphasized,
                "type": "structure",
                "structure": "emphasis"
            })

        # Make it a statement about self
        if not phrase.lower().startswith("i "):
            self_statement = f"I {phrase.lower()}"
            variations.append({
                "text": self_statement,
                "type": "structure",
                "structure": "self_statement"
            })

        # Make it possessive
        if not phrase.lower().startswith("my "):
            possessive = f"My {phrase.lower()}"
            variations.append({
                "text": possessive,
                "type": "structure",
                "structure": "possessive"
            })

        # Add "life" at the end
        if "life" not in phrase.lower():
            life_phrase = f"{phrase} life"
            variations.append({
                "text": life_phrase,
                "type": "structure",
                "structure": "lifestyle"
            })

        return variations

    def suggest_niches(self, phrase: str) -> List[str]:
        """Suggest niches that might work well with a phrase."""
        phrase_lower = phrase.lower()

        niche_keywords = {
            "fitness": ["gym", "workout", "gains", "lift", "run", "sweat", "muscle"],
            "coffee": ["coffee", "caffeine", "espresso", "morning", "brew"],
            "parenting": ["mom", "dad", "kids", "parent", "child", "baby"],
            "pets": ["dog", "cat", "pet", "fur", "paw", "bark", "meow"],
            "nursing": ["nurse", "scrubs", "hospital", "patient", "shift"],
            "teaching": ["teacher", "school", "class", "student", "grade"],
            "gaming": ["game", "gamer", "play", "level", "quest"],
            "programming": ["code", "debug", "program", "developer", "software"],
            "fishing": ["fish", "catch", "bait", "reel", "lake", "boat"],
            "reading": ["book", "read", "library", "chapter", "story"],
        }

        matching_niches = []
        for niche, keywords in niche_keywords.items():
            for keyword in keywords:
                if keyword in phrase_lower:
                    matching_niches.append(niche)
                    break

        # If no specific match, suggest general niches
        if not matching_niches:
            matching_niches = ["humor", "lifestyle", "general"]

        return matching_niches

    def adjust_for_merch(self, phrase: str) -> Dict[str, Any]:
        """
        Adjust a phrase to be more suitable for merchandise.

        Returns adjusted phrase and recommendations.
        """
        result = {
            "original": phrase,
            "adjusted": phrase,
            "changes": [],
            "recommendations": []
        }

        # Check length
        word_count = len(phrase.split())
        if word_count > 8:
            result["recommendations"].append(
                "Consider shortening - phrases over 8 words may not fit well on products"
            )

        if word_count < 2:
            result["recommendations"].append(
                "Very short phrases may lack context - consider expanding"
            )

        # Check for potentially problematic content
        problematic = ["kill", "die", "dead", "hate", "stupid", "idiot"]
        for word in problematic:
            if word in phrase.lower():
                result["recommendations"].append(
                    f"Word '{word}' may cause issues with some POD platforms"
                )

        # Suggest capitalization
        if phrase.islower():
            result["adjusted"] = phrase.title()
            result["changes"].append("Applied title case")
        elif phrase.isupper():
            result["adjusted"] = phrase.title()
            result["changes"].append("Changed from all caps to title case")

        return result

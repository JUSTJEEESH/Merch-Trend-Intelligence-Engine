"""Phrase variation generator - creates useful merch phrase alternatives."""
import re
import logging
from typing import List, Dict, Any, Optional
import random

logger = logging.getLogger(__name__)


class VariationGenerator:
    """Generate creative variations of phrases for merch ideation."""

    # Activity/hobby synonyms and related concepts
    ACTIVITY_SYNONYMS = {
        "hiking": ["trails", "mountains", "nature", "outdoors", "trekking", "walking"],
        "fishing": ["angling", "casting", "the water", "the lake", "reeling"],
        "gaming": ["playing", "my controller", "the game", "leveling up"],
        "coding": ["programming", "debugging", "my keyboard", "the terminal"],
        "reading": ["books", "my kindle", "the library", "getting lost in pages"],
        "running": ["jogging", "the track", "miles", "my sneakers"],
        "yoga": ["stretching", "my mat", "breathing", "meditation"],
        "cooking": ["the kitchen", "my recipes", "baking", "food"],
        "gardening": ["my plants", "the garden", "growing things", "dirt"],
        "crafting": ["creating", "making things", "DIY", "my hands"],
        "camping": ["the outdoors", "nature", "under the stars", "the tent"],
        "hunting": ["the woods", "the blind", "tracking", "the wild"],
        "golfing": ["the course", "my clubs", "the green", "18 holes"],
        "swimming": ["the pool", "the water", "laps", "diving"],
        "biking": ["cycling", "pedaling", "two wheels", "the trail"],
        "lifting": ["the gym", "weights", "gains", "the iron"],
        "knitting": ["yarn", "needles", "stitches", "creating"],
    }

    # Therapy/self-care pattern alternatives
    THERAPY_PATTERNS = [
        "{activity} is my therapy",
        "{activity} is cheaper than therapy",
        "I don't need therapy I need {activity}",
        "My therapist recommends {activity}",
        "{activity}: cheaper than a therapist",
        "Therapy is expensive {activity} is free",
        "{activity} fixes everything",
        "{activity} is my happy place",
        "{activity} is my escape",
        "Less drama more {activity}",
        "{activity} over everything",
        "Born to {verb}",
        "I'd rather be {verb_ing}",
        "My soul needs {activity}",
        "{activity} heals the soul",
    ]

    # Common phrase patterns and their alternatives
    PHRASE_PATTERNS = {
        r"(.+) is my therapy": [
            "{0} is cheaper than therapy",
            "I don't need therapy I need {0}",
            "My therapist says I need more {0}",
            "{0} is my happy place",
            "{0} fixes everything therapy can't",
            "{0} heals the soul",
            "Forget therapy give me {0}",
            "{0} is the only therapy I need",
        ],
        r"I love (.+)": [
            "{0} is my love language",
            "My heart belongs to {0}",
            "{0} has my whole heart",
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
            "Send {0}",
        ],
        r"(.+) mom": [
            "{0} mama",
            "Proud {0} mom",
            "{0} mom life",
            "Best {0} mom ever",
            "{0} mom mode",
            "Living that {0} mom life",
        ],
        r"(.+) dad": [
            "{0} papa",
            "Proud {0} dad",
            "{0} dad life",
            "Best {0} dad ever",
            "{0} dad mode",
            "Rocking the {0} dad life",
        ],
        r"I('m| am) not (.+) I('m| am) (.+)": [
            "Not {1} just {3}",
            "{3} not {1}",
            "Call me {3} not {1}",
        ],
        r"powered by (.+)": [
            "Runs on {0}",
            "Fueled by {0}",
            "{0} is my fuel",
            "Operating on {0}",
            "{0} powered",
        ],
    }

    # Word-level synonyms for common merch words
    WORD_SYNONYMS = {
        "love": ["adore", "heart", "live for", "obsessed with"],
        "need": ["require", "must have", "can't live without"],
        "coffee": ["caffeine", "espresso", "java", "brew", "bean juice"],
        "wine": ["vino", "grape juice", "the good stuff"],
        "beer": ["brews", "cold ones", "hops"],
        "tired": ["exhausted", "running on empty", "drained", "sleepy"],
        "happy": ["joyful", "blessed", "content", "thriving"],
        "crazy": ["wild", "chaotic", "unhinged", "feral"],
        "mom": ["mama", "mother", "mommy", "madre"],
        "dad": ["papa", "father", "daddy", "pops"],
        "dog": ["pup", "pupper", "fur baby", "good boy", "doggo"],
        "cat": ["kitty", "feline", "fur baby", "floof"],
        "best": ["greatest", "top", "ultimate", "finest"],
        "life": ["existence", "journey", "vibe", "mood"],
        "therapy": ["medicine", "cure", "healing", "escape", "happy place"],
    }

    # Creative phrase twists
    TWIST_TEMPLATES = [
        "Less {bad_thing} more {good_thing}",
        "{good_thing} over {bad_thing}",
        "Choose {good_thing}",
        "{good_thing} is the answer",
        "When in doubt {good_thing}",
        "Will trade {bad_thing} for {good_thing}",
        "{good_thing} first {bad_thing} never",
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

        # Try pattern-based variations first (usually best)
        variations.extend(self._generate_pattern_variations(phrase))

        # Add word-swap variations
        variations.extend(self._generate_word_swap_variations(phrase))

        # Add creative twists
        variations.extend(self._generate_creative_twists(phrase))

        # Add alternative structures
        variations.extend(self._generate_alternative_structures(phrase))

        # Deduplicate and clean
        seen = set()
        unique_variations = []
        original_lower = phrase.lower().strip()

        for var in variations:
            text = var["text"].strip()
            normalized = text.lower()

            # Skip if same as original or already seen
            if normalized == original_lower or normalized in seen:
                continue

            # Skip if too similar (just added/removed a word)
            if self._is_too_similar(normalized, original_lower):
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
                        # Fill in the template with captured groups
                        new_phrase = template
                        for i, group in enumerate(groups):
                            if group:  # Skip None groups
                                new_phrase = new_phrase.replace(f"{{{i}}}", group)

                        if new_phrase != template:  # Make sure substitution happened
                            variations.append({
                                "text": new_phrase.capitalize(),
                                "type": "pattern",
                                "pattern": pattern
                            })
                    except Exception:
                        continue

        return variations

    def _generate_word_swap_variations(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate variations by swapping words with synonyms."""
        variations = []
        words = phrase.lower().split()

        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word)

            # Check direct synonyms
            if clean_word in self.WORD_SYNONYMS:
                for synonym in self.WORD_SYNONYMS[clean_word][:3]:
                    new_words = words.copy()
                    new_words[i] = synonym
                    new_phrase = ' '.join(new_words)
                    variations.append({
                        "text": new_phrase.capitalize(),
                        "type": "synonym",
                        "swap": f"{clean_word} → {synonym}"
                    })

            # Check activity synonyms
            if clean_word in self.ACTIVITY_SYNONYMS:
                for alt in self.ACTIVITY_SYNONYMS[clean_word][:2]:
                    new_words = words.copy()
                    new_words[i] = alt
                    new_phrase = ' '.join(new_words)
                    variations.append({
                        "text": new_phrase.capitalize(),
                        "type": "activity_swap",
                        "swap": f"{clean_word} → {alt}"
                    })

        return variations

    def _generate_creative_twists(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate creative alternative phrasings."""
        variations = []
        phrase_lower = phrase.lower()

        # Extract the main subject/activity
        activity = self._extract_activity(phrase_lower)
        if not activity:
            return variations

        # Generate "I'd rather be X" style
        verb_ing = self._to_gerund(activity)
        if verb_ing:
            variations.append({
                "text": f"I'd rather be {verb_ing}",
                "type": "creative",
                "style": "preference"
            })

        # Generate "Born to X" style
        variations.append({
            "text": f"Born to {activity}",
            "type": "creative",
            "style": "destiny"
        })

        # Generate comparison style
        variations.append({
            "text": f"Less talk more {activity}",
            "type": "creative",
            "style": "comparison"
        })

        variations.append({
            "text": f"{activity.capitalize()} over everything",
            "type": "creative",
            "style": "priority"
        })

        variations.append({
            "text": f"Eat sleep {activity} repeat",
            "type": "creative",
            "style": "routine"
        })

        variations.append({
            "text": f"Will work for {activity}",
            "type": "creative",
            "style": "humor"
        })

        return variations

    def _generate_alternative_structures(self, phrase: str) -> List[Dict[str, Any]]:
        """Generate structural alternatives."""
        variations = []
        phrase_lower = phrase.lower()

        # If it's an "X is my Y" phrase
        match = re.match(r'(.+) is my (.+)', phrase_lower)
        if match:
            subject, object_ = match.groups()
            variations.extend([
                {"text": f"My {object_} is {subject}", "type": "structure", "style": "inverted"},
                {"text": f"{subject.capitalize()}: my {object_}", "type": "structure", "style": "colon"},
                {"text": f"All I need is {subject}", "type": "structure", "style": "simplified"},
                {"text": f"{subject.capitalize()} = {object_}", "type": "structure", "style": "equation"},
            ])

        # If it has "I'm" or "I am"
        match = re.match(r"i'?m (.+)", phrase_lower)
        if match:
            rest = match.group(1)
            variations.extend([
                {"text": f"Proud to be {rest}", "type": "structure", "style": "proud"},
                {"text": f"100% {rest}", "type": "structure", "style": "percentage"},
                {"text": f"Certified {rest}", "type": "structure", "style": "certified"},
            ])

        return variations

    def _extract_activity(self, phrase: str) -> Optional[str]:
        """Extract the main activity/subject from a phrase."""
        # Common patterns to extract activity
        patterns = [
            r'(.+?) is my',
            r'i love (.+)',
            r'i need (.+)',
            r"i'd rather be (.+)",
            r'powered by (.+)',
            r'fueled by (.+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, phrase.lower())
            if match:
                return match.group(1).strip()

        # Fall back to first noun-like word
        words = phrase.lower().split()
        for word in words:
            clean = re.sub(r'[^\w]', '', word)
            if clean in self.ACTIVITY_SYNONYMS or len(clean) > 3:
                return clean

        return None

    def _to_gerund(self, word: str) -> Optional[str]:
        """Convert a word to its -ing form."""
        word = word.lower().strip()

        # Special cases
        gerunds = {
            "hike": "hiking", "hiking": "hiking",
            "fish": "fishing", "fishing": "fishing",
            "game": "gaming", "gaming": "gaming",
            "code": "coding", "coding": "coding",
            "run": "running", "running": "running",
            "swim": "swimming", "swimming": "swimming",
            "read": "reading", "reading": "reading",
            "cook": "cooking", "cooking": "cooking",
            "camp": "camping", "camping": "camping",
            "hunt": "hunting", "hunting": "hunting",
            "golf": "golfing", "golfing": "golfing",
            "bike": "biking", "biking": "biking",
            "lift": "lifting", "lifting": "lifting",
            "craft": "crafting", "crafting": "crafting",
            "garden": "gardening", "gardening": "gardening",
            "travel": "traveling", "traveling": "traveling",
            "climb": "climbing", "climbing": "climbing",
            "surf": "surfing", "surfing": "surfing",
            "ski": "skiing", "skiing": "skiing",
            "skate": "skating", "skating": "skating",
            "dance": "dancing", "dancing": "dancing",
            "paint": "painting", "painting": "painting",
            "write": "writing", "writing": "writing",
            "shop": "shopping", "shopping": "shopping",
            "nap": "napping", "napping": "napping",
            "sleep": "sleeping", "sleeping": "sleeping",
            "eat": "eating", "eating": "eating",
            "drink": "drinking", "drinking": "drinking",
        }

        if word in gerunds:
            return gerunds[word]

        # Generic rule
        if word.endswith('e'):
            return word[:-1] + 'ing'
        elif word.endswith('ing'):
            return word
        else:
            return word + 'ing'

    def _is_too_similar(self, var: str, original: str) -> bool:
        """Check if variation is too similar to original."""
        var_words = set(var.split())
        orig_words = set(original.split())

        # If only 1 word different and phrase is short, too similar
        diff = var_words.symmetric_difference(orig_words)
        if len(diff) <= 1 and len(orig_words) <= 4:
            return True

        return False

    def _clean_text(self, text: str) -> str:
        """Clean and format text properly."""
        # Remove extra spaces
        text = ' '.join(text.split())

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        return text

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

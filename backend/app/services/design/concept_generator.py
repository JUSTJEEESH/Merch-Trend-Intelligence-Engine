"""Design concept generator service."""
import random
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DesignConceptGenerator:
    """
    Service for generating design concepts, font pairings,
    color palettes, and layout suggestions for merch phrases.
    """

    # Font pairings by style
    FONT_PAIRINGS = {
        "bold_statement": [
            {"primary": "Impact", "secondary": "Helvetica", "style": "bold"},
            {"primary": "Bebas Neue", "secondary": "Montserrat", "style": "modern"},
            {"primary": "Anton", "secondary": "Roboto", "style": "clean"},
        ],
        "playful": [
            {"primary": "Pacifico", "secondary": "Poppins", "style": "fun"},
            {"primary": "Comic Sans MS", "secondary": "Arial", "style": "casual"},
            {"primary": "Bangers", "secondary": "Open Sans", "style": "comic"},
        ],
        "elegant": [
            {"primary": "Playfair Display", "secondary": "Lato", "style": "sophisticated"},
            {"primary": "Cormorant Garamond", "secondary": "Raleway", "style": "classic"},
            {"primary": "Bodoni", "secondary": "Futura", "style": "luxury"},
        ],
        "vintage": [
            {"primary": "American Typewriter", "secondary": "Courier", "style": "retro"},
            {"primary": "Rockwell", "secondary": "Georgia", "style": "western"},
            {"primary": "Abril Fatface", "secondary": "Josefin Sans", "style": "classic"},
        ],
        "modern": [
            {"primary": "Oswald", "secondary": "Source Sans Pro", "style": "sleek"},
            {"primary": "Raleway", "secondary": "Open Sans", "style": "minimal"},
            {"primary": "Montserrat", "secondary": "Hind", "style": "contemporary"},
        ],
        "handwritten": [
            {"primary": "Dancing Script", "secondary": "Quicksand", "style": "script"},
            {"primary": "Sacramento", "secondary": "Nunito", "style": "cursive"},
            {"primary": "Great Vibes", "secondary": "Lora", "style": "calligraphy"},
        ],
        "grunge": [
            {"primary": "Permanent Marker", "secondary": "Roboto Condensed", "style": "edgy"},
            {"primary": "Rock Salt", "secondary": "Arimo", "style": "distressed"},
            {"primary": "Special Elite", "secondary": "PT Sans", "style": "typewriter"},
        ],
    }

    # Color palettes by mood/niche
    COLOR_PALETTES = {
        "energetic": [
            {"name": "Electric", "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"], "bg": "#1A1A2E"},
            {"name": "Sunset", "colors": ["#FF7E5F", "#FEB47B", "#FFE66D", "#B8E994"], "bg": "#2D3436"},
            {"name": "Neon", "colors": ["#FF00FF", "#00FFFF", "#FFFF00", "#FF00AA"], "bg": "#0D0D0D"},
        ],
        "calm": [
            {"name": "Ocean", "colors": ["#0077B6", "#00B4D8", "#90E0EF", "#CAF0F8"], "bg": "#03045E"},
            {"name": "Forest", "colors": ["#2D6A4F", "#40916C", "#52B788", "#95D5B2"], "bg": "#1B4332"},
            {"name": "Lavender", "colors": ["#7B68EE", "#9370DB", "#BA55D3", "#DDA0DD"], "bg": "#2C2C54"},
        ],
        "bold": [
            {"name": "Fire", "colors": ["#FF0000", "#FF4500", "#FF6347", "#FFA500"], "bg": "#1A0000"},
            {"name": "Royal", "colors": ["#4B0082", "#8A2BE2", "#9400D3", "#9932CC"], "bg": "#0D0D1A"},
            {"name": "Power", "colors": ["#000000", "#FFD700", "#FFFFFF", "#FF0000"], "bg": "#1A1A1A"},
        ],
        "pastel": [
            {"name": "Cotton Candy", "colors": ["#FFB6C1", "#87CEEB", "#98FB98", "#DDA0DD"], "bg": "#FFF0F5"},
            {"name": "Easter", "colors": ["#E6E6FA", "#FFB7C5", "#BDFCC9", "#FFFACD"], "bg": "#FFFFFF"},
            {"name": "Soft", "colors": ["#F0E6EF", "#E6F0F0", "#F0F0E6", "#E6E6F0"], "bg": "#FAFAFA"},
        ],
        "monochrome": [
            {"name": "Classic BW", "colors": ["#FFFFFF", "#CCCCCC", "#666666", "#000000"], "bg": "#1A1A1A"},
            {"name": "Noir", "colors": ["#F5F5F5", "#BDBDBD", "#757575", "#212121"], "bg": "#121212"},
        ],
        "retro": [
            {"name": "70s", "colors": ["#DB7093", "#E9967A", "#F0E68C", "#98FB98"], "bg": "#8B4513"},
            {"name": "80s", "colors": ["#FF1493", "#00CED1", "#FFD700", "#32CD32"], "bg": "#0D0D0D"},
            {"name": "90s", "colors": ["#9400D3", "#00FF7F", "#FF6347", "#00BFFF"], "bg": "#2F4F4F"},
        ],
        "coffee": [
            {"name": "Espresso", "colors": ["#3E2723", "#5D4037", "#8D6E63", "#D7CCC8"], "bg": "#1A1A1A"},
            {"name": "Latte", "colors": ["#4E342E", "#795548", "#A1887F", "#EFEBE9"], "bg": "#3E2723"},
        ],
        "nature": [
            {"name": "Earth", "colors": ["#5D4037", "#8D6E63", "#A1887F", "#BCAAA4"], "bg": "#3E2723"},
            {"name": "Jungle", "colors": ["#1B5E20", "#388E3C", "#4CAF50", "#81C784"], "bg": "#0D0D0D"},
        ],
    }

    # Layout templates
    LAYOUT_TEMPLATES = {
        "centered": {
            "name": "Centered Classic",
            "description": "Text centered horizontally and vertically",
            "best_for": ["short phrases", "single words", "statements"],
            "css": "text-align: center; display: flex; align-items: center; justify-content: center;",
        },
        "stacked": {
            "name": "Stacked Words",
            "description": "Each word on its own line, varying sizes",
            "best_for": ["2-4 word phrases", "emphasis phrases"],
            "css": "display: flex; flex-direction: column; text-align: center;",
        },
        "badge": {
            "name": "Badge/Emblem",
            "description": "Circular or shield-shaped design with text",
            "best_for": ["clubs", "teams", "official-looking designs"],
            "css": "border-radius: 50%; border: 4px solid; padding: 20px;",
        },
        "vintage_banner": {
            "name": "Vintage Banner",
            "description": "Ribbon banner with distressed text",
            "best_for": ["retro phrases", "established dates", "classic sayings"],
            "css": "background: ribbon-shape; text-transform: uppercase;",
        },
        "diagonal": {
            "name": "Diagonal Angle",
            "description": "Text at a dynamic angle",
            "best_for": ["action phrases", "energetic messages"],
            "css": "transform: rotate(-15deg);",
        },
        "arch": {
            "name": "Arched Text",
            "description": "Text curved in an arc shape",
            "best_for": ["team names", "location names", "pride phrases"],
            "css": "text-on-path: arc;",
        },
        "split": {
            "name": "Split Design",
            "description": "Text split across design with graphic in middle",
            "best_for": ["longer phrases", "before/after concepts"],
            "css": "display: grid; grid-template-rows: 1fr auto 1fr;",
        },
        "corner_small": {
            "name": "Small Corner",
            "description": "Small text in corner/pocket area",
            "best_for": ["minimalist designs", "subtle messages", "pocket prints"],
            "css": "position: absolute; top: 20px; left: 20px; font-size: 0.8em;",
        },
        "full_front": {
            "name": "Full Front",
            "description": "Large text across entire front",
            "best_for": ["bold statements", "maximum visibility"],
            "css": "font-size: 4em; width: 100%;",
        },
    }

    # Style presets by phrase type
    STYLE_PRESETS = {
        "funny": {
            "fonts": ["playful", "bold_statement"],
            "colors": ["energetic", "bold", "retro"],
            "layouts": ["centered", "stacked", "diagonal"],
        },
        "motivational": {
            "fonts": ["modern", "bold_statement", "elegant"],
            "colors": ["bold", "nature", "monochrome"],
            "layouts": ["centered", "stacked", "full_front"],
        },
        "sarcastic": {
            "fonts": ["grunge", "handwritten", "vintage"],
            "colors": ["retro", "monochrome", "bold"],
            "layouts": ["centered", "diagonal", "corner_small"],
        },
        "wholesome": {
            "fonts": ["handwritten", "playful", "elegant"],
            "colors": ["pastel", "calm", "nature"],
            "layouts": ["centered", "arch", "badge"],
        },
        "edgy": {
            "fonts": ["grunge", "bold_statement", "modern"],
            "colors": ["bold", "monochrome", "energetic"],
            "layouts": ["diagonal", "full_front", "split"],
        },
        "aesthetic": {
            "fonts": ["elegant", "handwritten", "modern"],
            "colors": ["pastel", "calm", "monochrome"],
            "layouts": ["centered", "corner_small", "stacked"],
        },
        "vintage": {
            "fonts": ["vintage", "grunge"],
            "colors": ["retro", "coffee", "monochrome"],
            "layouts": ["vintage_banner", "badge", "arch"],
        },
    }

    def generate_concept(self, phrase: str, style: str = "funny") -> Dict[str, Any]:
        """Generate a complete design concept for a phrase."""
        preset = self.STYLE_PRESETS.get(style, self.STYLE_PRESETS["funny"])

        # Select font pairing
        font_style = random.choice(preset["fonts"])
        font = random.choice(self.FONT_PAIRINGS[font_style])

        # Select color palette
        color_mood = random.choice(preset["colors"])
        palette = random.choice(self.COLOR_PALETTES[color_mood])

        # Select layout
        layout_name = random.choice(preset["layouts"])
        layout = self.LAYOUT_TEMPLATES[layout_name]

        # Analyze phrase for additional suggestions
        analysis = self._analyze_phrase(phrase)

        return {
            "phrase": phrase,
            "style": style,
            "concept": {
                "font_pairing": font,
                "color_palette": palette,
                "layout": layout,
                "recommendations": analysis,
            },
            "alternatives": self._generate_alternatives(phrase, preset),
        }

    def get_concepts_for_phrase(self, phrase: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple design concepts for a phrase."""
        # Determine best styles for phrase
        styles = self._suggest_styles(phrase)

        concepts = []
        for i, style in enumerate(styles[:count]):
            concept = self.generate_concept(phrase, style)
            concept["rank"] = i + 1
            concepts.append(concept)

        return concepts

    def _analyze_phrase(self, phrase: str) -> Dict[str, Any]:
        """Analyze phrase for design recommendations."""
        words = phrase.split()
        char_count = len(phrase)

        recommendations = []

        # Length-based recommendations
        if char_count > 30:
            recommendations.append("Consider splitting into multiple lines")
            recommendations.append("Use smaller font or stacked layout")
        elif char_count < 15:
            recommendations.append("Great for large, bold typography")
            recommendations.append("Works well for pocket prints")

        # Word count recommendations
        if len(words) <= 2:
            recommendations.append("Perfect for centered, large text")
        elif len(words) <= 4:
            recommendations.append("Consider stacked layout with varying sizes")
        else:
            recommendations.append("Use hierarchy to emphasize key words")

        # Special character detection
        if any(c in phrase for c in "!?"):
            recommendations.append("Emphasize punctuation for impact")

        return {
            "word_count": len(words),
            "character_count": char_count,
            "recommendations": recommendations,
            "emphasis_words": self._find_emphasis_words(words),
        }

    def _find_emphasis_words(self, words: List[str]) -> List[str]:
        """Find words that should be emphasized in design."""
        emphasis_triggers = [
            "not", "never", "always", "very", "best", "worst",
            "love", "hate", "need", "want", "literally", "actually",
            "but", "only", "all", "no", "yes", "maybe",
        ]

        emphasis = []
        for word in words:
            clean = word.lower().strip(".,!?")
            if clean in emphasis_triggers or len(clean) <= 2:
                continue
            emphasis.append(word)

        # Return longest/most important words
        return sorted(emphasis, key=len, reverse=True)[:2]

    def _suggest_styles(self, phrase: str) -> List[str]:
        """Suggest best styles for a phrase."""
        phrase_lower = phrase.lower()

        # Keyword-based style detection
        if any(w in phrase_lower for w in ["slay", "era", "vibes", "aesthetic", "core"]):
            return ["aesthetic", "modern", "funny"]
        elif any(w in phrase_lower for w in ["anxious", "tired", "chaos", "mess"]):
            return ["sarcastic", "edgy", "funny"]
        elif any(w in phrase_lower for w in ["love", "blessed", "grateful", "happy"]):
            return ["wholesome", "aesthetic", "motivational"]
        elif any(w in phrase_lower for w in ["vintage", "retro", "classic", "old"]):
            return ["vintage", "aesthetic", "wholesome"]
        elif any(w in phrase_lower for w in ["grind", "hustle", "goal", "dream"]):
            return ["motivational", "modern", "edgy"]
        else:
            return ["funny", "modern", "sarcastic"]

    def _generate_alternatives(self, phrase: str, preset: Dict) -> List[Dict]:
        """Generate alternative design options."""
        alternatives = []

        # Generate 2 alternative concepts
        for _ in range(2):
            font_style = random.choice(preset["fonts"])
            color_mood = random.choice(preset["colors"])

            alternatives.append({
                "font": random.choice(self.FONT_PAIRINGS[font_style]),
                "colors": random.choice(self.COLOR_PALETTES[color_mood]),
                "layout": random.choice(preset["layouts"]),
            })

        return alternatives

    def get_color_palette_for_niche(self, niche: str) -> Dict[str, Any]:
        """Get recommended color palettes for a niche."""
        niche_colors = {
            "coffee": ["coffee", "nature", "monochrome"],
            "fitness": ["energetic", "bold", "monochrome"],
            "dogs": ["calm", "nature", "pastel"],
            "cats": ["calm", "pastel", "monochrome"],
            "gaming": ["energetic", "bold", "retro"],
            "mom": ["pastel", "calm", "energetic"],
            "dad": ["retro", "monochrome", "bold"],
            "beer": ["retro", "bold", "nature"],
            "wine": ["calm", "pastel", "monochrome"],
            "nurse": ["calm", "bold", "pastel"],
            "teacher": ["pastel", "calm", "energetic"],
        }

        moods = niche_colors.get(niche.lower(), ["monochrome", "bold"])
        palettes = []

        for mood in moods:
            palettes.extend(self.COLOR_PALETTES.get(mood, []))

        return {
            "niche": niche,
            "recommended_palettes": palettes[:5],
        }


# Singleton instance
design_generator = DesignConceptGenerator()

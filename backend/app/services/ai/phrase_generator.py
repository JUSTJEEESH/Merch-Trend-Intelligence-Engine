"""AI-powered phrase generation service with tone control."""
import random
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIPhraseGenerator:
    """
    Advanced phrase generator with AI-like capabilities.
    Supports multiple tones, styles, and formats.
    """

    # Tone-specific phrase patterns
    TONES = {
        "sarcastic": {
            "prefixes": [
                "Oh great, another", "Wow, shocking:", "Plot twist:",
                "Breaking news:", "Surprise surprise:", "Who knew:",
                "Apparently", "Allegedly", "Thanks, I hate",
            ],
            "suffixes": [
                "...said no one ever", "(sent from my couch)",
                "(insert eye roll)", "...shocking", "...but whatever",
                "...I guess", "...allegedly", "*heavy sigh*",
            ],
            "templates": [
                "{topic}? In THIS economy?",
                "Not me pretending to {action}",
                "My {thing} has left the chat",
                "If {thing} was a personality trait",
                "{topic}: A Saga",
                "POV: You're {action} again",
                "Tell me you're {thing} without telling me",
            ],
        },
        "wholesome": {
            "prefixes": [
                "Blessed with", "Grateful for", "Lucky to have",
                "Thankful for", "In love with", "Cherishing",
                "Appreciating", "Celebrating", "Loving my",
            ],
            "suffixes": [
                "and loving it", "always", "forever and always",
                "every single day", "with my whole heart",
                "and I wouldn't have it any other way",
            ],
            "templates": [
                "Home is where {thing} is",
                "Living for {thing}",
                "{thing} makes everything better",
                "Spreading {thing} everywhere I go",
                "Choose {thing} today",
                "Be someone's {thing}",
                "{thing} is my superpower",
            ],
        },
        "edgy": {
            "prefixes": [
                "Dead inside but", "Chaos mode:", "Zero f***s given:",
                "Warning:", "Caution:", "Enter at your own risk:",
                "Not today, Satan:", "Unhinged and",
            ],
            "suffixes": [
                "...and I took that personally", "(mentally)",
                "- the villain arc", "but make it toxic",
                "in this economy?!", "*screams internally*",
            ],
            "templates": [
                "Running on {thing} and bad decisions",
                "Professional {thing} destroyer",
                "{thing} but make it unhinged",
                "One {thing} away from losing it",
                "Certified {thing} menace",
                "My {thing} is everyone's problem now",
                "I don't have {thing}, I have audacity",
            ],
        },
        "motivational": {
            "prefixes": [
                "Rise and", "Born to", "Built to", "Destined for",
                "Chasing", "Becoming", "Embracing", "Conquering",
            ],
            "suffixes": [
                "one day at a time", "no matter what",
                "against all odds", "every single day",
                "and never looking back", "on my own terms",
            ],
            "templates": [
                "Be the {thing} you wish to see",
                "Your only limit is {thing}",
                "Make {thing} happen",
                "Dream big, {thing} bigger",
                "{thing} in progress",
                "Becoming {thing} version of me",
                "Watch me {action}",
            ],
        },
        "funny": {
            "prefixes": [
                "Probably", "Definitely", "99% sure I'm",
                "Professional", "Certified", "Licensed",
                "Self-proclaimed", "Undercover",
            ],
            "suffixes": [
                "but make it fashion", "and I have no regrets",
                "(I'm not sorry)", "(and I'm not apologizing)",
                "...allegedly", "...or whatever",
            ],
            "templates": [
                "I put the {thing} in {related}",
                "Part-time {thing}, full-time mess",
                "Too {thing} to function",
                "{thing} is my love language",
                "Here for the {thing}",
                "Fluent in {thing} and sarcasm",
                "Running on {thing} and spite",
            ],
        },
        "aesthetic": {
            "prefixes": [
                "That", "Core", "Softly", "Quietly",
                "Deeply", "Main character", "It girl",
            ],
            "suffixes": [
                "aesthetic", "vibes", "energy", "era",
                "coded", "core", "mood",
            ],
            "templates": [
                "{thing} girl aesthetic",
                "Giving {thing}",
                "{thing} core",
                "Very {thing}, very mindful",
                "In my {thing} era",
                "{thing} but make it chic",
                "Channeling {thing} energy",
            ],
        },
        "gen_z": {
            "prefixes": [
                "No cap,", "Fr fr", "Lowkey", "Highkey",
                "Not me", "POV:", "It's giving",
            ],
            "suffixes": [
                "no cap", "fr fr", "on god", "periodt",
                "slay", "ate that", "understood the assignment",
            ],
            "templates": [
                "{thing} hits different",
                "The way {thing} just",
                "{thing} is sending me",
                "Not me {action} again",
                "When the {thing} is {description}",
                "{thing} but unironically",
                "Me when {thing}:",
            ],
        },
        "millennial": {
            "prefixes": [
                "Adulting is", "When you realize", "That moment when",
                "Me: *tries to*", "Narrator:", "*laughs in*",
            ],
            "suffixes": [
                "is that too much to ask?", "I can't even",
                "and that's the tea", "but here we are",
                "it's fine, everything's fine",
            ],
            "templates": [
                "I survived {thing} and all I got was this shirt",
                "Old enough to know better, young enough for {thing}",
                "Will {thing} for coffee",
                "{thing}: A Memoir",
                "My therapist says {thing}",
                "I'm not {thing}, I'm quirky",
                "Tired but {thing}",
            ],
        },
    }

    # Topic-specific vocabulary
    TOPICS = {
        "coffee": {
            "things": ["coffee", "caffeine", "espresso", "latte", "iced coffee", "cold brew"],
            "actions": ["caffeinate", "coffee", "espresso", "brew"],
            "related": ["morning", "energy", "survival", "life"],
            "descriptions": ["strong", "bold", "caffeinated", "iced"],
        },
        "dogs": {
            "things": ["dogs", "puppy", "fur baby", "good boy", "paws", "treats"],
            "actions": ["pet", "walk", "snuggle", "adopt"],
            "related": ["love", "loyalty", "cuddles", "walks"],
            "descriptions": ["fluffy", "adorable", "loyal", "goofy"],
        },
        "cats": {
            "things": ["cats", "kitten", "fur baby", "meow", "whiskers", "catnip"],
            "actions": ["adopt", "nap", "judge", "ignore"],
            "related": ["naps", "attitude", "chaos", "independence"],
            "descriptions": ["fluffy", "sassy", "chaotic", "sleepy"],
        },
        "fitness": {
            "things": ["gains", "gym", "workout", "muscles", "protein", "weights"],
            "actions": ["lift", "train", "grind", "flex"],
            "related": ["sweat", "strength", "dedication", "results"],
            "descriptions": ["strong", "dedicated", "relentless", "unstoppable"],
        },
        "mom": {
            "things": ["mom life", "kids", "chaos", "wine", "coffee", "patience"],
            "actions": ["mom", "survive", "repeat", "caffeinate"],
            "related": ["love", "exhaustion", "snacks", "school"],
            "descriptions": ["tired", "blessed", "chaotic", "loving"],
        },
        "dad": {
            "things": ["dad life", "dad jokes", "naps", "grill", "lawn", "tools"],
            "actions": ["dad", "fix", "grill", "coach"],
            "related": ["jokes", "wisdom", "snoring", "sports"],
            "descriptions": ["tired", "proud", "handy", "legendary"],
        },
        "introvert": {
            "things": ["alone time", "books", "home", "quiet", "peace", "solitude"],
            "actions": ["recharge", "hide", "cancel", "avoid"],
            "related": ["energy", "boundaries", "comfort", "plans"],
            "descriptions": ["quiet", "content", "selective", "peaceful"],
        },
        "nurse": {
            "things": ["scrubs", "patients", "coffee", "night shift", "stethoscope"],
            "actions": ["heal", "care", "save", "caffeinate"],
            "related": ["healthcare", "heroes", "compassion", "overtime"],
            "descriptions": ["strong", "dedicated", "caffeinated", "heroic"],
        },
        "teacher": {
            "things": ["students", "coffee", "patience", "lesson plans", "markers"],
            "actions": ["teach", "inspire", "educate", "repeat"],
            "related": ["education", "summer", "grading", "learning"],
            "descriptions": ["dedicated", "patient", "inspiring", "caffeinated"],
        },
        "gaming": {
            "things": ["games", "controller", "respawn", "level up", "loot"],
            "actions": ["game", "play", "rage quit", "grind"],
            "related": ["skills", "noob", "pro", "stream"],
            "descriptions": ["epic", "legendary", "sweaty", "casual"],
        },
        "anxiety": {
            "things": ["anxiety", "overthinking", "worry", "what ifs", "panic"],
            "actions": ["overthink", "spiral", "worry", "stress"],
            "related": ["peace", "calm", "breathing", "therapy"],
            "descriptions": ["anxious", "chaotic", "spiraling", "coping"],
        },
        "work": {
            "things": ["work", "meetings", "emails", "deadline", "Mondays"],
            "actions": ["work", "survive", "clock out", "email"],
            "related": ["office", "corporate", "salary", "weekends"],
            "descriptions": ["burnt out", "over it", "professional", "underpaid"],
        },
    }

    def __init__(self):
        pass

    def generate_phrases(
        self,
        topic: str,
        tone: str = "funny",
        count: int = 20,
        max_length: int = 35,
    ) -> List[Dict[str, Any]]:
        """Generate phrases for a topic with specified tone."""
        phrases = []
        tone_data = self.TONES.get(tone, self.TONES["funny"])
        topic_data = self.TOPICS.get(topic.lower(), self._get_generic_topic(topic))

        # Generate from templates
        for template in tone_data["templates"]:
            phrase = self._fill_template(template, topic_data)
            if phrase and len(phrase) <= max_length:
                phrases.append({
                    "phrase": phrase,
                    "tone": tone,
                    "topic": topic,
                    "type": "template",
                })

        # Generate with prefixes
        for _ in range(count // 3):
            prefix = random.choice(tone_data["prefixes"])
            thing = random.choice(topic_data["things"])
            phrase = f"{prefix} {thing}"
            if len(phrase) <= max_length:
                phrases.append({
                    "phrase": phrase,
                    "tone": tone,
                    "topic": topic,
                    "type": "prefix",
                })

        # Generate with suffixes
        for _ in range(count // 3):
            thing = random.choice(topic_data["things"]).title()
            suffix = random.choice(tone_data["suffixes"])
            phrase = f"{thing} {suffix}"
            if len(phrase) <= max_length:
                phrases.append({
                    "phrase": phrase,
                    "tone": tone,
                    "topic": topic,
                    "type": "suffix",
                })

        # Deduplicate and limit
        seen = set()
        unique_phrases = []
        for p in phrases:
            if p["phrase"].lower() not in seen:
                seen.add(p["phrase"].lower())
                unique_phrases.append(p)

        return unique_phrases[:count]

    def generate_bulk(
        self,
        topic: str,
        tones: List[str] = None,
        count_per_tone: int = 10,
    ) -> Dict[str, List[Dict]]:
        """Generate phrases in multiple tones."""
        if tones is None:
            tones = list(self.TONES.keys())

        results = {}
        for tone in tones:
            results[tone] = self.generate_phrases(topic, tone, count_per_tone)

        return results

    def _fill_template(self, template: str, topic_data: Dict) -> Optional[str]:
        """Fill a template with topic-specific words."""
        try:
            filled = template
            if "{thing}" in filled:
                filled = filled.replace("{thing}", random.choice(topic_data["things"]))
            if "{action}" in filled:
                filled = filled.replace("{action}", random.choice(topic_data["actions"]))
            if "{related}" in filled:
                filled = filled.replace("{related}", random.choice(topic_data["related"]))
            if "{description}" in filled:
                filled = filled.replace("{description}", random.choice(topic_data["descriptions"]))
            if "{topic}" in filled:
                filled = filled.replace("{topic}", topic_data["things"][0].title())
            return filled
        except Exception:
            return None

    def _get_generic_topic(self, topic: str) -> Dict:
        """Generate generic topic data for unknown topics."""
        return {
            "things": [topic, f"{topic} life", f"my {topic}", topic.lower()],
            "actions": [f"{topic}", f"do {topic}", f"love {topic}"],
            "related": [topic, "life", "love", "passion"],
            "descriptions": ["amazing", "awesome", "incredible", "epic"],
        }

    def get_available_tones(self) -> List[str]:
        """Get list of available tones."""
        return list(self.TONES.keys())

    def get_available_topics(self) -> List[str]:
        """Get list of available topics with built-in vocabulary."""
        return list(self.TOPICS.keys())

    def suggest_tones_for_topic(self, topic: str) -> List[str]:
        """Suggest best tones for a given topic."""
        # Topic to tone mapping
        suggestions = {
            "coffee": ["sarcastic", "funny", "millennial"],
            "dogs": ["wholesome", "funny", "aesthetic"],
            "cats": ["sarcastic", "edgy", "funny"],
            "fitness": ["motivational", "edgy", "gen_z"],
            "mom": ["funny", "sarcastic", "wholesome"],
            "dad": ["funny", "sarcastic", "wholesome"],
            "introvert": ["sarcastic", "funny", "aesthetic"],
            "nurse": ["funny", "motivational", "edgy"],
            "teacher": ["funny", "sarcastic", "motivational"],
            "gaming": ["gen_z", "edgy", "funny"],
            "anxiety": ["sarcastic", "millennial", "gen_z"],
            "work": ["sarcastic", "edgy", "millennial"],
        }

        return suggestions.get(topic.lower(), ["funny", "sarcastic", "motivational"])


# Singleton instance
ai_phrase_generator = AIPhraseGenerator()

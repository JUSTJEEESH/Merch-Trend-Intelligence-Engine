"""Bulk idea generator - creates hundreds of merch phrase ideas at once."""
import random
import re
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime

from .bestseller_patterns import (
    BESTSELLER_TEMPLATES,
    TRENDING_TOPICS,
    CLASSIC_BESTSELLERS,
    NICHE_BESTSELLERS,
    NICHE_DATA,
    WORD_VARIATIONS,
    get_all_bestseller_phrases,
    get_niche_topics,
    get_niche_data,
    get_niche_competition,
    get_niche_bsr,
    get_all_niches,
)
from .variation_generator import VariationGenerator

logger = logging.getLogger(__name__)


class IdeaGenerator:
    """Generate hundreds of merch phrase ideas using proven patterns."""

    def __init__(self):
        self.variation_generator = VariationGenerator()
        self._trademark_checker = None

    def generate_ideas(
        self,
        count: int = 200,
        niches: Optional[List[str]] = None,
        include_classics: bool = True,
        include_generated: bool = True,
        include_variations: bool = True,
        creativity_level: str = "medium",  # low, medium, high
    ) -> Dict[str, Any]:
        """
        Generate a large batch of phrase ideas.

        Args:
            count: Number of ideas to generate (max 500)
            niches: Optional list of niches to focus on (STRICT - only these niches)
            include_classics: Include proven bestseller phrases
            include_generated: Include pattern-generated phrases
            include_variations: Include variations of bestsellers
            creativity_level: How creative/experimental to be

        Returns:
            Dictionary with categorized ideas and metadata
        """
        count = min(count, 500)  # Cap at 500
        ideas = []
        categories = {}

        # Normalize niches
        target_niches = None
        if niches:
            if isinstance(niches, str):
                target_niches = [niches.lower()]
            else:
                target_niches = [n.lower() for n in niches]

        # 1. Add classic bestsellers (proven winners)
        if include_classics:
            classics = self._get_classic_bestsellers(target_niches)
            for phrase in classics:
                detected = self._detect_niche(phrase)
                idea = self._create_idea(phrase, "classic", detected)
                ideas.append(idea)
            categories["classics"] = len(classics)

        # 2. Generate from templates + topics (STRICT niche mode)
        if include_generated:
            generated = self._generate_from_templates(
                count=count,  # Generate more to ensure enough after filtering
                niches=target_niches,
                creativity=creativity_level
            )
            ideas.extend(generated)
            categories["generated"] = len(generated)

        # 3. Generate variations of top phrases
        if include_variations:
            variations = self._generate_variations(
                ideas[:50],  # Use top 50 as seeds
                count=count // 4
            )
            ideas.extend(variations)
            categories["variations"] = len(variations)

        # 4. Generate trending combinations
        trending = self._generate_trending_combinations(
            count=count // 4,
            niches=target_niches
        )
        ideas.extend(trending)
        categories["trending"] = len(trending)

        # STRICT NICHE FILTERING: Only keep ideas that match target niches
        if target_niches:
            ideas = [
                idea for idea in ideas
                if idea.get("niche", "general").lower() in target_niches
                or idea.get("niche", "general") == "general"
            ]
            # Re-detect niches for general ones and filter more strictly
            filtered_ideas = []
            for idea in ideas:
                phrase_lower = idea["phrase"].lower()
                # Check if phrase contains any topic from target niches
                matches_niche = False
                for niche in target_niches:
                    niche_topics = get_niche_topics(niche)
                    for topic in niche_topics:
                        if topic.lower() in phrase_lower:
                            idea["niche"] = niche
                            matches_niche = True
                            break
                    if matches_niche:
                        break
                if matches_niche:
                    filtered_ideas.append(idea)
            ideas = filtered_ideas

        # Deduplicate while preserving order
        seen = set()
        unique_ideas = []
        for idea in ideas:
            normalized = idea["phrase"].lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_ideas.append(idea)

        # Sort by potential score
        unique_ideas.sort(key=lambda x: x.get("score", 0), reverse=True)

        # Limit to requested count
        unique_ideas = unique_ideas[:count]

        # Group by category for UI
        by_category = self._group_by_category(unique_ideas)
        by_niche = self._group_by_niche(unique_ideas)

        # Get niche metadata
        niche_info = {}
        if target_niches:
            for niche in target_niches:
                data = get_niche_data(niche)
                if data:
                    niche_info[niche] = {
                        "competition": data["competition"],
                        "avg_bsr": data["avg_bsr"],
                    }

        return {
            "total": len(unique_ideas),
            "generated_at": datetime.utcnow().isoformat(),
            "ideas": unique_ideas,
            "by_category": by_category,
            "by_niche": by_niche,
            "niche_info": niche_info,
            "stats": {
                "categories": categories,
                "unique_niches": len(by_niche),
            }
        }

    def _get_classic_bestsellers(self, niches: Optional[List[str]] = None) -> List[str]:
        """Get classic bestseller phrases, optionally filtered by niche."""
        phrases = list(CLASSIC_BESTSELLERS)

        if niches:
            # Add niche-specific bestsellers
            for niche in niches:
                niche_lower = niche.lower()
                if niche_lower in NICHE_BESTSELLERS:
                    phrases.extend(NICHE_BESTSELLERS[niche_lower])
        else:
            # Add all niche bestsellers
            for niche_phrases in NICHE_BESTSELLERS.values():
                phrases.extend(niche_phrases)

        random.shuffle(phrases)
        return phrases

    def _generate_from_templates(
        self,
        count: int,
        niches: Optional[List[str]] = None,
        creativity: str = "medium"
    ) -> List[Dict[str, Any]]:
        """Generate phrases by combining templates with topics."""
        ideas = []
        templates = list(BESTSELLER_TEMPLATES)

        # Filter topics by niche if specified
        if niches:
            topics = self._get_topics_for_niches(niches)
        else:
            topics = list(TRENDING_TOPICS)

        # Creativity affects how we combine things
        if creativity == "high":
            # More random, experimental combinations
            random.shuffle(templates)
            random.shuffle(topics)
            iterations = count * 2
        elif creativity == "low":
            # Stick to proven combinations
            templates = templates[:50]  # Top patterns only
            topics = topics[:30]  # Popular topics only
            iterations = count
        else:
            iterations = int(count * 1.5)

        for _ in range(iterations):
            template = random.choice(templates)
            topic = random.choice(topics)

            # Generate the phrase
            phrase = self._fill_template(template, topic)
            if phrase:
                niche = self._detect_niche(phrase)
                idea = self._create_idea(phrase, "generated", niche)
                ideas.append(idea)

            if len(ideas) >= count:
                break

        return ideas

    def _fill_template(self, template: str, topic: str) -> Optional[str]:
        """Fill a template with a topic, handling verb forms."""
        try:
            phrase = template.replace("{X}", topic)

            # Handle verb forms
            if "{X}" not in template:
                return None

            # Convert to gerund for patterns like "I'd rather be {X}"
            if "be {X}" in template.lower():
                gerund = self._to_gerund(topic)
                phrase = template.replace("{X}", gerund)

            # Handle "to {X}" patterns
            elif "to {X}" in template.lower():
                verb = self._to_base_verb(topic)
                phrase = template.replace("{X}", verb)

            return phrase.strip()

        except Exception:
            return None

    def _generate_variations(
        self,
        seed_ideas: List[Dict[str, Any]],
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate variations of seed phrases."""
        ideas = []

        for seed in seed_ideas:
            if len(ideas) >= count:
                break

            try:
                variations = self.variation_generator.generate(
                    seed["phrase"],
                    count=3
                )
                for var in variations:
                    idea = self._create_idea(
                        var["text"],
                        "variation",
                        seed.get("niche", "general"),
                        source_phrase=seed["phrase"]
                    )
                    ideas.append(idea)

            except Exception as e:
                logger.debug(f"Variation error: {e}")
                continue

        return ideas[:count]

    def _generate_trending_combinations(
        self,
        count: int,
        niches: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Generate combinations based on trending patterns."""
        ideas = []

        # Hot combinations that work across niches
        hot_patterns = [
            "Currently in my {X} era",
            "{X} is my Roman Empire",
            "Tell me you love {X} without telling me",
            "POV: you love {X}",
            "{X} core",
            "Very demure very {X}",
            "Main character {X} energy",
            "No thoughts just {X}",
            "Unhinged {X} behavior",
            "Feral {X} girl",
            "Chaotic {X} energy",
            "{X} girlie",
            "That {X} girl",
            "In my {X} feels",
            "Soft launch {X}",
            "Hard launch {X}",
            "{X} coded",
            "Delulu about {X}",
            "{X} pilled",
            "Chronically online {X}",
        ]

        topics = self._get_topics_for_niches(niches) if niches else TRENDING_TOPICS

        for pattern in hot_patterns:
            for topic in random.sample(topics, min(5, len(topics))):
                phrase = pattern.replace("{X}", topic)
                idea = self._create_idea(phrase, "trending", self._detect_niche(phrase))
                ideas.append(idea)

                if len(ideas) >= count:
                    break

            if len(ideas) >= count:
                break

        return ideas

    def _get_topics_for_niches(self, niches: List[str], strict: bool = True) -> List[str]:
        """Get relevant topics for given niches.

        Args:
            niches: List of niche names
            strict: If True, ONLY return topics for specified niches (no general topics)
        """
        topics = []
        for niche in niches:
            niche_lower = niche.lower()
            # Get topics from comprehensive NICHE_DATA
            niche_topics = get_niche_topics(niche_lower)
            if niche_topics:
                topics.extend(niche_topics)
            # Also add the niche itself
            topics.append(niche_lower)

        # STRICT MODE: Only use niche-specific topics, no general mixing
        if not strict:
            # Add some general topics only if not in strict mode
            topics.extend(random.sample(TRENDING_TOPICS, min(20, len(TRENDING_TOPICS))))

        return list(set(topics))

    def _create_idea(
        self,
        phrase: str,
        category: str,
        niche: str,
        source_phrase: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an idea dictionary with metadata including competition and BSR."""
        # Calculate potential score based on phrase characteristics
        score = self._calculate_potential(phrase)

        # Get competition and BSR data for the niche
        niche_data = get_niche_data(niche)
        competition = niche_data["competition"] if niche_data else "unknown"
        avg_bsr = niche_data["avg_bsr"] if niche_data else None

        # Estimate BSR with some variance
        estimated_bsr = None
        if avg_bsr:
            # Higher scoring phrases get better BSR estimates
            score_factor = 1 - (score / 200)  # 0.5 to 1.0 range
            variance = random.uniform(0.7, 1.3)
            estimated_bsr = int(avg_bsr * score_factor * variance)

        return {
            "phrase": phrase,
            "category": category,
            "niche": niche,
            "score": score,
            "word_count": len(phrase.split()),
            "char_count": len(phrase),
            "source": source_phrase,
            "competition": competition,
            "estimated_bsr": estimated_bsr,
            "discovered_at": datetime.utcnow().isoformat(),
        }

    def _calculate_potential(self, phrase: str) -> int:
        """Calculate a potential score (0-100) for a phrase."""
        score = 50  # Base score

        words = phrase.lower().split()
        word_count = len(words)

        # Optimal length (3-6 words)
        if 3 <= word_count <= 6:
            score += 20
        elif word_count <= 8:
            score += 10
        elif word_count > 10:
            score -= 10

        # Bonus for emotional words
        emotional_words = ["love", "obsessed", "need", "happy", "life", "best", "proud"]
        if any(w in words for w in emotional_words):
            score += 10

        # Bonus for action words
        action_words = ["born", "made", "built", "powered", "fueled", "running"]
        if any(w in words for w in action_words):
            score += 10

        # Bonus for humor indicators
        humor_words = ["probably", "sorry", "can't", "don't", "won't", "adulting"]
        if any(w in words for w in humor_words):
            score += 5

        # Penalty for being too generic
        generic_words = ["the", "a", "an", "is", "are", "to", "for"]
        generic_count = sum(1 for w in words if w in generic_words)
        if generic_count > word_count // 2:
            score -= 10

        return max(0, min(100, score))

    def _detect_niche(self, phrase: str) -> str:
        """Detect the likely niche of a phrase using comprehensive NICHE_DATA."""
        phrase_lower = phrase.lower()

        # Check against all niches in NICHE_DATA
        for niche, data in NICHE_DATA.items():
            topics = data.get("topics", [])
            for topic in topics:
                # Check if topic appears as a word in the phrase
                if topic.lower() in phrase_lower:
                    return niche

        return "general"

    def _group_by_category(self, ideas: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group ideas by category."""
        groups = {}
        for idea in ideas:
            cat = idea.get("category", "other")
            if cat not in groups:
                groups[cat] = []
            groups[cat].append(idea)
        return groups

    def _group_by_niche(self, ideas: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group ideas by niche."""
        groups = {}
        for idea in ideas:
            niche = idea.get("niche", "general")
            if niche not in groups:
                groups[niche] = []
            groups[niche].append(idea)
        return groups

    def _to_gerund(self, word: str) -> str:
        """Convert word to -ing form."""
        word = word.lower().strip()

        gerunds = {
            "hike": "hiking", "fish": "fishing", "camp": "camping",
            "hunt": "hunting", "run": "running", "swim": "swimming",
            "game": "gaming", "code": "coding", "cook": "cooking",
            "read": "reading", "lift": "lifting", "bike": "biking",
            "golf": "golfing", "craft": "crafting", "garden": "gardening",
        }

        if word in gerunds:
            return gerunds[word]

        if word.endswith("ing"):
            return word
        if word.endswith("e"):
            return word[:-1] + "ing"
        return word + "ing"

    def _to_base_verb(self, word: str) -> str:
        """Convert to base verb form."""
        word = word.lower().strip()

        if word.endswith("ing"):
            # Remove -ing and handle special cases
            base = word[:-3]
            if base.endswith("mm") or base.endswith("nn"):
                return base[:-1]  # running -> run
            if len(base) > 2:
                return base
        return word

    def quick_generate(self, topic: str, count: int = 50) -> List[str]:
        """Quickly generate ideas for a single topic."""
        ideas = []

        for template in BESTSELLER_TEMPLATES:
            phrase = self._fill_template(template, topic)
            if phrase and phrase not in ideas:
                ideas.append(phrase)

            if len(ideas) >= count:
                break

        return ideas

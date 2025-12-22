"""Pattern detection service using embeddings and clustering."""
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import json

from ...config import settings

logger = logging.getLogger(__name__)


class PatternDetector:
    """Detect reusable phrase patterns using embeddings and clustering."""

    # Known merch phrase patterns
    KNOWN_PATTERNS = [
        {
            "template": "I'm not {WORD}, I'm {WORD}",
            "regex": r"i'?m not (\w+),?\s*i'?m (\w+)",
            "description": "Contrast statement pattern",
            "examples": ["I'm not lazy, I'm energy efficient", "I'm not short, I'm fun-sized"]
        },
        {
            "template": "Tell me you're {PHRASE} without telling me",
            "regex": r"tell me you'?re? (.+) without telling me",
            "description": "TikTok-style reveal pattern",
            "examples": ["Tell me you're a mom without telling me"]
        },
        {
            "template": "Powered by {PHRASE}",
            "regex": r"powered by (.+)",
            "description": "Energy source pattern",
            "examples": ["Powered by coffee and anxiety", "Powered by spite"]
        },
        {
            "template": "I used to {PHRASE} now I {PHRASE}",
            "regex": r"i used to (.+) now i (.+)",
            "description": "Before/after transformation pattern",
            "examples": ["I used to be cool now I'm just cold"]
        },
        {
            "template": "{WORD} is my cardio",
            "regex": r"(\w+) is my cardio",
            "description": "Activity as exercise pattern",
            "examples": ["Shopping is my cardio", "Running late is my cardio"]
        },
        {
            "template": "{WORD} loading please wait",
            "regex": r"(\w+) loading,?\s*please wait",
            "description": "Computer loading pattern",
            "examples": ["Dad joke loading please wait", "Patience loading please wait"]
        },
        {
            "template": "{WORD} mode activated",
            "regex": r"(\w+) mode activated",
            "description": "Mode activation pattern",
            "examples": ["Beast mode activated", "Mom mode activated"]
        },
        {
            "template": "Professional {WORD}",
            "regex": r"^professional (\w+)$",
            "description": "Professional title pattern",
            "examples": ["Professional overthinker", "Professional napper"]
        },
        {
            "template": "{WORD} whisperer",
            "regex": r"(\w+) whisperer",
            "description": "Expert/whisperer pattern",
            "examples": ["Dog whisperer", "Plant whisperer", "Baby whisperer"]
        },
        {
            "template": "{WORD} is my love language",
            "regex": r"(\w+) is my love language",
            "description": "Love language pattern",
            "examples": ["Sarcasm is my love language", "Food is my love language"]
        },
        {
            "template": "Sorry I can't I have {PHRASE}",
            "regex": r"sorry i can'?t i have (.+)",
            "description": "Excuse pattern",
            "examples": ["Sorry I can't I have plans with my dog"]
        },
        {
            "template": "Life is better with {PHRASE}",
            "regex": r"life is better with (.+)",
            "description": "Life improvement pattern",
            "examples": ["Life is better with coffee", "Life is better with dogs"]
        },
        {
            "template": "Keep calm and {PHRASE}",
            "regex": r"keep calm and (.+)",
            "description": "Keep calm pattern (use carefully - check saturation)",
            "examples": ["Keep calm and carry on", "Keep calm and drink coffee"]
        },
        {
            "template": "{WORD} dad/mom life",
            "regex": r"(\w+) (dad|mom) life",
            "description": "Parent life pattern",
            "examples": ["Soccer mom life", "Dog dad life"]
        },
        {
            "template": "But first, {WORD}",
            "regex": r"but first,?\s*(\w+)",
            "description": "Priority pattern",
            "examples": ["But first, coffee", "But first, tacos"]
        },
    ]

    def __init__(self):
        self.embedder = None
        self._init_embedder()

    def _init_embedder(self):
        """Initialize sentence transformer for embeddings."""
        try:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer loaded")
        except ImportError:
            logger.warning("sentence-transformers not installed")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")

    def detect_pattern(self, phrase: str) -> Optional[Dict[str, Any]]:
        """
        Detect if a phrase matches a known pattern.

        Returns:
            Pattern info dict if matched, None otherwise
        """
        normalized = phrase.lower().strip()

        for pattern in self.KNOWN_PATTERNS:
            match = re.search(pattern["regex"], normalized, re.IGNORECASE)
            if match:
                return {
                    "template": pattern["template"],
                    "description": pattern["description"],
                    "variables": list(match.groups()),
                    "examples": pattern["examples"]
                }

        return None

    def fill_pattern(self, template: str, variables: List[str]) -> str:
        """
        Fill a pattern template with variables.

        Args:
            template: Pattern template like "I'm not {WORD}, I'm {WORD}"
            variables: List of values to fill in

        Returns:
            Filled phrase
        """
        result = template
        var_index = 0

        # Replace {WORD} and {PHRASE} placeholders
        while '{WORD}' in result or '{PHRASE}' in result:
            if var_index >= len(variables):
                break

            if '{WORD}' in result:
                result = result.replace('{WORD}', variables[var_index], 1)
            elif '{PHRASE}' in result:
                result = result.replace('{PHRASE}', variables[var_index], 1)

            var_index += 1

        return result

    def cluster_phrases(
        self,
        phrases: List[str],
        n_clusters: int = 10
    ) -> Dict[int, List[str]]:
        """
        Cluster similar phrases using embeddings.

        Args:
            phrases: List of phrases to cluster
            n_clusters: Number of clusters

        Returns:
            Dictionary mapping cluster ID to list of phrases
        """
        if not self.embedder or len(phrases) < n_clusters:
            return {0: phrases}

        try:
            from sklearn.cluster import KMeans
            import numpy as np

            # Generate embeddings
            embeddings = self.embedder.encode(phrases)

            # Cluster
            n_clusters = min(n_clusters, len(phrases))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)

            # Group phrases by cluster
            clusters = defaultdict(list)
            for phrase, label in zip(phrases, labels):
                clusters[int(label)].append(phrase)

            return dict(clusters)

        except Exception as e:
            logger.error(f"Clustering failed: {e}")
            return {0: phrases}

    def find_similar_phrases(
        self,
        query: str,
        phrases: List[str],
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Find phrases similar to a query.

        Args:
            query: Query phrase
            phrases: List of phrases to search
            top_k: Number of results to return

        Returns:
            List of (phrase, similarity_score) tuples
        """
        if not self.embedder or not phrases:
            return []

        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            # Encode query and phrases
            query_embedding = self.embedder.encode([query])
            phrase_embeddings = self.embedder.encode(phrases)

            # Calculate similarities
            similarities = cosine_similarity(query_embedding, phrase_embeddings)[0]

            # Get top-k
            top_indices = np.argsort(similarities)[::-1][:top_k]

            return [
                (phrases[i], float(similarities[i]))
                for i in top_indices
            ]

        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    def extract_pattern_from_cluster(
        self,
        phrases: List[str]
    ) -> Optional[str]:
        """
        Try to extract a common pattern from a cluster of similar phrases.

        Args:
            phrases: List of similar phrases

        Returns:
            Pattern template if found, None otherwise
        """
        if len(phrases) < 3:
            return None

        # Tokenize all phrases
        tokenized = [phrase.lower().split() for phrase in phrases]

        # Find common words at each position
        min_len = min(len(tokens) for tokens in tokenized)

        pattern_parts = []
        for pos in range(min_len):
            words_at_pos = [tokens[pos] for tokens in tokenized if pos < len(tokens)]

            # If same word in most phrases, it's a fixed part
            from collections import Counter
            word_counts = Counter(words_at_pos)
            most_common_word, count = word_counts.most_common(1)[0]

            if count >= len(phrases) * 0.7:  # 70% agreement
                pattern_parts.append(most_common_word)
            else:
                pattern_parts.append("{WORD}")

        if "{WORD}" not in pattern_parts:
            return None

        return " ".join(pattern_parts)

    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """Get all known patterns."""
        return [
            {
                "template": p["template"],
                "description": p["description"],
                "examples": p["examples"],
                "variable_count": p["template"].count("{")
            }
            for p in self.KNOWN_PATTERNS
        ]

    def suggest_pattern_variations(
        self,
        template: str,
        niche: str = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest variable values for a pattern based on niche.

        Args:
            template: Pattern template
            niche: Optional niche to tailor suggestions

        Returns:
            List of suggested phrase variations
        """
        # Niche-specific word banks
        niche_words = {
            "fitness": ["gym", "gains", "protein", "cardio", "weights", "sweat"],
            "coffee": ["caffeine", "espresso", "latte", "beans", "brew"],
            "dogs": ["bark", "fetch", "treats", "walks", "puppy", "paws"],
            "cats": ["meow", "nap", "purr", "scratches", "whiskers"],
            "gaming": ["respawn", "level", "quest", "loot", "noob", "pro"],
            "programming": ["code", "debug", "deploy", "coffee", "sleep"],
            "parenting": ["kids", "sleep", "chaos", "love", "patience"],
            "fishing": ["catch", "bait", "reel", "tackle", "bass"],
            "nursing": ["scrubs", "coffee", "patience", "shots", "vitals"],
        }

        # General funny words
        general_words = [
            "coffee", "wine", "tacos", "pizza", "naps", "sarcasm",
            "anxiety", "chaos", "snacks", "drama", "silence"
        ]

        # Get words for this niche
        words = niche_words.get(niche, []) + general_words

        suggestions = []
        var_count = template.count("{WORD}") + template.count("{PHRASE}")

        # Generate combinations
        import itertools
        for combo in itertools.combinations(words, var_count):
            filled = self.fill_pattern(template, list(combo))
            suggestions.append({
                "text": filled,
                "variables": list(combo),
                "niche": niche
            })

            if len(suggestions) >= 10:
                break

        return suggestions

"""NLP phrase extraction service using spaCy."""
import re
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from collections import Counter

from ...config import settings

logger = logging.getLogger(__name__)


class NLPExtractor:
    """Extract and normalize phrases from text using NLP."""

    # Stop words to filter out
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
        'which', 'who', 'whom', 'when', 'where', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'just', 'also', 'now', 'here', 'there', 'then', 'once', 'any', 'am',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him', 'us',
        'them', 'if', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
        'further', 'while', 'www', 'http', 'https', 'com'
    }

    # POS tags to keep for phrase extraction
    VALID_POS_TAGS = {'NOUN', 'PROPN', 'ADJ', 'VERB', 'ADV'}

    def __init__(self):
        self.nlp = None
        self._init_spacy()

    def _init_spacy(self):
        """Initialize spaCy model."""
        try:
            import spacy
            self.nlp = spacy.load(settings.SPACY_MODEL)
            logger.info(f"spaCy model '{settings.SPACY_MODEL}' loaded")
        except OSError:
            logger.warning(f"spaCy model '{settings.SPACY_MODEL}' not found. Run: python -m spacy download en_core_web_sm")
        except Exception as e:
            logger.error(f"Failed to load spaCy: {e}")

    def normalize_text(self, text: str) -> str:
        """Normalize text for consistent storage and comparison."""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)

        # Remove special characters but keep apostrophes and basic punctuation
        text = re.sub(r'[^\w\s\'\-]', ' ', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text.strip()

    def extract_phrases(
        self,
        text: str,
        source_type: str = "unknown",
        source_context: str = "",
        db = None
    ) -> List[Dict[str, Any]]:
        """
        Extract meaningful phrases from text.

        Args:
            text: Input text to extract phrases from
            source_type: Type of source (reddit, amazon, etc.)
            source_context: Additional context about the source
            db: Database session for storing phrases

        Returns:
            List of extracted phrase dictionaries
        """
        if not text or len(text.strip()) < 5:
            return []

        phrases = []
        normalized = self.normalize_text(text)

        # Extract n-grams
        ngrams = self._extract_ngrams(normalized)

        # If spaCy available, also extract noun phrases
        if self.nlp:
            doc = self.nlp(text)
            noun_phrases = self._extract_noun_phrases(doc)
            ngrams.extend(noun_phrases)

        # Deduplicate and filter
        seen = set()
        for phrase in ngrams:
            normalized_phrase = self.normalize_text(phrase)

            # Skip if already seen or too short/long
            if normalized_phrase in seen:
                continue
            if not self._is_valid_phrase(normalized_phrase):
                continue

            seen.add(normalized_phrase)

            phrase_data = {
                "text": phrase,
                "normalized_text": normalized_phrase,
                "word_count": len(normalized_phrase.split()),
                "source_type": source_type,
                "source_context": source_context,
                "extracted_at": datetime.utcnow().isoformat()
            }

            # Check if it's a pattern
            pattern = self.extract_pattern(phrase)
            if pattern:
                phrase_data["is_pattern"] = True
                phrase_data["pattern_template"] = pattern

            phrases.append(phrase_data)

            # Store in database if provided
            if db:
                self._store_phrase(phrase_data, source_type, db)

        return phrases

    def _extract_ngrams(self, text: str) -> List[str]:
        """Extract n-grams from text."""
        words = text.split()
        ngrams = []

        for n in range(settings.MIN_PHRASE_LENGTH, settings.MAX_PHRASE_LENGTH + 1):
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i+n])
                ngrams.append(ngram)

        return ngrams

    def _extract_noun_phrases(self, doc) -> List[str]:
        """Extract noun phrases using spaCy."""
        phrases = []

        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip()
            if len(phrase.split()) >= settings.MIN_PHRASE_LENGTH:
                phrases.append(phrase)

        return phrases

    def _is_valid_phrase(self, phrase: str) -> bool:
        """Check if a phrase is valid for extraction."""
        words = phrase.split()

        # Check length
        if len(words) < settings.MIN_PHRASE_LENGTH:
            return False
        if len(words) > settings.MAX_PHRASE_LENGTH:
            return False

        # Check if all words are stop words
        non_stop_words = [w for w in words if w not in self.STOP_WORDS]
        if len(non_stop_words) < 1:
            return False

        # Check if phrase is too short in characters
        if len(phrase) < 5:
            return False

        # Check for nonsense patterns
        if re.match(r'^[\d\s]+$', phrase):  # Only numbers
            return False

        return True

    def extract_pattern(self, phrase: str) -> Optional[str]:
        """
        Detect if a phrase follows a reusable pattern.

        Returns pattern template if found, None otherwise.
        """
        # Common merch phrase patterns
        patterns = [
            # "I'm not X, I'm Y"
            (r"i'?m not (\w+),?\s*i'?m (\w+)", "I'm not {WORD}, I'm {WORD}"),

            # "Tell me you're X without telling me"
            (r"tell me you'?re? (.+) without telling me", "Tell me you're {PHRASE} without telling me"),

            # "Powered by X"
            (r"powered by (.+)", "Powered by {PHRASE}"),

            # "I used to X now I Y"
            (r"i used to (.+) now i (.+)", "I used to {PHRASE} now I {PHRASE}"),

            # "X is my cardio"
            (r"(\w+) is my cardio", "{WORD} is my cardio"),

            # "X loading please wait"
            (r"(\w+) loading,?\s*please wait", "{WORD} loading please wait"),

            # "X mode activated"
            (r"(\w+) mode activated", "{WORD} mode activated"),

            # "Professional X"
            (r"professional (\w+)", "Professional {WORD}"),

            # "X whisperer"
            (r"(\w+) whisperer", "{WORD} whisperer"),

            # "X is my love language"
            (r"(\w+) is my love language", "{WORD} is my love language"),
        ]

        normalized = self.normalize_text(phrase)

        for regex, template in patterns:
            if re.search(regex, normalized, re.IGNORECASE):
                return template

        return None

    def _store_phrase(self, phrase_data: Dict, source_type: str, db) -> None:
        """Store extracted phrase in database."""
        from ...models import Phrase, Source, PhraseMetrics

        try:
            # Get or create source
            source = db.query(Source).filter(Source.name == source_type).first()
            if not source:
                source = Source(name=source_type, source_type=source_type)
                db.add(source)
                db.flush()

            # Check if phrase exists
            existing = db.query(Phrase).filter(
                Phrase.normalized_text == phrase_data["normalized_text"],
                Phrase.source_id == source.id
            ).first()

            if existing:
                # Update frequency
                existing.frequency += 1
                existing.last_seen = datetime.utcnow()
            else:
                # Create new phrase
                phrase = Phrase(
                    text=phrase_data["text"],
                    normalized_text=phrase_data["normalized_text"],
                    word_count=phrase_data["word_count"],
                    source_id=source.id,
                    source_context=phrase_data.get("source_context", ""),
                    is_pattern=phrase_data.get("is_pattern", False),
                    pattern_template=phrase_data.get("pattern_template")
                )
                db.add(phrase)
                db.flush()

                # Create metrics entry
                metrics = PhraseMetrics(phrase_id=phrase.id)
                db.add(metrics)

            db.commit()

        except Exception as e:
            logger.error(f"Failed to store phrase: {e}")
            db.rollback()

    def get_word_frequency(self, texts: List[str]) -> Dict[str, int]:
        """Get word frequency from a list of texts."""
        all_words = []

        for text in texts:
            normalized = self.normalize_text(text)
            words = [w for w in normalized.split() if w not in self.STOP_WORDS]
            all_words.extend(words)

        return dict(Counter(all_words).most_common(100))

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract top keywords from text using TF-IDF-like scoring."""
        if not self.nlp:
            # Fallback to simple word frequency
            words = self.normalize_text(text).split()
            filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 2]
            counter = Counter(filtered)
            return [word for word, _ in counter.most_common(top_n)]

        doc = self.nlp(text)
        keywords = []

        for token in doc:
            if (token.pos_ in self.VALID_POS_TAGS and
                token.text.lower() not in self.STOP_WORDS and
                len(token.text) > 2):
                keywords.append(token.lemma_.lower())

        counter = Counter(keywords)
        return [word for word, _ in counter.most_common(top_n)]

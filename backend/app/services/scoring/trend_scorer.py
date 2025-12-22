"""Trend scoring engine."""
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func

from ...config import settings

logger = logging.getLogger(__name__)


class TrendScorer:
    """
    Calculate Trend Opportunity Score (0-100) for phrases.

    Weighted Formula:
    - Velocity (growth rate): 30%
    - Novelty: 25%
    - Low saturation: 25%
    - Cross-platform presence: 10%
    - Phrase length suitability: 10%
    """

    def __init__(self):
        self.weights = {
            "velocity": settings.WEIGHT_VELOCITY,
            "novelty": settings.WEIGHT_NOVELTY,
            "saturation": settings.WEIGHT_SATURATION,
            "cross_platform": settings.WEIGHT_CROSS_PLATFORM,
            "length": settings.WEIGHT_LENGTH
        }

    def calculate_score(self, phrase: str, db=None) -> Dict[str, Any]:
        """
        Calculate trend opportunity score for a phrase.

        Args:
            phrase: Phrase to score
            db: Database session for historical data

        Returns:
            Dictionary with overall score and component scores
        """
        from ...models import Phrase, PhraseMetrics

        result = {
            "score": 0.0,
            "components": {},
            "explanation": []
        }

        # Get phrase data if in database
        phrase_data = None
        metrics = None
        if db:
            phrase_data = db.query(Phrase).filter(
                Phrase.normalized_text == phrase.lower()
            ).first()
            if phrase_data:
                metrics = phrase_data.metrics

        # Calculate component scores
        velocity_score = self._calculate_velocity_score(phrase_data, metrics, db)
        novelty_score = self._calculate_novelty_score(phrase_data, metrics)
        saturation_score = self._calculate_saturation_score(phrase_data, metrics)
        cross_platform_score = self._calculate_cross_platform_score(phrase_data, metrics)
        length_score = self._calculate_length_score(phrase)

        # Store components
        result["components"] = {
            "velocity": velocity_score,
            "novelty": novelty_score,
            "saturation": saturation_score,
            "cross_platform": cross_platform_score,
            "length": length_score
        }

        # Calculate weighted total
        result["score"] = (
            velocity_score * self.weights["velocity"] +
            novelty_score * self.weights["novelty"] +
            saturation_score * self.weights["saturation"] +
            cross_platform_score * self.weights["cross_platform"] +
            length_score * self.weights["length"]
        )

        # Add explanations
        result["explanation"] = self._generate_explanation(result["components"])

        return result

    def _calculate_velocity_score(
        self,
        phrase_data,
        metrics,
        db
    ) -> float:
        """
        Calculate velocity score based on growth rate.

        High velocity = phrase is gaining traction quickly
        """
        if not phrase_data or not db:
            return 50.0  # Neutral score for new/unknown phrases

        from ...models import PhraseHistory

        try:
            # Get frequency history
            week_ago = datetime.utcnow() - timedelta(days=7)
            two_weeks_ago = datetime.utcnow() - timedelta(days=14)

            # Get this week's total
            this_week = db.query(func.sum(PhraseHistory.frequency)).filter(
                PhraseHistory.phrase_id == phrase_data.id,
                PhraseHistory.date >= week_ago
            ).scalar() or 0

            # Get last week's total
            last_week = db.query(func.sum(PhraseHistory.frequency)).filter(
                PhraseHistory.phrase_id == phrase_data.id,
                PhraseHistory.date >= two_weeks_ago,
                PhraseHistory.date < week_ago
            ).scalar() or 0

            if last_week == 0:
                if this_week > 0:
                    return 90.0  # New phrase with activity
                return 50.0

            # Calculate growth rate
            growth_rate = (this_week - last_week) / last_week

            # Convert to 0-100 score
            # Breakout growth (>100%) = 100
            # Strong growth (50-100%) = 80-99
            # Moderate growth (10-50%) = 60-80
            # Slight growth (0-10%) = 50-60
            # Decline = 0-50

            if growth_rate >= 1.0:
                return 100.0
            elif growth_rate >= 0.5:
                return 80 + (growth_rate - 0.5) * 40
            elif growth_rate >= 0.1:
                return 60 + (growth_rate - 0.1) * 50
            elif growth_rate >= 0:
                return 50 + growth_rate * 100
            else:
                return max(0, 50 + growth_rate * 50)

        except Exception as e:
            logger.error(f"Velocity calculation failed: {e}")
            return 50.0

    def _calculate_novelty_score(self, phrase_data, metrics) -> float:
        """
        Calculate novelty score based on how new the phrase is.

        Newer phrases = higher novelty
        """
        if not phrase_data:
            return 80.0  # Unknown phrases assumed relatively new

        days_old = (datetime.utcnow() - phrase_data.first_seen).days

        # Score based on age
        # < 7 days = 90-100
        # 7-14 days = 75-90
        # 14-30 days = 50-75
        # 30-60 days = 25-50
        # > 60 days = 0-25

        if days_old < 7:
            return 90 + (7 - days_old) * 10 / 7
        elif days_old < 14:
            return 75 + (14 - days_old) * 15 / 7
        elif days_old < 30:
            return 50 + (30 - days_old) * 25 / 16
        elif days_old < 60:
            return 25 + (60 - days_old) * 25 / 30
        else:
            return max(0, 25 - (days_old - 60) / 10)

    def _calculate_saturation_score(self, phrase_data, metrics) -> float:
        """
        Calculate saturation score (inverted - low saturation = high score).

        Based on Amazon and Etsy search results.
        """
        if not metrics:
            return 70.0  # Unknown = assume moderate opportunity

        amazon_results = metrics.amazon_results or 0
        etsy_results = metrics.etsy_results or 0
        total_results = amazon_results + etsy_results

        # Score based on existing competition
        # 0 results = 100 (virgin territory)
        # 1-10 results = 80-99 (low competition)
        # 11-50 results = 60-80 (moderate)
        # 51-200 results = 40-60 (high)
        # 201-1000 results = 20-40 (very high)
        # >1000 results = 0-20 (saturated)

        if total_results == 0:
            return 100.0
        elif total_results <= 10:
            return 80 + (10 - total_results) * 2
        elif total_results <= 50:
            return 60 + (50 - total_results) * 0.5
        elif total_results <= 200:
            return 40 + (200 - total_results) * 0.13
        elif total_results <= 1000:
            return 20 + (1000 - total_results) * 0.025
        else:
            return max(0, 20 - (total_results - 1000) * 0.01)

    def _calculate_cross_platform_score(self, phrase_data, metrics) -> float:
        """
        Calculate cross-platform presence score.

        Phrase appearing on multiple platforms = validation
        """
        if not metrics or not metrics.platforms_found:
            return 30.0  # Single platform assumed

        try:
            import json
            platforms = json.loads(metrics.platforms_found)
            platform_count = len(platforms)

            # Score based on platform diversity
            # 1 platform = 30
            # 2 platforms = 60
            # 3 platforms = 80
            # 4+ platforms = 100

            if platform_count >= 4:
                return 100.0
            elif platform_count == 3:
                return 80.0
            elif platform_count == 2:
                return 60.0
            else:
                return 30.0

        except Exception:
            return 30.0

    def _calculate_length_score(self, phrase: str) -> float:
        """
        Calculate phrase length suitability score.

        Optimal merch phrase length: 3-6 words
        """
        words = phrase.split()
        word_count = len(words)
        char_count = len(phrase)

        # Word count scoring
        if 3 <= word_count <= 6:
            word_score = 100.0
        elif word_count == 2 or word_count == 7:
            word_score = 80.0
        elif word_count == 1 or word_count == 8:
            word_score = 50.0
        else:
            word_score = 20.0

        # Character count scoring (for fitting on products)
        if 15 <= char_count <= 40:
            char_score = 100.0
        elif 10 <= char_count < 15 or 40 < char_count <= 50:
            char_score = 70.0
        elif char_count > 50:
            char_score = 30.0
        else:
            char_score = 50.0

        return (word_score + char_score) / 2

    def _generate_explanation(self, components: Dict[str, float]) -> list:
        """Generate human-readable explanations for the score."""
        explanations = []

        if components["velocity"] >= 80:
            explanations.append("High velocity - phrase is gaining traction quickly")
        elif components["velocity"] <= 30:
            explanations.append("Low velocity - phrase growth is stagnant or declining")

        if components["novelty"] >= 80:
            explanations.append("High novelty - relatively new phrase")
        elif components["novelty"] <= 30:
            explanations.append("Low novelty - phrase has been around for a while")

        if components["saturation"] >= 80:
            explanations.append("Low saturation - good opportunity, little competition")
        elif components["saturation"] <= 30:
            explanations.append("High saturation - lots of existing competition")

        if components["cross_platform"] >= 70:
            explanations.append("Strong cross-platform presence - validated trend")

        if components["length"] >= 80:
            explanations.append("Optimal phrase length for merchandise")
        elif components["length"] <= 50:
            explanations.append("Phrase length may not be ideal for merch")

        return explanations

    def update_phrase_score(self, phrase_id: int, db) -> float:
        """Update the trend score for a phrase in the database."""
        from ...models import Phrase

        phrase = db.query(Phrase).filter(Phrase.id == phrase_id).first()
        if not phrase:
            return 0.0

        result = self.calculate_score(phrase.normalized_text, db)
        phrase.trend_score = result["score"]

        # Update metrics
        if phrase.metrics:
            phrase.metrics.velocity = result["components"]["velocity"] / 100
            phrase.metrics.novelty_score = result["components"]["novelty"] / 100
            phrase.metrics.saturation_score = result["components"]["saturation"] / 100
            phrase.metrics.cross_platform_score = result["components"]["cross_platform"] / 100
            phrase.metrics.length_score = result["components"]["length"] / 100

        db.commit()
        return result["score"]

    def batch_update_scores(self, db, limit: int = 1000) -> int:
        """Update scores for multiple phrases."""
        from ...models import Phrase

        phrases = db.query(Phrase).filter(
            Phrase.is_safe == True
        ).limit(limit).all()

        updated = 0
        for phrase in phrases:
            try:
                self.update_phrase_score(phrase.id, db)
                updated += 1
            except Exception as e:
                logger.error(f"Failed to update score for phrase {phrase.id}: {e}")

        return updated

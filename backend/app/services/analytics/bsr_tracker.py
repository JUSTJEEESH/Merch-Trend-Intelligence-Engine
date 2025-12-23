"""BSR (Best Seller Rank) tracking and estimation service."""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import math

logger = logging.getLogger(__name__)


class BSRTracker:
    """
    Service for tracking and estimating BSR performance.
    Provides historical data, sales estimates, and ranking insights.
    """

    # BSR to daily sales estimation (approximate for clothing)
    BSR_SALES_MAP = [
        (1000, 25),      # BSR 1-1000: ~25 sales/day
        (5000, 10),      # BSR 1001-5000: ~10 sales/day
        (10000, 5),      # BSR 5001-10000: ~5 sales/day
        (25000, 3),      # BSR 10001-25000: ~3 sales/day
        (50000, 2),      # BSR 25001-50000: ~2 sales/day
        (100000, 1),     # BSR 50001-100000: ~1 sale/day
        (250000, 0.5),   # BSR 100001-250000: ~0.5 sales/day
        (500000, 0.2),   # BSR 250001-500000: ~0.2 sales/day
        (1000000, 0.1),  # BSR 500001-1000000: ~0.1 sales/day
    ]

    # Niche average BSRs (for estimation)
    NICHE_BSR_AVERAGES = {
        "coffee": {"avg": 15000, "low": 5000, "high": 50000, "competition": "high"},
        "dogs": {"avg": 12000, "low": 3000, "high": 40000, "competition": "high"},
        "cats": {"avg": 18000, "low": 5000, "high": 60000, "competition": "high"},
        "fitness": {"avg": 20000, "low": 8000, "high": 80000, "competition": "high"},
        "nursing": {"avg": 8000, "low": 2000, "high": 25000, "competition": "medium"},
        "teaching": {"avg": 10000, "low": 3000, "high": 35000, "competition": "medium"},
        "mom": {"avg": 6000, "low": 1500, "high": 20000, "competition": "high"},
        "dad": {"avg": 12000, "low": 4000, "high": 40000, "competition": "medium"},
        "gaming": {"avg": 25000, "low": 10000, "high": 100000, "competition": "high"},
        "hunting": {"avg": 15000, "low": 5000, "high": 50000, "competition": "medium"},
        "fishing": {"avg": 18000, "low": 6000, "high": 60000, "competition": "medium"},
        "camping": {"avg": 22000, "low": 8000, "high": 70000, "competition": "medium"},
        "beer": {"avg": 20000, "low": 7000, "high": 65000, "competition": "medium"},
        "wine": {"avg": 25000, "low": 10000, "high": 80000, "competition": "low"},
        "whiskey": {"avg": 28000, "low": 12000, "high": 90000, "competition": "low"},
        "yoga": {"avg": 16000, "low": 5000, "high": 55000, "competition": "medium"},
        "running": {"avg": 22000, "low": 8000, "high": 75000, "competition": "medium"},
        "golf": {"avg": 30000, "low": 15000, "high": 100000, "competition": "low"},
        "trucking": {"avg": 12000, "low": 4000, "high": 40000, "competition": "medium"},
        "firefighter": {"avg": 10000, "low": 3000, "high": 35000, "competition": "low"},
        "military": {"avg": 8000, "low": 2500, "high": 28000, "competition": "medium"},
        "introvert": {"avg": 15000, "low": 5000, "high": 50000, "competition": "medium"},
        "sarcasm": {"avg": 10000, "low": 3000, "high": 35000, "competition": "high"},
        "anxiety": {"avg": 12000, "low": 4000, "high": 40000, "competition": "medium"},
    }

    def __init__(self):
        self.history_cache = {}

    def estimate_sales_from_bsr(self, bsr: int) -> Dict[str, Any]:
        """Estimate daily/monthly sales from BSR."""
        daily_sales = 0.05  # Default for very high BSR

        for threshold, sales in self.BSR_SALES_MAP:
            if bsr <= threshold:
                daily_sales = sales
                break

        monthly_sales = daily_sales * 30
        yearly_sales = daily_sales * 365

        # Calculate revenue (assuming $4 royalty per sale)
        royalty = 4.00
        monthly_revenue = monthly_sales * royalty
        yearly_revenue = yearly_sales * royalty

        return {
            "bsr": bsr,
            "estimated_daily_sales": round(daily_sales, 2),
            "estimated_monthly_sales": round(monthly_sales, 1),
            "estimated_yearly_sales": round(yearly_sales, 0),
            "estimated_monthly_revenue": round(monthly_revenue, 2),
            "estimated_yearly_revenue": round(yearly_revenue, 2),
            "royalty_assumed": royalty,
            "confidence": self._get_confidence(bsr),
        }

    def get_niche_bsr_data(self, niche: str) -> Dict[str, Any]:
        """Get BSR statistics for a niche."""
        data = self.NICHE_BSR_AVERAGES.get(
            niche.lower(),
            {"avg": 50000, "low": 15000, "high": 150000, "competition": "unknown"}
        )

        return {
            "niche": niche,
            "average_bsr": data["avg"],
            "top_performer_bsr": data["low"],
            "average_performer_bsr": data["high"],
            "competition_level": data["competition"],
            "estimated_avg_sales": self.estimate_sales_from_bsr(data["avg"]),
            "estimated_top_sales": self.estimate_sales_from_bsr(data["low"]),
        }

    def simulate_bsr_history(
        self,
        keyword: str,
        days: int = 30,
        starting_bsr: int = None
    ) -> List[Dict[str, Any]]:
        """
        Simulate BSR history for a keyword.
        In production, this would come from actual tracking data.
        """
        if starting_bsr is None:
            starting_bsr = random.randint(10000, 50000)

        history = []
        current_bsr = starting_bsr
        today = datetime.now()

        for i in range(days, -1, -1):
            date = today - timedelta(days=i)

            # Simulate BSR fluctuation
            change_pct = random.uniform(-0.15, 0.15)
            current_bsr = int(current_bsr * (1 + change_pct))
            current_bsr = max(100, min(current_bsr, 500000))

            sales = self.estimate_sales_from_bsr(current_bsr)

            history.append({
                "date": date.strftime("%Y-%m-%d"),
                "bsr": current_bsr,
                "estimated_daily_sales": sales["estimated_daily_sales"],
            })

        return history

    def analyze_bsr_trend(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze BSR trend from history data."""
        if len(history) < 2:
            return {"trend": "insufficient_data"}

        bsrs = [h["bsr"] for h in history]
        first_half = bsrs[:len(bsrs)//2]
        second_half = bsrs[len(bsrs)//2:]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        # Lower BSR = better, so if second half is lower, it's improving
        if avg_second < avg_first * 0.9:
            trend = "improving"
            trend_pct = round((1 - avg_second/avg_first) * 100, 1)
        elif avg_second > avg_first * 1.1:
            trend = "declining"
            trend_pct = round((avg_second/avg_first - 1) * 100, 1)
        else:
            trend = "stable"
            trend_pct = 0

        return {
            "trend": trend,
            "trend_percentage": trend_pct,
            "best_bsr": min(bsrs),
            "worst_bsr": max(bsrs),
            "current_bsr": bsrs[-1],
            "average_bsr": round(sum(bsrs) / len(bsrs)),
            "volatility": self._calculate_volatility(bsrs),
        }

    def get_bsr_opportunities(self) -> List[Dict[str, Any]]:
        """Get niches with good BSR opportunity (low competition, good sales)."""
        opportunities = []

        for niche, data in self.NICHE_BSR_AVERAGES.items():
            if data["competition"] in ["low", "medium"]:
                sales = self.estimate_sales_from_bsr(data["avg"])
                score = self._calculate_opportunity_score(data, sales)

                opportunities.append({
                    "niche": niche,
                    "competition": data["competition"],
                    "average_bsr": data["avg"],
                    "estimated_monthly_sales": sales["estimated_monthly_sales"],
                    "estimated_monthly_revenue": sales["estimated_monthly_revenue"],
                    "opportunity_score": score,
                })

        return sorted(opportunities, key=lambda x: x["opportunity_score"], reverse=True)

    def _calculate_opportunity_score(self, niche_data: Dict, sales: Dict) -> int:
        """Calculate opportunity score for a niche."""
        score = 50

        # Competition bonus
        if niche_data["competition"] == "low":
            score += 30
        elif niche_data["competition"] == "medium":
            score += 15

        # Sales potential bonus
        if sales["estimated_monthly_sales"] >= 50:
            score += 20
        elif sales["estimated_monthly_sales"] >= 20:
            score += 10

        return min(score, 100)

    def _get_confidence(self, bsr: int) -> str:
        """Get confidence level for BSR estimation."""
        if bsr < 10000:
            return "high"
        elif bsr < 50000:
            return "medium"
        else:
            return "low"

    def _calculate_volatility(self, bsrs: List[int]) -> str:
        """Calculate BSR volatility."""
        if len(bsrs) < 2:
            return "unknown"

        avg = sum(bsrs) / len(bsrs)
        variance = sum((x - avg) ** 2 for x in bsrs) / len(bsrs)
        std_dev = math.sqrt(variance)
        cv = std_dev / avg  # Coefficient of variation

        if cv < 0.1:
            return "low"
        elif cv < 0.3:
            return "medium"
        else:
            return "high"


# Singleton instance
bsr_tracker = BSRTracker()

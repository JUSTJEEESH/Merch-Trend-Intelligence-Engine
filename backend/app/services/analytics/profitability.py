"""Niche profitability calculator service."""
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ProfitabilityCalculator:
    """
    Service for calculating niche profitability, ROI,
    and revenue projections for merch sellers.
    """

    # Amazon Merch royalty rates by product (approximate)
    ROYALTY_RATES = {
        "standard_tee": {
            "price_19.99": 4.51,
            "price_21.99": 5.31,
            "price_24.99": 6.51,
            "price_29.99": 8.51,
            "default": 4.51,
        },
        "premium_tee": {
            "price_22.99": 4.13,
            "price_24.99": 4.93,
            "price_27.99": 6.13,
            "default": 4.13,
        },
        "long_sleeve": {
            "price_24.99": 4.91,
            "price_27.99": 6.11,
            "default": 4.91,
        },
        "hoodie": {
            "price_39.99": 6.51,
            "price_44.99": 8.51,
            "default": 6.51,
        },
        "sweatshirt": {
            "price_34.99": 5.71,
            "price_39.99": 7.71,
            "default": 5.71,
        },
        "tank_top": {
            "price_19.99": 4.51,
            "price_21.99": 5.31,
            "default": 4.51,
        },
        "popsocket": {
            "price_14.99": 2.25,
            "default": 2.25,
        },
        "phone_case": {
            "price_17.99": 2.69,
            "default": 2.69,
        },
    }

    # Niche competition and saturation data
    NICHE_DATA = {
        "coffee": {"saturation": 0.85, "demand": 0.90, "seasonality": 0.1},
        "dogs": {"saturation": 0.90, "demand": 0.95, "seasonality": 0.05},
        "cats": {"saturation": 0.85, "demand": 0.88, "seasonality": 0.05},
        "mom": {"saturation": 0.80, "demand": 0.92, "seasonality": 0.4},  # Mother's Day spike
        "dad": {"saturation": 0.70, "demand": 0.85, "seasonality": 0.4},  # Father's Day spike
        "nursing": {"saturation": 0.60, "demand": 0.75, "seasonality": 0.15},
        "teaching": {"saturation": 0.65, "demand": 0.70, "seasonality": 0.3},  # Back to school
        "fitness": {"saturation": 0.75, "demand": 0.80, "seasonality": 0.2},  # New Year spike
        "beer": {"saturation": 0.55, "demand": 0.70, "seasonality": 0.15},
        "wine": {"saturation": 0.50, "demand": 0.65, "seasonality": 0.2},
        "gaming": {"saturation": 0.80, "demand": 0.85, "seasonality": 0.25},  # Holiday spike
        "hunting": {"saturation": 0.50, "demand": 0.65, "seasonality": 0.3},
        "fishing": {"saturation": 0.55, "demand": 0.68, "seasonality": 0.25},
        "camping": {"saturation": 0.55, "demand": 0.70, "seasonality": 0.3},
        "introvert": {"saturation": 0.45, "demand": 0.60, "seasonality": 0.05},
        "sarcasm": {"saturation": 0.75, "demand": 0.80, "seasonality": 0.05},
        "anxiety": {"saturation": 0.55, "demand": 0.70, "seasonality": 0.1},
        "trucking": {"saturation": 0.40, "demand": 0.55, "seasonality": 0.05},
        "firefighter": {"saturation": 0.35, "demand": 0.50, "seasonality": 0.1},
        "military": {"saturation": 0.50, "demand": 0.65, "seasonality": 0.15},
        "christmas": {"saturation": 0.90, "demand": 0.95, "seasonality": 0.95},
        "halloween": {"saturation": 0.85, "demand": 0.90, "seasonality": 0.90},
    }

    def calculate_niche_profitability(self, niche: str) -> Dict[str, Any]:
        """Calculate overall profitability score for a niche."""
        data = self.NICHE_DATA.get(
            niche.lower(),
            {"saturation": 0.5, "demand": 0.5, "seasonality": 0.1}
        )

        # Calculate opportunity score (higher = better)
        # Opportunity = Demand / Saturation (adjusted for seasonality)
        base_score = (data["demand"] / (data["saturation"] + 0.1)) * 50
        seasonality_bonus = data["seasonality"] * 20  # Seasonal niches can spike

        opportunity_score = min(base_score + seasonality_bonus, 100)

        # Calculate competition level
        if data["saturation"] >= 0.8:
            competition = "very_high"
        elif data["saturation"] >= 0.6:
            competition = "high"
        elif data["saturation"] >= 0.4:
            competition = "medium"
        else:
            competition = "low"

        return {
            "niche": niche,
            "opportunity_score": round(opportunity_score),
            "competition_level": competition,
            "saturation": f"{int(data['saturation'] * 100)}%",
            "demand": f"{int(data['demand'] * 100)}%",
            "seasonality": "high" if data["seasonality"] > 0.3 else "medium" if data["seasonality"] > 0.1 else "low",
            "recommendation": self._get_recommendation(opportunity_score, competition),
        }

    def calculate_revenue_projection(
        self,
        estimated_monthly_sales: int,
        product: str = "standard_tee",
        months: int = 12,
    ) -> Dict[str, Any]:
        """Project revenue based on estimated sales."""
        royalty = self.ROYALTY_RATES.get(product, {}).get("default", 4.00)

        monthly_revenue = estimated_monthly_sales * royalty
        yearly_revenue = monthly_revenue * 12

        # Apply growth/decline modeling
        projections = []
        cumulative = 0
        for month in range(1, months + 1):
            # Assume slight organic growth over time
            growth_factor = 1 + (0.02 * (month - 1))  # 2% monthly growth
            month_sales = int(estimated_monthly_sales * growth_factor)
            month_revenue = month_sales * royalty
            cumulative += month_revenue

            projections.append({
                "month": month,
                "sales": month_sales,
                "revenue": round(month_revenue, 2),
                "cumulative": round(cumulative, 2),
            })

        return {
            "product": product,
            "royalty_per_sale": royalty,
            "monthly_sales": estimated_monthly_sales,
            "monthly_revenue": round(monthly_revenue, 2),
            "yearly_revenue": round(yearly_revenue, 2),
            "projections": projections,
        }

    def calculate_design_roi(
        self,
        design_cost: float = 0,  # Self-made or purchased
        time_invested_hours: float = 1,
        hourly_value: float = 25,
        estimated_monthly_sales: int = 5,
        royalty: float = 4.51,
    ) -> Dict[str, Any]:
        """Calculate ROI for a design."""
        # Total investment
        time_cost = time_invested_hours * hourly_value
        total_investment = design_cost + time_cost

        # Revenue calculations
        monthly_revenue = estimated_monthly_sales * royalty
        yearly_revenue = monthly_revenue * 12

        # ROI calculations
        if total_investment > 0:
            months_to_break_even = total_investment / monthly_revenue if monthly_revenue > 0 else float('inf')
            yearly_roi = ((yearly_revenue - total_investment) / total_investment) * 100 if total_investment > 0 else float('inf')
        else:
            months_to_break_even = 0
            yearly_roi = float('inf')

        return {
            "design_cost": design_cost,
            "time_invested": f"{time_invested_hours} hours",
            "time_value": round(time_cost, 2),
            "total_investment": round(total_investment, 2),
            "estimated_monthly_revenue": round(monthly_revenue, 2),
            "estimated_yearly_revenue": round(yearly_revenue, 2),
            "months_to_break_even": round(months_to_break_even, 1) if months_to_break_even != float('inf') else "N/A",
            "yearly_roi": f"{round(yearly_roi)}%" if yearly_roi != float('inf') else "Infinite (no cost)",
            "profitable": yearly_revenue > total_investment,
        }

    def compare_niches(self, niches: List[str]) -> List[Dict[str, Any]]:
        """Compare profitability across multiple niches."""
        comparisons = []

        for niche in niches:
            data = self.calculate_niche_profitability(niche)
            comparisons.append(data)

        # Sort by opportunity score
        comparisons.sort(key=lambda x: x["opportunity_score"], reverse=True)

        return comparisons

    def get_best_niches(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most profitable niches."""
        all_niches = list(self.NICHE_DATA.keys())
        comparisons = self.compare_niches(all_niches)
        return comparisons[:count]

    def calculate_portfolio_metrics(
        self,
        designs_count: int,
        avg_sales_per_design: float,
        product: str = "standard_tee",
    ) -> Dict[str, Any]:
        """Calculate metrics for entire design portfolio."""
        royalty = self.ROYALTY_RATES.get(product, {}).get("default", 4.00)

        total_monthly_sales = designs_count * avg_sales_per_design
        total_monthly_revenue = total_monthly_sales * royalty
        total_yearly_revenue = total_monthly_revenue * 12

        # Tier progression (Amazon Merch tiers)
        tiers = [
            {"tier": 10, "designs": 10},
            {"tier": 25, "designs": 25},
            {"tier": 100, "designs": 100},
            {"tier": 500, "designs": 500},
            {"tier": 1000, "designs": 1000},
            {"tier": 2000, "designs": 2000},
            {"tier": 4000, "designs": 4000},
            {"tier": 8000, "designs": 8000},
        ]

        current_tier = 10
        for t in tiers:
            if designs_count >= t["designs"]:
                current_tier = t["tier"]

        next_tier = None
        for t in tiers:
            if t["tier"] > current_tier:
                next_tier = t
                break

        return {
            "designs_count": designs_count,
            "avg_sales_per_design": avg_sales_per_design,
            "total_monthly_sales": round(total_monthly_sales, 1),
            "total_monthly_revenue": round(total_monthly_revenue, 2),
            "total_yearly_revenue": round(total_yearly_revenue, 2),
            "current_tier": current_tier,
            "next_tier": next_tier["tier"] if next_tier else "Max tier reached",
            "designs_to_next_tier": next_tier["designs"] - designs_count if next_tier else 0,
        }

    def _get_recommendation(self, score: float, competition: str) -> str:
        """Get recommendation based on metrics."""
        if score >= 70 and competition in ["low", "medium"]:
            return "Highly Recommended - Low competition with good demand"
        elif score >= 70:
            return "Good potential but requires standout designs due to competition"
        elif score >= 50:
            return "Moderate opportunity - Focus on unique angles"
        else:
            return "Consider alternative niches with better opportunity scores"


# Singleton instance
profitability_calculator = ProfitabilityCalculator()

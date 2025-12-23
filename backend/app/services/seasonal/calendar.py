"""Seasonal calendar service for merch planning."""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SeasonalCalendar:
    """
    Service for tracking upcoming holidays, events, and seasonal opportunities.
    Provides upload deadlines and phrase suggestions.
    """

    # Comprehensive holiday/event database with merch potential
    EVENTS = [
        # Q1 - January
        {"name": "New Year's Day", "date": "01-01", "upload_days_before": 30, "priority": "high", "niches": ["motivation", "fitness", "lifestyle"], "phrases": ["New Year New Me", "Fresh Start Energy", "2025 Goals Loading", "My Year Era"]},
        {"name": "Martin Luther King Jr Day", "date": "01-20", "upload_days_before": 21, "priority": "medium", "niches": ["inspiration", "equality"], "phrases": ["Dream Big", "I Have A Dream", "Be The Change"]},
        {"name": "National Puzzle Day", "date": "01-29", "upload_days_before": 14, "priority": "low", "niches": ["puzzles", "hobbies"], "phrases": ["Piece By Piece", "Puzzle Addict", "Missing Piece"]},

        # Q1 - February
        {"name": "Groundhog Day", "date": "02-02", "upload_days_before": 14, "priority": "low", "niches": ["humor"], "phrases": ["Same Day Different Vibes", "Groundhog Era"]},
        {"name": "Super Bowl", "date": "02-09", "upload_days_before": 21, "priority": "high", "niches": ["sports", "football", "food"], "phrases": ["Game Day Mode", "Here For The Snacks", "Super Bowl Sunday"]},
        {"name": "Valentine's Day", "date": "02-14", "upload_days_before": 45, "priority": "critical", "niches": ["love", "relationships", "humor", "singles"], "phrases": ["Self Love Club", "Anti-Valentine", "Love Yourself First", "Taken By My Dog", "My Cat Is My Valentine"]},
        {"name": "Presidents Day", "date": "02-17", "upload_days_before": 14, "priority": "low", "niches": ["patriotic"], "phrases": ["American Made", "USA Vibes"]},
        {"name": "Mardi Gras", "date": "02-25", "upload_days_before": 21, "priority": "medium", "niches": ["party", "new orleans"], "phrases": ["Let The Good Times Roll", "Mardi Gras Mode", "Beads Please"]},

        # Q1 - March
        {"name": "International Women's Day", "date": "03-08", "upload_days_before": 21, "priority": "high", "niches": ["women", "empowerment", "feminist"], "phrases": ["Future Is Female", "Girl Power", "Women Supporting Women", "Empowered Women"]},
        {"name": "St. Patrick's Day", "date": "03-17", "upload_days_before": 45, "priority": "critical", "niches": ["irish", "drinking", "luck"], "phrases": ["Lucky Charm", "Irish Ish", "Feeling Lucky", "Shenanigans Coordinator", "Kiss Me Im Irish"]},
        {"name": "March Madness Start", "date": "03-18", "upload_days_before": 21, "priority": "medium", "niches": ["basketball", "sports"], "phrases": ["Bracket Buster", "March Madness Mode", "Basketball Is Life"]},
        {"name": "First Day of Spring", "date": "03-20", "upload_days_before": 21, "priority": "medium", "niches": ["spring", "nature", "gardening"], "phrases": ["Spring Has Sprung", "Bloom Where Planted", "Spring Vibes Only"]},

        # Q2 - April
        {"name": "April Fools Day", "date": "04-01", "upload_days_before": 21, "priority": "medium", "niches": ["humor", "pranks"], "phrases": ["Professional Fool", "Trust No One Today", "Prank Mode Activated"]},
        {"name": "Easter", "date": "04-20", "upload_days_before": 45, "priority": "critical", "niches": ["easter", "spring", "religious", "family"], "phrases": ["Some Bunny Loves You", "Hoppy Easter", "Egg Hunter", "Easter Vibes"]},
        {"name": "Earth Day", "date": "04-22", "upload_days_before": 21, "priority": "medium", "niches": ["environment", "nature", "eco"], "phrases": ["Mother Earth", "Planet Over Profit", "Eco Warrior", "Earth Day Every Day"]},
        {"name": "Administrative Professionals Day", "date": "04-23", "upload_days_before": 14, "priority": "medium", "niches": ["office", "work"], "phrases": ["Office Hero", "Best Admin Ever", "Running This Office"]},

        # Q2 - May
        {"name": "Cinco de Mayo", "date": "05-05", "upload_days_before": 30, "priority": "high", "niches": ["mexican", "party", "tacos"], "phrases": ["Taco Tuesday Every Day", "Nacho Average Person", "Fiesta Mode", "Tequila Made Me Do It"]},
        {"name": "Mother's Day", "date": "05-11", "upload_days_before": 60, "priority": "critical", "niches": ["mom", "family", "parenting"], "phrases": ["Best Mom Ever", "Mama Bear", "Mom Mode", "Tired But Blessed", "Boy Mom", "Girl Mom"]},
        {"name": "Memorial Day", "date": "05-26", "upload_days_before": 30, "priority": "high", "niches": ["patriotic", "military", "summer"], "phrases": ["Land Of The Free", "Home Of The Brave", "Freedom Isnt Free", "American Pride"]},

        # Q2 - June
        {"name": "Pride Month Start", "date": "06-01", "upload_days_before": 45, "priority": "critical", "niches": ["lgbtq", "pride", "equality"], "phrases": ["Love Is Love", "Pride Mode", "Born This Way", "Ally Vibes", "Rainbow Everything"]},
        {"name": "Father's Day", "date": "06-15", "upload_days_before": 60, "priority": "critical", "niches": ["dad", "family", "parenting"], "phrases": ["Best Dad Ever", "Dad Jokes Champion", "Father Figure", "Girl Dad", "Boy Dad", "Dadlife"]},
        {"name": "Juneteenth", "date": "06-19", "upload_days_before": 21, "priority": "medium", "niches": ["equality", "history"], "phrases": ["Freedom Day", "Juneteenth Celebration"]},
        {"name": "First Day of Summer", "date": "06-20", "upload_days_before": 30, "priority": "high", "niches": ["summer", "beach", "vacation"], "phrases": ["Summer State Of Mind", "Beach Please", "Vitamin Sea", "Hot Girl Summer"]},

        # Q3 - July
        {"name": "Independence Day", "date": "07-04", "upload_days_before": 60, "priority": "critical", "niches": ["patriotic", "usa", "summer"], "phrases": ["Freedom Looks Good On Me", "American Made", "USA All Day", "Party Like Its 1776", "Red White Blessed"]},
        {"name": "National Ice Cream Day", "date": "07-20", "upload_days_before": 14, "priority": "low", "niches": ["food", "summer"], "phrases": ["Ice Cream Is My Love Language", "Sprinkle Kindness"]},

        # Q3 - August
        {"name": "National Dog Day", "date": "08-26", "upload_days_before": 21, "priority": "high", "niches": ["dogs", "pets"], "phrases": ["Dog Mom", "Dog Dad", "My Kids Have Paws", "Life Is Better With Dogs", "Dog Person"]},
        {"name": "Back to School", "date": "08-15", "upload_days_before": 45, "priority": "high", "niches": ["school", "teaching", "students"], "phrases": ["First Day Feels", "Teacher Mode", "School Survival Mode", "Too Cool For School"]},

        # Q3 - September
        {"name": "Labor Day", "date": "09-01", "upload_days_before": 21, "priority": "medium", "niches": ["work", "summer"], "phrases": ["Last Day Of Summer Mode", "Work Hard Rest Hard"]},
        {"name": "Grandparents Day", "date": "09-07", "upload_days_before": 30, "priority": "medium", "niches": ["grandparents", "family"], "phrases": ["Best Grandma Ever", "Best Grandpa Ever", "Promoted To Grandma", "Grandpa Life"]},
        {"name": "First Day of Fall", "date": "09-22", "upload_days_before": 30, "priority": "high", "niches": ["fall", "pumpkin", "cozy"], "phrases": ["Fall Vibes Only", "Sweater Weather", "Pumpkin Everything", "Autumn Leaves And Please"]},

        # Q4 - October
        {"name": "Breast Cancer Awareness Month", "date": "10-01", "upload_days_before": 30, "priority": "high", "niches": ["awareness", "health", "pink"], "phrases": ["Fight Like A Girl", "Pink Power", "Cancer Warrior", "Survivor Strong"]},
        {"name": "Halloween", "date": "10-31", "upload_days_before": 60, "priority": "critical", "niches": ["halloween", "spooky", "horror"], "phrases": ["Spooky Season", "Basic Witch", "Creep It Real", "Boo Crew", "Too Cute To Spook", "Trick Or Treat Yourself"]},

        # Q4 - November
        {"name": "Dia de los Muertos", "date": "11-01", "upload_days_before": 30, "priority": "medium", "niches": ["mexican", "culture", "skulls"], "phrases": ["Remember Me", "Sugar Skull Vibes", "Día De Los Muertos"]},
        {"name": "Veterans Day", "date": "11-11", "upload_days_before": 30, "priority": "high", "niches": ["military", "veterans", "patriotic"], "phrases": ["Veteran Owned", "Thank A Vet", "Proudly Served", "Military Family"]},
        {"name": "Thanksgiving", "date": "11-27", "upload_days_before": 45, "priority": "critical", "niches": ["thanksgiving", "family", "food"], "phrases": ["Thankful Blessed", "Gobble Til You Wobble", "Pie Fix Everything", "Turkey Coma Mode"]},
        {"name": "Black Friday", "date": "11-28", "upload_days_before": 30, "priority": "high", "niches": ["shopping", "deals"], "phrases": ["Professional Shopper", "Cart Goals", "Shop Til You Drop"]},

        # Q4 - December
        {"name": "Hanukkah Start", "date": "12-14", "upload_days_before": 45, "priority": "high", "niches": ["jewish", "hanukkah", "holiday"], "phrases": ["Happy Hanukkah", "Festival Of Lights", "Eight Crazy Nights"]},
        {"name": "Christmas", "date": "12-25", "upload_days_before": 90, "priority": "critical", "niches": ["christmas", "holiday", "winter"], "phrases": ["Merry Everything", "Santa Baby", "Jingle All The Way", "Dear Santa I Tried", "Naughty List Member"]},
        {"name": "New Year's Eve", "date": "12-31", "upload_days_before": 45, "priority": "high", "niches": ["new year", "party"], "phrases": ["New Year Who Dis", "Midnight Kisses", "Cheers To New Year"]},
    ]

    # Recurring awareness months
    AWARENESS_MONTHS = {
        1: [("National Mentoring Month", ["mentoring", "education"]), ("Thyroid Awareness Month", ["health"])],
        2: [("Black History Month", ["history", "equality"]), ("Heart Health Month", ["health", "fitness"])],
        3: [("Women's History Month", ["women", "empowerment"]), ("National Reading Month", ["books", "reading"])],
        4: [("Autism Awareness Month", ["autism", "awareness"]), ("Stress Awareness Month", ["mental health"])],
        5: [("Mental Health Awareness Month", ["mental health", "anxiety"]), ("Asian American Heritage Month", ["heritage"])],
        6: [("Pride Month", ["lgbtq", "pride"]), ("Men's Health Month", ["health", "fitness"])],
        7: [("UV Safety Month", ["summer", "health"]), ("Ice Cream Month", ["food", "summer"])],
        8: [("National Wellness Month", ["health", "fitness"]), ("Back to School Month", ["school", "teaching"])],
        9: [("Suicide Prevention Month", ["mental health", "awareness"]), ("Hispanic Heritage Month", ["heritage"])],
        10: [("Breast Cancer Awareness", ["awareness", "pink"]), ("Domestic Violence Awareness", ["awareness"])],
        11: [("Native American Heritage Month", ["heritage"]), ("Movember", ["men's health"])],
        12: [("National Handwashing Month", ["health"]), ("Safe Toys & Gifts Month", ["holiday"])],
    }

    def get_upcoming_events(self, days_ahead: int = 90) -> List[Dict[str, Any]]:
        """Get upcoming events within the specified days."""
        today = datetime.now()
        current_year = today.year
        upcoming = []

        for event in self.EVENTS:
            # Parse date
            month, day = map(int, event["date"].split("-"))

            # Try this year first
            event_date = datetime(current_year, month, day)

            # If already passed, use next year
            if event_date < today:
                event_date = datetime(current_year + 1, month, day)

            days_until = (event_date - today).days

            if 0 <= days_until <= days_ahead:
                upload_deadline = event_date - timedelta(days=event["upload_days_before"])
                days_to_upload = (upload_deadline - today).days

                upcoming.append({
                    **event,
                    "event_date": event_date.strftime("%Y-%m-%d"),
                    "days_until": days_until,
                    "upload_deadline": upload_deadline.strftime("%Y-%m-%d"),
                    "days_to_upload_deadline": days_to_upload,
                    "urgency": self._calculate_urgency(days_to_upload),
                    "status": "overdue" if days_to_upload < 0 else "urgent" if days_to_upload <= 7 else "upcoming",
                })

        return sorted(upcoming, key=lambda x: x["days_until"])

    def get_current_month_awareness(self) -> List[Dict[str, Any]]:
        """Get awareness themes for current month."""
        current_month = datetime.now().month
        awareness = self.AWARENESS_MONTHS.get(current_month, [])

        return [{
            "name": a[0],
            "niches": a[1],
            "month": current_month,
        } for a in awareness]

    def _calculate_urgency(self, days_to_upload: int) -> str:
        """Calculate urgency level based on upload deadline."""
        if days_to_upload < 0:
            return "overdue"
        elif days_to_upload <= 3:
            return "critical"
        elif days_to_upload <= 7:
            return "high"
        elif days_to_upload <= 14:
            return "medium"
        else:
            return "low"

    def get_suggested_phrases_for_event(self, event_name: str) -> List[str]:
        """Get phrase suggestions for a specific event."""
        for event in self.EVENTS:
            if event["name"].lower() == event_name.lower():
                return event.get("phrases", [])
        return []

    def get_events_for_niche(self, niche: str) -> List[Dict[str, Any]]:
        """Get all events relevant to a specific niche."""
        upcoming = self.get_upcoming_events(days_ahead=365)

        return [
            event for event in upcoming
            if niche.lower() in [n.lower() for n in event.get("niches", [])]
        ]

    def get_calendar_overview(self) -> Dict[str, Any]:
        """Get a complete calendar overview."""
        upcoming_30 = self.get_upcoming_events(30)
        upcoming_90 = self.get_upcoming_events(90)

        critical = [e for e in upcoming_90 if e["priority"] == "critical"]
        overdue = [e for e in upcoming_90 if e["status"] == "overdue"]
        urgent = [e for e in upcoming_90 if e["urgency"] in ["critical", "high"]]

        return {
            "next_30_days": upcoming_30,
            "next_90_days": upcoming_90,
            "critical_events": critical,
            "overdue_uploads": overdue,
            "urgent_uploads": urgent,
            "awareness_this_month": self.get_current_month_awareness(),
            "summary": {
                "total_upcoming": len(upcoming_90),
                "critical_count": len(critical),
                "overdue_count": len(overdue),
                "urgent_count": len(urgent),
            }
        }


# Singleton instance
seasonal_calendar = SeasonalCalendar()

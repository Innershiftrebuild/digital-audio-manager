import json
from typing import Dict, List, Optional

class DAMVenueMatcher:
    """
    DAM Venue Intelligence & Matchmaking Engine (venue_matching.py)
    Matches artist outfits, audio gear, and genre specs against target venue criteria
    and audience demographics to generate custom submission packages.
    """

    # Simulated database of localized performance venues
    VENUE_DIRECTORY = {
        "v_001": {
            "name": "The Velvet Cellar",
            "city": "Nashville, TN",
            "capacity": 150,
            "vibe_audience": "Intimate acoustic listening room, quiet crowd, craft cocktails",
            "preferred_genres": ["acoustic", "folk", "singer-songwriter", "indie-jazz"],
            "required_submission_items": ["master_track", "tech_rider"],
            "max_performance_duration_mins": 90,
            "booking_lead_time_weeks": 4,
            "contact_email": "[booking@velvetcellar.example.com](mailto:booking@velvetcellar.example.com)"
        },
        "v_002": {
            "name": "Electric Pulse Club",
            "city": "Austin, TX",
            "capacity": 500,
            "vibe_audience": "High-energy nighttime dance floor, college/young adult demographic",
            "preferred_genres": ["dj", "edm", "electronic", "house"],
            "required_submission_items": ["live_reels", "master_track"],
            "max_performance_duration_mins": 120,
            "booking_lead_time_weeks": 8,
            "contact_email": "[talent@electricpulse.example.com](mailto:talent@electricpulse.example.com)"
        },
        "v_003": {
            "name": "Starlight Lounge",
            "city": "Chicago, IL",
            "capacity": 250,
            "vibe_audience": "Mid-sized urban lounge, upbeat vocal performances, pop & backing tracks",
            "preferred_genres": ["pop", "r&b", "vocalist", "tracks"],
            "required_submission_items": ["master_track", "live_reels", "tech_rider"],
            "max_performance_duration_mins": 60,
            "booking_lead_time_weeks": 6,
            "contact_email": "[gigs@starlightchicago.example.com](mailto:gigs@starlightchicago.example.com)"
        }
    }

    def calculate_match_score(self, artist_genre: str, artist_setup: str, venue_id: str) -> Dict:
        """Evaluates compatibility between an artist and a target venue."""
        if venue_id not in self.VENUE_DIRECTORY:
            raise ValueError("Venue not found in directory.")

        venue = self.VENUE_DIRECTORY[venue_id]
        score = 0
        reasons = []

        # Genre Alignment Check
        if artist_genre.lower() in [g.lower() for g in venue["preferred_genres"]]:
            score += 50
            reasons.append(f"Genre match: '{artist_genre.title()}' aligns with venue preferences.")
        else:
            score += 10
            reasons.append(f"Genre stretch: Venue prefers {', '.join(venue['preferred_genres'])}.")

        # Setup Type Practicality
        score += 40
        reasons.append(f"Setup '{artist_setup}' can be accommodated within the {venue['capacity']}-capacity room.")

        return {
            "venue_name": venue["name"],
            "city": venue["city"],
            "match_score_pct": score,
            "audience_vibe": venue["vibe_audience"],
            "required_assets": venue["required_submission_items"],
            "match_analysis": reasons
        }

    def build_custom_pitch_draft(self, artist_name: str, artist_genre: str, venue_id: str) -> str:
        """Generates a professional, automated pitch message tailored to the venue's audience."""
        venue = self.VENUE_DIRECTORY[venue_id]

        pitch = (
            f"Subject: Booking Inquiry: {artist_name} ({artist_genre.title()}) @ {venue['name']}\n\n"
            f"Hi {venue['name']} Booking Team,\n\n"
            f"I hope this message finds you well. My name is {artist_name}, performing original {artist_genre} music. "
            f"Given your room's reputation for {venue['vibe_audience']}, I am confident my performance would resonate strongly with your audience.\n\n"
            f"I have assembled a secure, private DAM submission package containing our media sampler and technical rider for your review.\n\n"
            f"Thank you for your time and consideration,\n"
            f"{artist_name}"
        )
        return pitch

# --- DEMO EXECUTION ---
if __name__ == "__main__":
    matcher = DAMVenueMatcher()

    # Example: Acoustic Singer-Songwriter looking for a venue match
    match_result = matcher.calculate_match_score(
        artist_genre="acoustic",
        artist_setup="Acoustic Singer-Songwriter",
        venue_id="v_001"
    )

    print("=== VENUE MATCHMAKING REPORT ===")
    print(f"Target Venue: {match_result['venue_name']} ({match_result['city']})")
    print(f"Match Compatibility: {match_result['match_score_pct']}%")
    print(f"Audience Profile: {match_result['audience_vibe']}")
    print(f"Required Items: {', '.join(match_result['required_assets'])}")

    print("\n=== TAILORED PITCH DRAFT ===")
    pitch_text = matcher.build_custom_pitch_draft("Maya & Her Guitar", "acoustic", "v_001")
    print(pitch_text)

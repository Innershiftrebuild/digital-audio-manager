# +==========================================================================+
# |                             healthvenom.com                              |
# |                            Health Venom Inc.                             |
# |                                                                          |
# |   _   _ _____    _    _   _____ _   ___     _______ _   _  ___  __  __   |
# |  | | | | ____|  / \  | | |_   _| | | \ \   / / ____| \ | |/ _ \|  \/  |  |
# |  | |_| |  _|   / _ \ | |   | | | |_| |\ \ / /|  _| |  \| | | | | |\/| |  |
# |  |  _  | |___ / ___ \| |___| | |  _  | \ V / | |___| |\  | |_| | |  | |  |
# |  |_| |_|_____/_/   \_\_____|_| |_| |_|  \_/  |_____|_| \_|\___/|_|  |_|  |
# |                                                                          |
# |               The DAM / BookedStage - Sanitas Mentis Inc.                |
# |                  Imprinted in the code, so it lives on.                  |
# +==========================================================================+

DAM_BANNER = r"""
+==========================================================================+
|                             healthvenom.com                              |
|                            Health Venom Inc.                             |
|                                                                          |
|   _   _ _____    _    _   _____ _   ___     _______ _   _  ___  __  __   |
|  | | | | ____|  / \  | | |_   _| | | \ \   / / ____| \ | |/ _ \|  \/  |  |
|  | |_| |  _|   / _ \ | |   | | | |_| |\ \ / /|  _| |  \| | | | | |\/| |  |
|  |  _  | |___ / ___ \| |___| | |  _  | \ V / | |___| |\  | |_| | |  | |  |
|  |_| |_|_____/_/   \_\_____|_| |_| |_|  \_/  |_____|_| \_|\___/|_|  |_|  |
|                                                                          |
|               The DAM / BookedStage - Sanitas Mentis Inc.                |
|                  Imprinted in the code, so it lives on.                  |
+==========================================================================+
"""

import json
import math
from typing import Dict, List, Optional

class DAMVenueMatcher:
    """
    DAM Venue Intelligence & Matchmaking Engine (venue_matching.py) — v2

    v2 adds location search, per Rich's spec (2026-11-23): a musician enters
    their location and a distance limit, then explores the venues inside that
    radius — each carrying a full profile (who runs it, who's played it, who
    vouches for it, what it pays, and its content policy) so the musician can
    judge the fit before pitching. Content policy (originals / covers / mixed)
    and pay are first-class filters: an originals-only artist never gets
    matched to a covers-only room.

    v1 functions (calculate_match_score, build_custom_pitch_draft) are
    unchanged in behavior.

    v2.1 (2026-11-24) adds the artist side of content policy: an artist
    declares one of three categories — originals, covers, or mixed — and
    matching pairs it against the venue's content policy. A mixed artist
    fits any room; an originals artist never lands in a covers-only room,
    and a covers artist never lands in an originals-only room.
    """

    # Artist content categories — what the artist plays. The artist side of
    # content policy (added 2026-11-24, per Rich): every artist declares one
    # of three categories, and matching pairs it against the venue's policy.
    #   originals — the artist plays only their own songs (Rich's own case)
    #   covers    — the artist plays other people's songs
    #   mixed     — a variety of both originals and covers
    ARTIST_CONTENT_CATEGORIES = ("originals", "covers", "mixed")

    @staticmethod
    def validate_content_category(category: str) -> str:
        """Normalize and validate an artist content category."""
        key = category.strip().lower()
        if key not in DAMVenueMatcher.ARTIST_CONTENT_CATEGORIES:
            raise ValueError(
                f"Unknown artist content category: {category!r} — "
                f"use one of: {', '.join(DAMVenueMatcher.ARTIST_CONTENT_CATEGORIES)}."
            )
        return key

    @staticmethod
    def content_fits(artist_category: str, venue_policy: str) -> bool:
        """True when an artist of this category fits a venue of this policy.
        - originals artist: originals or mixed rooms only
        - covers artist: covers or mixed rooms only
        - mixed artist: any room
        """
        category = DAMVenueMatcher.validate_content_category(artist_category)
        policy = venue_policy.strip().lower()
        if category == "mixed":
            return True
        return category == policy

    # Known city coordinates for location entry by name (latitude, longitude).
    # A musician can type a city from this table, or pass coordinates directly.
    CITY_COORDS = {
        "lancaster, pa": (40.0379, -76.3055),
        "harrisburg, pa": (40.2732, -76.8867),
        "philadelphia, pa": (39.9526, -75.1652),
        "pittsburgh, pa": (40.4406, -79.9959),
        "baltimore, md": (39.2904, -76.6122),
        "nashville, tn": (36.1627, -86.7816),
        "austin, tx": (30.2672, -97.7431),
        "chicago, il": (41.8781, -87.6298),
        "new york, ny": (40.7128, -74.0060),
        "los angeles, ca": (34.0522, -118.2437),
    }

    # Directory of performance venues. The four profile fields — run_by,
    # played_by, vouched_by, pay — plus content_policy are the BookedStage
    # venue profile (approved 2026-11-06; content policy added 2026-11-23).
    # Example venues carry example terms; real venues are filled firsthand.
    VENUE_DIRECTORY = {
        "v_001": {
            "name": "The Velvet Cellar",
            "city": "Nashville, TN",
            "lat": 36.1627,
            "lon": -86.7816,
            "capacity": 150,
            "vibe_audience": "Intimate acoustic listening room, quiet crowd, craft cocktails",
            "preferred_genres": ["acoustic", "folk", "singer-songwriter", "indie-jazz"],
            "content_policy": "originals",
            "pay": "$200 guarantee plus tips (example terms)",
            "run_by": "",
            "played_by": [],
            "vouched_by": [],
            "required_submission_items": ["master_track", "tech_rider"],
            "max_performance_duration_mins": 90,
            "booking_lead_time_weeks": 4,
            "contact_email": "booking@velvetcellar.example.com"
        },
        "v_002": {
            "name": "Electric Pulse Club",
            "city": "Austin, TX",
            "lat": 30.2672,
            "lon": -97.7431,
            "capacity": 500,
            "vibe_audience": "High-energy nighttime dance floor, college/young adult demographic",
            "preferred_genres": ["dj", "edm", "electronic", "house"],
            "content_policy": "covers",
            "pay": "$300 flat (example terms)",
            "run_by": "",
            "played_by": [],
            "vouched_by": [],
            "required_submission_items": ["live_reels", "master_track"],
            "max_performance_duration_mins": 120,
            "booking_lead_time_weeks": 8,
            "contact_email": "talent@electricpulse.example.com"
        },
        "v_003": {
            "name": "Starlight Lounge",
            "city": "Chicago, IL",
            "lat": 41.8781,
            "lon": -87.6298,
            "capacity": 250,
            "vibe_audience": "Mid-sized urban lounge, upbeat vocal performances, pop & backing tracks",
            "preferred_genres": ["pop", "r&b", "vocalist", "tracks"],
            "content_policy": "mixed",
            "pay": "Door split 70/30 (example terms)",
            "run_by": "",
            "played_by": [],
            "vouched_by": [],
            "required_submission_items": ["master_track", "live_reels", "tech_rider"],
            "max_performance_duration_mins": 60,
            "booking_lead_time_weeks": 6,
            "contact_email": "gigs@starlightchicago.example.com"
        },
        "v_004": {
            "name": "Example Listening Room (sample venue)",
            "city": "Lancaster, PA",
            "lat": 40.0379,
            "lon": -76.3055,
            "capacity": 80,
            "vibe_audience": "Quiet listening room, originals-first, early-evening crowd",
            "preferred_genres": ["acoustic", "folk", "singer-songwriter"],
            "content_policy": "originals",
            "pay": "$100 guarantee (example terms)",
            "run_by": "",
            "played_by": [],
            "vouched_by": [],
            "required_submission_items": ["master_track", "tech_rider"],
            "max_performance_duration_mins": 75,
            "booking_lead_time_weeks": 3,
            "contact_email": "booking@examplelancaster.example.com"
        }
    }

    # ---------- distance ----------

    @staticmethod
    def distance_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Straight-line (haversine) distance between two points, in miles."""
        earth_radius_miles = 3958.8
        p1 = math.radians(lat1)
        p2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
        return 2 * earth_radius_miles * math.asin(math.sqrt(a))

    def coords_for_city(self, city: str) -> tuple:
        """Look up a typed-in city name in the known-city table."""
        key = city.strip().lower()
        if key not in self.CITY_COORDS:
            raise ValueError(f"City not in the known-city table yet: {city}")
        return self.CITY_COORDS[key]

    # ---------- v1: single-venue match ----------

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

    def build_custom_pitch_draft(
        self, artist_name: str, artist_genre: str, venue_id: str, artist_category: str = "originals"
    ) -> str:
        """Generates a professional, automated pitch message tailored to the venue's audience."""
        venue = self.VENUE_DIRECTORY[venue_id]
        category = self.validate_content_category(artist_category)
        plays = {"originals": "original", "covers": "cover", "mixed": "original and cover"}[category]

        pitch = (
            f"Subject: Booking Inquiry: {artist_name} ({artist_genre.title()}) @ {venue['name']}\n\n"
            f"Hi {venue['name']} Booking Team,\n\n"
            f"I hope this message finds you well. My name is {artist_name}, performing {plays} {artist_genre} music. "
            f"Given your room's reputation for {venue['vibe_audience']}, I am confident my performance would resonate strongly with your audience.\n\n"
            f"I have assembled a secure, private DAM submission package containing our media sampler and technical rider for your review.\n\n"
            f"Thank you for your time and consideration,\n"
            f"{artist_name}"
        )
        return pitch

    # ---------- v2: location + radius search ----------

    def search_venues(
        self,
        artist_lat: float,
        artist_lon: float,
        radius_miles: float,
        artist_genre: str,
        artist_setup: str,
        artist_category: str = "mixed",
        originals_only: bool = False,
    ) -> List[Dict]:
        """
        Find venues within radius_miles of the artist, ranked by match.

        artist_category is what the artist plays: "originals", "covers", or
        "mixed" (a variety of both). It is paired against each venue's
        content_policy — an originals artist never lands in a covers-only
        room, and a covers artist never lands in an originals-only room.
        A mixed artist fits any room. originals_only=True is kept for
        backward compatibility and means artist_category="originals".

        Hard filters (a venue failing either is excluded entirely):
        - distance beyond the radius
        - artist category vs venue content policy mismatch

        Each result carries the venue's full profile — distance, content
        policy, pay, run_by, played_by, vouched_by — so the musician can
        get familiar with the room before pitching it.
        """
        category = "originals" if originals_only else self.validate_content_category(artist_category)
        results = []

        for venue_id, venue in self.VENUE_DIRECTORY.items():
            dist = self.distance_miles(artist_lat, artist_lon, venue["lat"], venue["lon"])
            if dist > radius_miles:
                continue
            if not self.content_fits(category, venue["content_policy"]):
                continue

            base = self.calculate_match_score(artist_genre, artist_setup, venue_id)
            score = base["match_score_pct"]
            reasons = list(base["match_analysis"])

            # Content-policy fit: the artist's category against the room's policy.
            if category == "originals" and venue["content_policy"] == "originals":
                score += 10
                reasons.append("Content match: venue books originals, and this artist plays originals only.")
            elif category == "originals" and venue["content_policy"] == "mixed":
                reasons.append("Content note: venue is mixed originals/covers — originals are accepted.")
            elif category == "covers" and venue["content_policy"] == "covers":
                score += 10
                reasons.append("Content match: venue books covers, and this artist plays covers.")
            elif category == "covers" and venue["content_policy"] == "mixed":
                reasons.append("Content note: venue is mixed originals/covers — covers are accepted.")
            elif category == "mixed":
                reasons.append(f"Content note: venue books {venue['content_policy']} — a mixed artist fits any room.")

            results.append({
                "venue_id": venue_id,
                "venue_name": venue["name"],
                "city": venue["city"],
                "distance_miles": round(dist, 1),
                "match_score_pct": score,
                "content_policy": venue["content_policy"],
                "artist_category": category,
                "pay": venue["pay"],
                "run_by": venue["run_by"] or "Not yet recorded",
                "played_by": venue["played_by"],
                "vouched_by": venue["vouched_by"],
                "capacity": venue["capacity"],
                "audience_vibe": venue["vibe_audience"],
                "required_assets": venue["required_submission_items"],
                "contact_email": venue["contact_email"],
                "match_analysis": reasons,
            })

        # Best match first; nearest first on a tie.
        results.sort(key=lambda r: (-r["match_score_pct"], r["distance_miles"]))
        return results

    def search_by_city(
        self,
        city: str,
        radius_miles: float,
        artist_genre: str,
        artist_setup: str,
        artist_category: str = "mixed",
        originals_only: bool = False,
    ) -> List[Dict]:
        """search_venues with the artist's location typed in as a city name."""
        lat, lon = self.coords_for_city(city)
        return self.search_venues(lat, lon, radius_miles, artist_genre, artist_setup, artist_category, originals_only)


# --- DEMO EXECUTION ---
if __name__ == "__main__":
    print(DAM_BANNER)
    matcher = DAMVenueMatcher()

    def show(title, results):
        print(f"\n=== {title} ===")
        if not results:
            print("No venues found under those terms.")
        for r in results:
            print(f"{r['venue_name']} — {r['city']} — {r['distance_miles']} mi away")
            print(f"  Match: {r['match_score_pct']}%  |  Artist: {r['artist_category']}  |  Content: {r['content_policy']}  |  Pay: {r['pay']}")
            print(f"  Run by: {r['run_by']}  |  Played by: {', '.join(r['played_by']) or 'Not yet recorded'}  |  Vouched by: {', '.join(r['vouched_by']) or 'Not yet recorded'}")
            for reason in r["match_analysis"]:
                print(f"  - {reason}")

    # Rich's own case: originals-only singer-songwriter standing in Lancaster.
    show(
        "LANCASTER, 25-MILE SEARCH — originals artist",
        matcher.search_by_city("Lancaster, PA", 25, "singer-songwriter", "Acoustic Singer-Songwriter", artist_category="originals"),
    )
    show(
        "LANCASTER, 800-MILE SEARCH — originals artist",
        matcher.search_by_city("Lancaster, PA", 800, "singer-songwriter", "Acoustic Singer-Songwriter", artist_category="originals"),
    )
    # Policy filter proof: the only room within 25 miles of Austin is
    # covers-only, so an originals artist gets no match there — while a
    # covers artist matches it, and a mixed artist matches it too.
    show(
        "AUSTIN, 25-MILE SEARCH — originals artist (covers-only room must not appear)",
        matcher.search_by_city("Austin, TX", 25, "singer-songwriter", "Acoustic Singer-Songwriter", artist_category="originals"),
    )
    show(
        "AUSTIN, 25-MILE SEARCH — covers artist (the covers-only room appears)",
        matcher.search_by_city("Austin, TX", 25, "singer-songwriter", "Acoustic Singer-Songwriter", artist_category="covers"),
    )
    show(
        "AUSTIN, 25-MILE SEARCH — mixed artist (any room fits)",
        matcher.search_by_city("Austin, TX", 25, "singer-songwriter", "Acoustic Singer-Songwriter", artist_category="mixed"),
    )

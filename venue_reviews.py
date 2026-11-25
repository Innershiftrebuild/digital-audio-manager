# +==========================================================================+
# |                             healthvenom.com                              |
# |                            Health Venom Inc.                             |
# |                                                                          |
# |   _   _ _____    _    _   _____ _   ___     _______ _   _  ___  __  __   |
# |  | | | | ____|  / \  | | |_   _| | | \ \   / / ____| \ | |/ _ \|  \/  |  |
# |  | |_| |  _|   / _ \ | |   | | |_| |\ \ / /|  _| |  \| | | | | |\/| |  |
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
|  | |_| |  _|   / _ \ | |   | | |_| |\ \ / /|  _| |  \| | | | | |\/| |  |
|  |  _  | |___ / ___ \| |___| | |  _  | \ V / | |___| |\  | |_| | |  | |  |
|  |_| |_|_____/_/   \_\_____|_| |_| |_|  \_/  |_____|_| \_|\___/|_|  |_|  |
|                                                                          |
|               The DAM / BookedStage - Sanitas Mentis Inc.                |
|                  Imprinted in the code, so it lives on.                  |
+==========================================================================+
"""

from datetime import date, datetime
from typing import Dict, List, Optional


class DAMVenueReviews:
    """
    DAM Venue Reviews (venue_reviews.py) — the accommodation for the
    musician after the gig, added 2026-11-24, per Rich.

    This is the Google Maps layer he asked for: a musician who played a
    room through BookedStage can tell other musicians how it went — the
    rating, whether the pay came as promised, how they were treated, the
    sound, and whether they would play there again — so the communication
    between musicians grows room by room.

    The rules, plainly:

    1. NAMED ONLY. No anonymous ratings. A review carries the musician's
       name, the room, and the date they played it. A nameless word is not
       a vouch and not a review.
    2. PLAYED IT ONLY. Only a musician who played the room can review it.
       The date played is required, and it cannot be in the future.
    3. ONE WORD PER GIG. One review per musician, per room, per date
       played. A second review for the same gig is refused.
    4. RATINGS ARE THE CROWD'S WORD. The average rating, the
       would-play-again share, and the pay-as-promised share are what
       musicians said after their gigs. They are never the trusted badge.
    5. THE TRUSTED BADGE IS A FIRSTHAND VOUCH — FROM SOMEONE WHO PLAYED
       THE ROOM. A room earns the trusted badge only when a named
       musician vouches for it firsthand (vouched_by in
       venue_matching.py) AND that musician is recorded as having played
       the room (played_by). A vouch from someone who never played there
       does not count. Ratings never confer the badge, and the badge
       never stands in for ratings. The two never stand in for each other.

    This module records how gigs went. The listing rule, as Rich ruled
    it 2026-11-24: candidate rooms go live marked unverified, and the
    trusted badge comes only from a named firsthand vouch (see rule 5).
    """

    RATING_MIN = 1
    RATING_MAX = 5
    NOTE_MAX_CHARS = 500

    def __init__(self):
        # Stored reviews, in the order they were added.
        self._reviews: List[Dict] = []

    # ---------- adding a review ----------

    def add_review(
        self,
        venue: str,
        musician: str,
        date_played: str,
        rating: int,
        pay_as_promised: Optional[bool] = None,
        treated_well: Optional[bool] = None,
        sound_ok: Optional[bool] = None,
        would_play_again: Optional[bool] = None,
        note: str = "",
    ) -> Dict:
        """
        Record how a gig went, from the musician who played it.

        venue: the room, as "Name, City, ST" (e.g. "The Evening Muse,
            Charlotte, NC"). musician: the reviewer's name — required,
            never anonymous. date_played: "YYYY-MM-DD", the night of the
            gig — required, and never in the future. rating: 1–5, the
            whole gig in one number. pay_as_promised / treated_well /
            sound_ok / would_play_again: True or False where the musician
            says so, None where they did not say. note: their words, up
            to 500 characters.
        """
        venue = (venue or "").strip()
        if not venue:
            raise ValueError("A review needs the room — venue is required.")
        musician = (musician or "").strip()
        if not musician:
            raise ValueError(
                "A review is named only — musician is required. "
                "A nameless word is not a review."
            )
        try:
            played = datetime.strptime(date_played.strip(), "%Y-%m-%d").date()
        except (ValueError, AttributeError):
            raise ValueError(
                f"date_played must be YYYY-MM-DD, got {date_played!r}."
            )
        if played > date.today():
            raise ValueError(
                f"date_played {date_played} is in the future — "
                "only a gig already played can be reviewed."
            )
        if not isinstance(rating, int) or isinstance(rating, bool):
            raise ValueError(f"rating must be a whole number 1–5, got {rating!r}.")
        if not (self.RATING_MIN <= rating <= self.RATING_MAX):
            raise ValueError(
                f"rating must be {self.RATING_MIN}–{self.RATING_MAX}, got {rating}."
            )
        note = (note or "").strip()
        if len(note) > self.NOTE_MAX_CHARS:
            raise ValueError(
                f"note is {len(note)} characters — keep it to "
                f"{self.NOTE_MAX_CHARS} or fewer."
            )
        for existing in self._reviews:
            if (
                existing["venue"].lower() == venue.lower()
                and existing["musician"].lower() == musician.lower()
                and existing["date_played"] == date_played.strip()
            ):
                raise ValueError(
                    f"{musician} already reviewed {venue} for "
                    f"{date_played} — one word per gig."
                )

        review = {
            "venue": venue,
            "musician": musician,
            "date_played": date_played.strip(),
            "rating": rating,
            "pay_as_promised": pay_as_promised,
            "treated_well": treated_well,
            "sound_ok": sound_ok,
            "would_play_again": would_play_again,
            "note": note,
        }
        self._reviews.append(review)
        return dict(review)

    # ---------- reading reviews ----------

    def reviews_for(self, venue: str) -> List[Dict]:
        """All reviews for one room, newest gig first."""
        venue = (venue or "").strip().lower()
        matches = [r for r in self._reviews if r["venue"].lower() == venue]
        matches.sort(key=lambda r: r["date_played"], reverse=True)
        return [dict(r) for r in matches]

    def average_rating(self, venue: str) -> Optional[float]:
        """The room's average rating, or None when no one has reviewed it."""
        reviews = self.reviews_for(venue)
        if not reviews:
            return None
        return round(sum(r["rating"] for r in reviews) / len(reviews), 1)

    def _share_true(self, venue: str, field: str) -> Optional[float]:
        """Share of reviews answering True on a yes/no field, or None."""
        answers = [
            r[field] for r in self.reviews_for(venue) if r[field] is not None
        ]
        if not answers:
            return None
        return round(100 * sum(1 for a in answers if a) / len(answers))

    def would_play_again_pct(self, venue: str) -> Optional[float]:
        """Share of reviewers who would play the room again, or None."""
        return self._share_true(venue, "would_play_again")

    def pay_as_promised_pct(self, venue: str) -> Optional[float]:
        """Share of reviewers whose pay came as promised, or None."""
        return self._share_true(venue, "pay_as_promised")

    def venue_summary(self, venue: str) -> Dict:
        """One room's whole story, as the musicians told it."""
        reviews = self.reviews_for(venue)
        latest_note = next(
            (r["note"] for r in reviews if r["note"]), ""
        )
        return {
            "venue": venue,
            "review_count": len(reviews),
            "average_rating": self.average_rating(venue),
            "would_play_again_pct": self.would_play_again_pct(venue),
            "pay_as_promised_pct": self.pay_as_promised_pct(venue),
            "latest_note": latest_note,
        }

    def venues_reviewed(self) -> List[str]:
        """Every room that carries at least one review, in first-seen order."""
        seen: List[str] = []
        for review in self._reviews:
            if review["venue"] not in seen:
                seen.append(review["venue"])
        return seen

    # ---------- the trusted badge (firsthand vouch, not ratings) ----------

    @staticmethod
    def verified_vouches(vouched_by: List[str], played_by: List[str]) -> List[str]:
        """
        The vouches that count: names in BOTH lists — a named musician
        who verifiably played the room. A vouch from someone who never
        played there does not count. Matching ignores case and
        surrounding spaces.
        """
        played = {
            name.strip().lower()
            for name in (played_by or [])
            if isinstance(name, str) and name.strip()
        }
        verified: List[str] = []
        for name in vouched_by or []:
            if (
                isinstance(name, str)
                and name.strip()
                and name.strip().lower() in played
                and name.strip() not in verified
            ):
                verified.append(name.strip())
        return verified

    @staticmethod
    def trusted_badge(vouched_by: List[str], played_by: List[str]) -> bool:
        """
        True only when a named musician who verifiably played the room
        vouches for it firsthand — at least one name in BOTH vouched_by
        and played_by (from venue_matching.py). Ratings never confer the
        badge.
        """
        return bool(DAMVenueReviews.verified_vouches(vouched_by, played_by))


# --- DEMO EXECUTION ---
# SAMPLE reviews only — fictional sample musicians on the sample rooms.
# No sample below is a real gig, a real vouch, or a real musician.
if __name__ == "__main__":
    print(DAM_BANNER)
    reviews = DAMVenueReviews()

    reviews.add_review(
        venue="The Corner Taproom, Lancaster, PA",
        musician="Sample Busker",
        date_played="2026-11-21",
        rating=5,
        pay_as_promised=True,
        treated_well=True,
        sound_ok=True,
        would_play_again=True,
        note="Paid what was agreed, room listened, would come back.",
    )
    reviews.add_review(
        venue="The Corner Taproom, Lancaster, PA",
        musician="Sample Songwriter",
        date_played="2026-11-14",
        rating=4,
        pay_as_promised=True,
        treated_well=True,
        sound_ok=False,
        would_play_again=True,
        note="Good room, kind host. Bring your own monitor.",
    )
    reviews.add_review(
        venue="Electric Pulse Club, Austin, TX",
        musician="Sample Busker",
        date_played="2026-11-07",
        rating=3,
        pay_as_promised=False,
        treated_well=True,
        sound_ok=True,
        would_play_again=False,
        note="Paid short of what was agreed. Room itself was fine.",
    )

    for venue in reviews.venues_reviewed():
        summary = reviews.venue_summary(venue)
        print(f"\n=== {venue} ===")
        print(f"Reviews: {summary['review_count']}  |  Average: {summary['average_rating']}/5")
        print(f"Would play again: {summary['would_play_again_pct']}%  |  Pay as promised: {summary['pay_as_promised_pct']}%")
        if summary["latest_note"]:
            print(f"Latest word: \"{summary['latest_note']}\"")
        print(f"Trusted badge (vouched + played): {DAMVenueReviews.trusted_badge(['Sample Busker'], ['Sample Busker'])}")
        print(f"Trusted badge (vouched, never played): {DAMVenueReviews.trusted_badge(['Sample Busker'], ['Other Musician'])}")
        print(f"Trusted badge (no vouch): {DAMVenueReviews.trusted_badge([], ['Sample Busker'])}")

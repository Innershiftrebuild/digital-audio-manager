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
|  |  |  _  | |___ / ___ \| |___| | |  _  | \ V / | |___| |\  | |_| | |  | |  |
|  |_| |_|_____/_/   \_\_____|_| |_| |_|  \_/  |_____|_| \_|\___/|_|  |_|  |
|                                                                          |
|               The DAM / BookedStage - Sanitas Mentis Inc.                |
|                  Imprinted in the code, so it lives on.                  |
+==========================================================================+
"""

from typing import Dict, List, Optional

class DAMGrantFinder:
    """
    DAM Grant Finder (grants.py) — built-in grant-finding resource for
    BookedStage (added 2026-11-24, per Rich).

    Financial resources only — no personal business contacts. Every entry
    carries who is eligible for the financing, so a musician can see at a
    glance whether the door is open to them directly, open to their small
    business, or open only through a nonprofit partner.

    The structural point, first: Rich's companies (Sanitas Mentis Inc. and
    HealthVenom Inc.) are for-profit Pennsylvania corporations. Most arts,
    wellbeing and community grants go only to nonprofits (or to individuals
    for a specific project). So the directory is split by who the money is
    for: "individual", "small_business", or "nonprofit_only" — where the
    door opens only through a nonprofit partner. Hardship assistance and
    free help are their own kinds, not project funding.

    Verification rule: "verified" means the entry was confirmed at the
    funder's or organizer's own site on November 24, 2026. Anything not so
    confirmed is labeled unverified in plain words, in "notes" — never
    stated as settled. One verified fact never verifies its neighbors.
    """

    # Who the money is for.
    APPLICANT_TYPES = ("individual", "small_business", "nonprofit_partner", "any")
    # What kind of resource it is.
    RESOURCE_KINDS = ("grant", "assistance", "donation", "free_help")

    # Directory of financial resources. "deadline_sort" is an ISO date for
    # sorting (None = rolling / no fixed date, sorts last). "door" is
    # "direct" (open to the applicant as they are) or "via_partner" (open
    # only through a nonprofit partner).
    GRANT_DIRECTORY = {
        # --- Grants open to individuals ---
        "awesome-foundation": {
            "name": "Awesome Foundation",
            "kind": "grant",
            "who": "individual",
            "door": "direct",
            "amount": "$1,000",
            "deadline": "Rolling — no deadline",
            "deadline_sort": None,
            "eligibility": "Anyone — individuals, groups, and organizations alike.",
            "fit": "Inner Shift Rebuild or BookedStage as a specific project — the free six-door recording, a Lancaster busking series, a venue-mapping sprint. Apply to a chapter that fits the project; most chapters prefer their own city.",
            "caution": "Do NOT promise the same recording to two funders: the November draft promised the free six-door recording, and the Verizon paragraph aims at the full nine-door sets.",
            "contact": "",
            "source": "awesomefoundation.org",
            "verified": True,
            "notes": "",
        },
        "creative-capital": {
            "name": "Creative Capital Award",
            "kind": "grant",
            "who": "individual",
            "door": "direct",
            "amount": "Up to $50,000, unrestricted",
            "deadline": "Next cycle expected spring 2027 (unverified)",
            "deadline_sort": "2027-04-01",
            "eligibility": "Individual artists: U.S. citizen or permanent resident, 25+, at least five years of professional artistic practice.",
            "fit": "A strong long shot for a future cycle — Inner Shift Rebuild as socially engaged practice, or the song work. Watch creative-capital.org; do not plan on it for 2026.",
            "caution": "",
            "contact": "",
            "source": "creative-capital.org",
            "verified": True,
            "notes": "2027 cycle closed April 2, 2026 (verified). Next cycle expected spring 2027 — unverified.",
        },
        "ppa-project-stream": {
            "name": "Pennsylvania Partners in the Arts — Project Stream (Berks Arts Council, Region 7)",
            "kind": "grant",
            "who": "individual",
            "door": "direct",
            "amount": "Historic grants ran up to $2,500 (2018–19 guidelines — stale figure)",
            "deadline": "Current cycle dates unverified — check with Berks Arts",
            "deadline_sort": None,
            "eligibility": "Individual artists and organizations, for arts projects with a public component in Berks, Lancaster, or Schuylkill counties.",
            "fit": "The most direct state-arts door for an individual artist in Lancaster County — a project grant for a public music or spoken-question project.",
            "caution": "",
            "contact": "Amanda Ehst, amanda@berksarts.org, 610-898-1930 ext. 23",
            "source": "pa.gov partnership map; berksarts.org",
            "verified": True,
            "notes": "Program and region verified. Current cycle dates and amounts unverified — check with Berks Arts.",
        },
        "fai-first-timer": {
            "name": "Folk Alliance International — First-Timer Artist Scholarships",
            "kind": "grant",
            "who": "individual",
            "door": "direct",
            "amount": "50–100% of conference registration",
            "deadline": "December 22, 2026",
            "deadline_sort": "2026-12-22",
            "eligibility": "First-time FAI attendees (artists and industry). FAI membership required once accepted.",
            "fit": "Makes the January 2027 FAI conference in Chicago affordable.",
            "caution": "",
            "contact": "",
            "source": "folk.org",
            "verified": True,
            "notes": "",
        },
        # --- Grants open to small businesses ---
        "ifundwomen": {
            "name": "IFundWomen Startup Accelerator",
            "kind": "grant",
            "who": "small_business",
            "door": "direct",
            "amount": "$5,000 — one winner nationally",
            "deadline": "November 30, 2026, 11:59 PM ET",
            "deadline_sort": "2026-11-30",
            "eligibility": "Small businesses. $5 fee to apply.",
            "fit": "Flagged plainly: IFundWomen's programs are built for women founders — Rich is not their target applicant. Long odds; his call.",
            "caution": "",
            "contact": "",
            "source": "Rich's record",
            "verified": False,
            "notes": "Deadline and amount from Rich's record, not confirmed at the funder's site.",
        },
        "verizon-digital-ready": {
            "name": "Verizon Digital Ready — $10,000 Grant",
            "kind": "grant",
            "who": "small_business",
            "door": "direct",
            "amount": "$10,000",
            "deadline": "Complete any 2 free courses by December 6, 2026; gate December 7, 2026",
            "deadline_sort": "2026-12-06",
            "eligibility": "Small businesses that complete any 2 free Digital Ready courses.",
            "fit": "Free courses. The use-of-funds paragraph aims at the full nine-door sets.",
            "caution": "Do NOT promise the same recording to two funders (see Awesome Foundation).",
            "contact": "",
            "source": "Rich's record",
            "verified": False,
            "notes": "Dates and amount from Rich's record, not confirmed at the funder's site.",
        },
        "skip-fall": {
            "name": "Skip Fall Grant",
            "kind": "grant",
            "who": "small_business",
            "door": "direct",
            "amount": "Amount not stated in the research — verify on the Skip site",
            "deadline": "December 17, 2026",
            "deadline_sort": "2026-12-17",
            "eligibility": "Small businesses.",
            "fit": "A dated gate on the calendar.",
            "caution": "",
            "contact": "",
            "source": "Rich's record",
            "verified": False,
            "notes": "Deadline from Rich's record. Amount and terms unverified.",
        },
        "lccf-fig-tree": {
            "name": "LCCF Fig Tree Grants",
            "kind": "grant",
            "who": "small_business",
            "door": "direct",
            "amount": "Amounts unverified — verify on lancfound.org when the window opens",
            "deadline": "Applications March 1 – May 1, 2027 (per a grant listing — unverified)",
            "deadline_sort": "2027-03-01",
            "eligibility": "Small business owners in Lancaster City.",
            "fit": "The one Lancaster County Community Foundation door built for a small business rather than a nonprofit — BookedStage or Inner Shift Rebuild as a Lancaster City business.",
            "caution": "",
            "contact": "",
            "source": "lancfound.org",
            "verified": True,
            "notes": "Program verified on the Foundation's grants page. Application window and amounts unverified.",
        },
        # --- Grants that are nonprofit-only: open only through a partner ---
        "pa-creative-catalyst": {
            "name": "PA Creative Catalyst Grant (PA Council on the Arts)",
            "kind": "grant",
            "who": "nonprofit_only",
            "door": "via_partner",
            "amount": "Up to $25,000",
            "deadline": "February 12, 2027",
            "deadline_sort": "2027-02-12",
            "eligibility": "Nonprofit tax-exempt corporation, unit of government, college/university, or school district ONLY. Fiscal agents and fiscal sponsors are NOT eligible. 1:1 cash match required; paid by reimbursement; no more than 20% for admin.",
            "fit": "Only through a nonprofit partner — e.g., a Lancaster nonprofit applying for a project that amplifies local creatives, with Rich's work as the program. A partnership conversation first, not an application.",
            "caution": "Rich's for-profit corporations cannot apply.",
            "contact": "",
            "source": "pa.gov 2026–27 guidelines",
            "verified": True,
            "notes": "",
        },
        "lccf-competitive": {
            "name": "Lancaster County Community Foundation — Competitive Grants",
            "kind": "grant",
            "who": "nonprofit_only",
            "door": "via_partner",
            "amount": "2026 Passion Grants ran $7,500–$37,000 (unverified for 2027)",
            "deadline": "Reopen March 2027; eligibility screen ~May 6, application ~May 13 (unverified)",
            "deadline_sort": "2027-03-01",
            "eligibility": "Community benefit organizations serving Lancaster County — not individuals, not for-profit businesses.",
            "fit": "Only through a nonprofit partner, or if a future Rich nonprofit ever exists (the Busker nonprofit is on hold until revenue shows).",
            "caution": "",
            "contact": "",
            "source": "lancfound.org",
            "verified": True,
            "notes": "Program verified. 2027 amounts and exact dates unverified.",
        },
        # --- Hardship assistance: help in hardship, not project funding ---
        "musicares": {
            "name": "MusiCares",
            "kind": "assistance",
            "who": "individual",
            "door": "direct",
            "amount": "Amounts not published; their latest Form 990 describes general assistance up to $10,000 a year (secondary source — unverified)",
            "deadline": "Rolling",
            "deadline_sort": None,
            "eligibility": "Individual music professionals in the U.S.: 5+ years of paid music-industry work (need not be consecutive) OR credits on 6+ commercially released recordings/videos.",
            "fit": "Hardship and mental-health support for a working musician. Covers rent/mortgage, utilities, medical and mental-health costs; payments go directly to providers, not to the applicant.",
            "caution": "Eligibility is uncertain for Rich: five years of paid music work, or six released credits, must be documented. Ask MusiCares before assuming either way.",
            "contact": "800-687-4227",
            "source": "musicares.org",
            "verified": True,
            "notes": "This is help in hardship, not project funding.",
        },
        "sweet-relief": {
            "name": "Sweet Relief Musicians Fund",
            "kind": "assistance",
            "who": "individual",
            "door": "direct",
            "amount": "Case-by-case; amounts not published",
            "deadline": "Rolling",
            "deadline_sort": None,
            "eligibility": "Career musicians and music-industry workers facing illness, disability, or age-related problems. Requires a serious medical or mental-health condition, demonstrated financial need, and — for industry workers — at least 50% of annual income from music work. Musicians must have regular public performances or 3+ widely released recordings.",
            "fit": "Uncertain. His MS is a serious medical condition, which meets the medical test, but the 50%-of-income-from-music test is likely a problem at his current income level. A request can be made with a written explanation if the criteria are not fully met — the fund says so on its own page.",
            "caution": "Do not assume eligibility.",
            "contact": "",
            "source": "sweetrelief.org",
            "verified": True,
            "notes": "This is help in hardship, not project funding.",
        },
        # --- Donations ---
        "ko-fi": {
            "name": "Ko-fi — Donations to Rich's Work",
            "kind": "donation",
            "who": "individual",
            "door": "direct",
            "amount": "Individual donations, any size",
            "deadline": "Open now",
            "deadline_sort": None,
            "eligibility": "Anyone who wants to give.",
            "fit": "Individual donations currently flow through ko-fi.com/healthvenom. Larger donations and grants from foundations generally need a nonprofit recipient — his for-profit corporations cannot receive tax-deductible donations. If a donor or foundation wants to fund the entertainers'-wellbeing mission at scale, the honest route is a nonprofit fiscal sponsor or a partner nonprofit.",
            "caution": "",
            "contact": "",
            "source": "ko-fi.com/healthvenom",
            "verified": True,
            "notes": "",
        },
        # --- Free help: the avenues that lead to funding ---
        "score-lancaster": {
            "name": "SCORE Lancaster-Lebanon — Free Mentoring",
            "kind": "free_help",
            "who": "small_business",
            "door": "direct",
            "amount": "FREE",
            "deadline": "Open now",
            "deadline_sort": None,
            "eligibility": "New and established small businesses.",
            "fit": "The first call for BookedStage and Inner Shift Rebuild as businesses — a mentor who has run a business, for free, in his own city. 50+ volunteer mentors; free, confidential, face-to-face mentoring; affordable seminars; business roundtables.",
            "caution": "",
            "contact": "313 W Liberty St, Lancaster, PA; (717) 397-3092",
            "source": "Lancaster business guides",
            "verified": True,
            "notes": "",
        },
        "kutztown-sbdc": {
            "name": "Kutztown University SBDC — Free Confidential Consulting",
            "kind": "free_help",
            "who": "small_business",
            "door": "direct",
            "amount": "FREE",
            "deadline": "Open now",
            "deadline_sort": None,
            "eligibility": "Small businesses in Berks, Chester, Dauphin, Lancaster, and Lebanon counties.",
            "fit": "The office that helps a business find money — the right place to take the BookedStage pricing ($9/mo) and the ISR tiers and ask what funding fits. One-on-one consulting to test a business proposition, shape a business plan, and investigate funding.",
            "caution": "",
            "contact": "(484) 646-5937; sbdc@kutztown.edu",
            "source": "kutztown.edu",
            "verified": True,
            "notes": "",
        },
        "assets-lancaster": {
            "name": "ASSETS — Training and Microloans for Lancaster Entrepreneurs",
            "kind": "free_help",
            "who": "small_business",
            "door": "direct",
            "amount": "Microloans — terms unverified",
            "deadline": "Open now",
            "deadline_sort": None,
            "eligibility": "Lancaster entrepreneurs.",
            "fit": "Training and microloans for Lancaster entrepreneurs. The Discovery Call is the next step, and it is already on Rich's list.",
            "caution": "",
            "contact": "(717) 393-6089",
            "source": "Rich's record",
            "verified": False,
            "notes": "Details unverified for this file — the call itself is the next step.",
        },
        "cultivate-lancaster": {
            "name": "Cultivate Lancaster — Free Mentorship",
            "kind": "free_help",
            "who": "small_business",
            "door": "direct",
            "amount": "FREE",
            "deadline": "Open now",
            "deadline_sort": None,
            "eligibility": "Lancaster entrepreneurs, startups, and small businesses.",
            "fit": "A mentor network built for Lancaster founders specifically — closer to his size than the Chamber. One-on-one mentorship and a digital hub of resources.",
            "caution": "",
            "contact": "",
            "source": "The Candy Factory's Lancaster resource guide",
            "verified": True,
            "notes": "",
        },
    }

    # ---------- finder ----------

    def find_grants(
        self,
        applicant_type: str = "any",
        kind: str = "any",
    ) -> List[Dict]:
        """
        Find financial resources by who the money is for and what kind it is.

        applicant_type: "individual" (an individual artist), "small_business"
        (a for-profit small business), "nonprofit_partner" (a nonprofit
        applying — or a for-profit working through one), or "any".
        kind: "grant", "assistance", "donation", "free_help", or "any".

        Results are ordered by deadline — dated doors first, rolling last —
        and each carries its eligibility in plain words, so the musician can
        see whether the door is open to them directly or only through a
        nonprofit partner.
        """
        applicant_type = applicant_type.strip().lower()
        if applicant_type not in self.APPLICANT_TYPES:
            raise ValueError(
                f"Unknown applicant type: {applicant_type!r} — "
                f"use one of: {', '.join(self.APPLICANT_TYPES)}."
            )
        kind = kind.strip().lower()
        if kind != "any" and kind not in self.RESOURCE_KINDS:
            raise ValueError(
                f"Unknown resource kind: {kind!r} — "
                f"use one of: {', '.join(self.RESOURCE_KINDS)}."
            )

        entries = []
        for resource_id, entry in self.GRANT_DIRECTORY.items():
            if applicant_type != "any":
                if applicant_type == "nonprofit_partner":
                    if entry["who"] != "nonprofit_only":
                        continue
                elif entry["who"] != applicant_type:
                    continue
            if kind != "any" and entry["kind"] != kind:
                continue
            entries.append((resource_id, entry))

        # Dated doors first (earliest first); rolling doors last.
        entries.sort(key=lambda pair: (pair[1]["deadline_sort"] is None, pair[1]["deadline_sort"] or ""))

        results = []
        for resource_id, entry in entries:
            results.append({
                "resource_id": resource_id,
                "name": entry["name"],
                "kind": entry["kind"],
                "who": entry["who"],
                "door": entry["door"],
                "amount": entry["amount"],
                "deadline": entry["deadline"],
                "eligibility": entry["eligibility"],
                "fit": entry["fit"],
                "caution": entry["caution"],
                "contact": entry["contact"],
                "source": entry["source"],
                "verified": entry["verified"],
                "notes": entry["notes"],
            })

        return results

    def find_for_rich(self) -> Dict:
        """
        Rich's own split: what is open to him directly as an individual
        artist and small-business owner, and what opens only through a
        nonprofit partner. His companies are for-profit; the partner doors
        are partnership conversations first, not applications.
        """
        direct = (
            self.find_grants(applicant_type="individual")
            + self.find_grants(applicant_type="small_business")
        )
        via_partner = self.find_grants(applicant_type="nonprofit_partner")
        return {"direct": direct, "via_partner": via_partner}


# --- DEMO EXECUTION ---
if __name__ == "__main__":
    print(DAM_BANNER)
    finder = DAMGrantFinder()

    def show(title, results):
        print(f"\n=== {title} ===")
        if not results:
            print("No resources under those terms.")
        for r in results:
            check = "verified" if r["verified"] else "UNVERIFIED"
            print(f"{r['name']} — {r['amount']} — {r['deadline']} [{check}]")
            print(f"  For: {r['who']}  |  Door: {r['door']}  |  Kind: {r['kind']}")
            print(f"  Eligible: {r['eligibility']}")
            if r["caution"]:
                print(f"  Caution: {r['caution']}")
            if r["notes"]:
                print(f"  Note: {r['notes']}")

    show("INDIVIDUAL ARTIST — grants open directly", finder.find_grants(applicant_type="individual", kind="grant"))
    show("SMALL BUSINESS — grants open directly", finder.find_grants(applicant_type="small_business", kind="grant"))
    show("NONPROFIT PARTNER — grants open only through a partner", finder.find_grants(applicant_type="nonprofit_partner"))
    show("FREE HELP — the avenues that lead to funding", finder.find_grants(kind="free_help"))

    split = finder.find_for_rich()
    print(f"\n=== RICH'S SPLIT ===")
    print(f"Direct doors: {len(split['direct'])}  |  Via a nonprofit partner: {len(split['via_partner'])}")

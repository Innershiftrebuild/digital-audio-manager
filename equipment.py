# create separate files for each module of **DAM** :
# -
# `vault.py` Holds the **Secure Asset Vault & Link Expiration** code.
#
# -
# `equipment.py` Holds the **Equipment Registry & Pricing** code.
#
# -
# `venue_matching.py` Holds the upcoming **Venue Directory** code.
#
# Open your `digital-audio-manager` repository on **GitHub** (via your iPhone or browser).
#
# Tap on `vault.py` (or create `equipment.py`).
# Tap the **Edit (pencil icon)**, paste this updated Python class in, and click **Commit changes**.
#
import json
from typing import Dict, List

class DAMEquipmentRegistryWithPricing:
    """
    DAM Audio Equipment Registry & Tech Rider Generator
    Includes dual-tier pricing: 'Good-Enough' vs 'Highest Sound Quality'.
    """

    EQUIPMENT_DATABASE = {
        "acoustic_solo": {
            "title": "Acoustic Singer-Songwriter",
            "required_inputs": 2,
            "gear_recommendations": [
                {
                    "category": "Direct Input (DI) Box",
                    "good_enough": {
                        "name": "Whirlwind IMP 2 Passive DI",
                        "estimated_price": "$65",
                        "why_it_works": "Indestructible, clean passive transformer for local gigs."
                    },
                    "pro_tour_grade": {
                        "name": "L.R. Baggs Para Acoustic DI",
                        "estimated_price": "$249",
                        "why_it_works": "Studio-grade 5-band parametric EQ + notch filter to kill acoustic feedback instantly."
                    }
                },
                {
                    "category": "Vocal Microphone",
                    "good_enough": {
                        "name": "Shure SM58 Dynamic Mic",
                        "estimated_price": "$99",
                        "why_it_works": "The industry standard workhorse. Every sound engineer knows how to mix it."
                    },
                    "pro_tour_grade": {
                        "name": "Telefunken M80 Dynamic Mic",
                        "estimated_price": "$249",
                        "why_it_works": "Condenser-like detail and high-end clarity without stage feedback."
                    }
                }
            ],
            "rider_text": "Artist requires 2 channel inputs (1 Vocal XLR, 1 Acoustic Guitar XLR via DI box)."
        },
        "singer_with_tracks": {
            "title": "Vocalist with Backing Tracks",
            "required_inputs": 3,
            "gear_recommendations": [
                {
                    "category": "Audio Interface / Track Output",
                    "good_enough": {
                        "name": "Focusrite Scarlett 2i2 (Gen 4)",
                        "estimated_price": "$199",
                        "why_it_works": "Clean balanced outputs, ultra-low noise preamps, plug-and-play USB-C."
                    },
                    "pro_tour_grade": {
                        "name": "Radial USB-Pro Stereo Laptop DI",
                        "estimated_price": "$329",
                        "why_it_works": "Built-in 24-bit DAC with transformer isolation to prevent laptop ground hum/buzz."
                    }
                },
                {
                    "category": "Vocal Microphone",
                    "good_enough": {
                        "name": "Sennheiser e835 Dynamic Mic",
                        "estimated_price": "$100",
                        "why_it_works": "Cuts through dense backing tracks with a crisp presence boost."
                    },
                    "pro_tour_grade": {
                        "name": "Neumann KMS 105 Stage Condenser",
                        "estimated_price": "$749",
                        "why_it_works": "Ultra-rich studio vocal tone engineered specifically for live stage use."
                    }
                }
            ],
            "rider_text": "Artist requires 3 channel inputs (1 Vocal Mic, 2 Stereo Track L/R)."
        },
        "dj_electronic": {
            "title": "DJ / Electronic Solo Artist",
            "required_inputs": 2,
            "gear_recommendations": [
                {
                    "category": "Stereo DI Box (Controller Protection)",
                    "good_enough": {
                        "name": "Livewire SPDI Passive Stereo DI",
                        "estimated_price": "$70",
                        "why_it_works": "Dual 1/4\" inputs to XLR outputs with attenuation pads for hot signals."
                    },
                    "pro_tour_grade": {
                        "name": "Radial ProD2 Passive Stereo DI",
                        "estimated_price": "$239",
                        "why_it_works": "Custom Eclipse transformers block 48V phantom power damage and keep bass tight."
                    }
                },
                {
                    "category": "DJ Booth / DJ Headphones",
                    "good_enough": {
                        "name": "Audio-Technica ATH-M50x",
                        "estimated_price": "$149",
                        "why_it_works": "Excellent passive sound isolation and punchy bass for beatmatching."
                    },
                    "pro_tour_grade": {
                        "name": "Sennheiser HD 25",
                        "estimated_price": "$150",
                        "why_it_works": "Lightweight legendary club standard designed for high-noise DJ booths."
                    }
                }
            ],
            "rider_text": "Artist provides Master Stereo XLR feed. Venue provides booth monitor wedge with local volume control."
        }
    }

    def get_gear_cost_summary(self, setup_type: str) -> Dict:
        """Calculates budget tier costs vs pro tour-grade setup costs."""
        if setup_type not in self.EQUIPMENT_DATABASE:
            raise ValueError(f"Unknown setup type: {setup_type}")

        data = self.EQUIPMENT_DATABASE[setup_type]
        good_enough_items = []
        pro_items = []

        for item in data["gear_recommendations"]:
            good_enough_items.append({
                "category": item["category"],
                "item": item["good_enough"]["name"],
                "price": item["good_enough"]["estimated_price"],
                "note": item["good_enough"]["why_it_works"]
            })
            pro_items.append({
                "category": item["category"],
                "item": item["pro_tour_grade"]["name"],
                "price": item["pro_tour_grade"]["estimated_price"],
                "note": item["pro_tour_grade"]["why_it_works"]
            })

        return {
            "setup_type": data["title"],
            "good_enough_tier": good_enough_items,
            "pro_tour_grade_tier": pro_items
        }

# --- DEMO EXECUTION ---
if __name__ == "__main__":
    registry = DAMEquipmentRegistryWithPricing()
    summary = registry.get_gear_cost_summary("acoustic_solo")

    print(f"=== COST & GEAR BREAKDOWN: {summary['setup_type'].upper()} ===")

    print("\n🟢 GOOD-ENOUGH TIER (Gig-Ready Budget):")
    for item in summary["good_enough_tier"]:
        print(f" • [{item['category']}] {item['item']} ({item['price']}) - {item['note']}")

    print("\n🔵 HIGHEST SOUND QUALITY TIER (Tour-Grade Pro):")
    for item in summary["pro_tour_grade_tier"]:
        print(f" • [{item['category']}] {item['item']} ({item['price']}) - {item['note']}")

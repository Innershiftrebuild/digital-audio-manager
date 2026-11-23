import json
from typing import Dict, List

class DAMEquipmentRegistry:
    """
    Automated Audio Equipment Registry & Tech Rider Generator for DAM.
    Translates simple artist profiles into professional technical riders.
    """

    EQUIPMENT_DATABASE = {
        "acoustic_solo": {
            "title": "Acoustic Singer-Songwriter",
            "required_inputs": 2,
            "artist_brings": [
                "Acoustic Guitar with active pickup",
                "1/4-inch Instrument Cable (10ft)",
                "Vocal Microphone (Shure SM58 or equivalent)"
            ],
            "recommended_gear": [
                {"item": "LR Baggs Para Acoustic DI Box", "purpose": "Impedance matching & feedback control"},
                {"item": "Korg Pitchblack Custom Tuner", "purpose": "Mute tuning during performance"}
            ],
            "venue_provides": [
                "1x Vocal Mic Stand (Boom arm)",
                "2x XLR Microphone Cables",
                "1x Floor Monitor Wedge"
            ],
            "rider_text": "Artist presents a 2-channel acoustic setup (Vocal + Acoustic Guitar). Acoustic guitar requires a DI box with flat EQ. Monitor mix requires 60% vocal, 40% guitar."
        },
        "singer_with_tracks": {
            "title": "Vocalist with Backing Tracks",
            "required_inputs": 3,
            "artist_brings": [
                "Laptop / iPad with backing tracks",
                "USB Audio Interface (Stereo Out)",
                "Lead Vocal Microphone"
            ],
            "recommended_gear": [
                {"item": "Focusrite Scarlett 2i2 Interface", "purpose": "Clean stereo audio output"},
                {"item": "Radial USB-Pro Stereo DI", "purpose": "Eliminates laptop ground hum/buzz"}
            ],
            "venue_provides": [
                "3x XLR Inputs (1 Mic, 2 Track Line Level L/R)",
                "Stage table/stand for laptop",
                "Full-range PA system with subwoofer support"
            ],
            "rider_text": "Artist presents 3 channels (1 Vocal Mic, 2 Stereo Track L/R). Backing tracks contain bass sub-frequencies; full-range PA and subwoofers are required."
        },
        "dj_electronic": {
            "title": "DJ / Electronic Solo Artist",
            "required_inputs": 2,
            "artist_brings": [
                "DJ Controller / Mixer",
                "Headphones",
                "Dual 1/4-inch to XLR Output Cables"
            ],
            "recommended_gear": [
                {"item": "Radial ProD2 Passive Stereo DI", "purpose": "Protects DJ mixer from phantom power damage"}
            ],
            "venue_provides": [
                "Master Stereo XLR In (L/R) to Main House PA",
                "1x Stereo DJ Booth Monitor Wedge (Independent volume control)",
                "2x Grounded Power Outlets (120V) on stage table"
            ],
            "rider_text": "Artist provides Master Stereo XLR feed. Venue must provide clean, unclipped main PA and a dedicated stage booth monitor with local volume control."
        }
    }

    def generate_tech_rider(self, setup_type: str, artist_name: str) -> Dict:
        """Generates a complete, venue-ready Tech Rider payload."""
        if setup_type not in self.EQUIPMENT_DATABASE:
            raise ValueError(f"Unknown setup type: {setup_type}")

        data = self.EQUIPMENT_DATABASE[setup_type]

        return {
            "artist_name": artist_name,
            "setup_name": data["title"],
            "total_channels": data["required_inputs"],
            "artist_gear_checklist": data["artist_brings"],
            "recommended_upgrades": data["recommended_gear"],
            "venue_requirements": data["venue_provides"],
            "technical_rider_summary": data["rider_text"]
        }

# --- DEMO EXECUTION ---
if __name__ == "__main__":
    registry = DAMEquipmentRegistry()

    # Example: Acoustic Singer-Songwriter creating a rider in 1 click
    rider = registry.generate_tech_rider("acoustic_solo", "Maya & Her Guitar")

    print("=== AUTOMATED TECH RIDER FOR VENUE ===")
    print(f"Artist: {rider['artist_name']}")
    print(f"Setup: {rider['setup_name']} ({rider['total_channels']} Channels)")
    print("\nVenue Requirements:")
    for req in rider['venue_requirements']:
        print(f" - {req}")
    print(f"\nRider Note:\n\"{rider['technical_rider_summary']}\"")

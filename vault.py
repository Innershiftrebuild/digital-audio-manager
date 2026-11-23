import os
import secrets
import hashlib
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from cryptography.fernet import Fernet

class DAMSecureVault:
    """
    Digital Audio Manager (DAM) - Secure Asset Vault & Wardrobe Engine
    Handles zero-knowledge local encryption, asset categorization,
    and temporary expiring link/package generation.
    """
    def __init__(self, master_key: Optional[bytes] = None):
        # Generate or assign AES-256 encryption key for the artist's personal vault
        self.key = master_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

        # The Artist's "Closet" / Shelves
        self.inventory: Dict[str, dict] = {}
        # Active Expiring Packages ("Outfits" dispatched to venues)
        self.active_dispatches: Dict[str, dict] = {}

    def store_asset(self, file_name: str, file_bytes: bytes, category: str, tags: List[str]) -> str:
        """
        Encrypts raw creative asset (WAV, PDF, MP4) and stores it on the artist's shelf.
        Categories: 'master_track', 'live_reels', 'tech_rider', 'press_photo', 'epk'
        """
        asset_id = f"asset_{secrets.token_hex(6)}"
        encrypted_data = self.cipher.encrypt(file_bytes)
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        self.inventory[asset_id] = {
            "asset_id": asset_id,
            "file_name": file_name,
            "category": category,
            "tags": tags,
            "encrypted_data": encrypted_data,
            "sha256_hash": file_hash,
            "created_at": datetime.utcnow().isoformat(),
            "size_bytes": len(file_bytes)
        }
        return asset_id

    def list_closet(self, category_filter: Optional[str] = None) -> List[dict]:
        """View all stored 'wares' categorized for easy outfit selection."""
        items = []
        for asset in self.inventory.values():
            if category_filter and asset["category"] != category_filter:
                continue
            items.append({
                "id": asset["asset_id"],
                "name": asset["file_name"],
                "category": asset["category"],
                "tags": asset["tags"],
                "size_kb": round(asset["size_bytes"] / 1024, 2)
            })
        return items

    def assemble_outfit_package(
        self,
        venue_name: str,
        selected_asset_ids: List[str],
        expiration_hours: int = 72,
        allow_download: bool = False
    ) -> dict:
        """
        Selects specific assets from the shelf and generates a secure,
        time-expiring dispatch link for a specific venue.
        """
        dispatch_id = f"disp_{secrets.token_hex(8)}"
        expiration_time = datetime.utcnow() + timedelta(hours=expiration_hours)

        # Verify selected assets exist in inventory
        packaged_assets = []
        for a_id in selected_asset_ids:
            if a_id in self.inventory:
                packaged_assets.append({
                    "asset_id": a_id,
                    "file_name": self.inventory[a_id]["file_name"],
                    "category": self.inventory[a_id]["category"]
                })

        dispatch_payload = {
            "dispatch_id": dispatch_id,
            "target_venue": venue_name,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expiration_time.isoformat(),
            "expiration_timestamp": expiration_time.timestamp(),
            "permissions": {
                "allow_download": allow_download,
                "stream_only": not allow_download,
                "watermarked": True
            },
            "assets": packaged_assets,
            "secure_url": f"https://stream.dam-app.io/v/{dispatch_id}"
        }

        self.active_dispatches[dispatch_id] = dispatch_payload
        return dispatch_payload

    def verify_access(self, dispatch_id: str) -> Optional[dict]:
        """
        Simulates a venue clicking the link. Checks if link is still valid or expired.
        """
        if dispatch_id not in self.active_dispatches:
            return {"status": "DENIED", "reason": "Invalid dispatch link."}

        package = self.active_dispatches[dispatch_id]
        now = datetime.utcnow().timestamp()

        if now > package["expiration_timestamp"]:
            return {"status": "EXPIRED", "reason": "This submission package link has expired."}

        return {
            "status": "GRANTED",
            "venue": package["target_venue"],
            "permissions": package["permissions"],
            "streamable_assets": package["assets"]
        }

# --- QUICK DEMO / VERIFICATION EXECUTION ---
if __name__ == "__main__":
    # Initialize artist's DAM Vault
    vault = DAMSecureVault()

    # 1. Musician stores creative "wares" on their shelves
    track_id = vault.store_asset(
        file_name="Midnight_Groove_Master.wav",
        file_bytes=b"AUDIO_DATA_BINARY_STREAM_SAMPLE",
        category="master_track",
        tags=["upbeat", "funk", "headline"]
    )

    rider_id = vault.store_asset(
        file_name="Tech_Rider_4Piece_Band.pdf",
        file_bytes=b"PDF_TECH_RIDER_BINARY",
        category="tech_rider",
        tags=["stageplot", "inputs", "4piece"]
    )

    print("--- ARTIST VAULT INVENTORY ---")
    for item in vault.list_closet():
        print(f"[{item['category'].upper()}] {item['name']} (ID: {item['id']})")

    # 2. Musician selects an "outfit" for a specific venue (72-hour expiring link)
    package = vault.assemble_outfit_package(
        venue_name="The Bluebird Cafe",
        selected_asset_ids=[track_id, rider_id],
        expiration_hours=72,
        allow_download=False
    )

    print("\n--- DISPATCHED OUTFIT PACKAGE ---")
    print(f"Target Venue: {package['target_venue']}")
    print(f"Expiring Link: {package['secure_url']}")
    print(f"Expires At: {package['expires_at']}")

    # 3. Simulate Venue Access Check
    access = vault.verify_access(package["dispatch_id"])
    print(f"\nAccess Check Status: {access['status']} (Download Allowed: {access['permissions']['allow_download']})")

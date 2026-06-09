import json
import time
import requests
from pathlib import Path

CLASS_MAP = Path("models/class_to_common.json")
OUTPUT = Path("src/species_photos.json")

# Load class map
with open(CLASS_MAP) as f:
    class_to_common = json.load(f)

# Load existing photos if file exists
if OUTPUT.exists():
    with open(OUTPUT) as f:
        photos = json.load(f)
    print(f"Loaded {len(photos)} existing entries")
else:
    photos = {}
    print("No existing file — starting fresh")

# Find missing or null photo_url
to_fetch = {
    k: v for k, v in class_to_common.items()
    if k not in photos or photos[k].get('photo_url') is None
}
print(f"Missing photos: {len(to_fetch)} — fetching...")

for scientific, common in to_fetch.items():
    name = scientific.replace('_', ' ')
    try:
        r = requests.get(
            "https://api.inaturalist.org/v1/taxa",
            params={"q": name, "rank": "species", "per_page": 1},
            timeout=10
        )
        data = r.json()
        if data['results']:
            taxon = data['results'][0]
            photo_url = None
            if taxon.get('default_photo'):
                photo_url = taxon['default_photo'].get('medium_url') or taxon['default_photo'].get('square_url')
            photos[scientific] = {
                "common": common,
                "scientific": name,
                "photo_url": photo_url,
                "taxon_id": taxon.get('id')
            }
            status = "✓" if photo_url else "✗ no photo"
            print(f"{status} {common}")
        else:
            photos[scientific] = {"common": common, "scientific": name, "photo_url": None}
            print(f"✗ {common} — not found")
    except Exception as e:
        photos[scientific] = {"common": common, "scientific": name, "photo_url": None}
        print(f"✗ {common} — {e}")
    time.sleep(0.3)

# Save updated file
with open(OUTPUT, 'w') as f:
    json.dump(photos, f, indent=2)

missing = sum(1 for v in photos.values() if not v.get('photo_url'))
print(f"\nSaved {len(photos)} species — missing photos: {missing}")
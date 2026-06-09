import requests
from pyinaturalist import get_observations
from pathlib import Path

samples = {
    "rainbow_trout": "Oncorhynchus mykiss",
    "largemouth_bass": "Micropterus nigricans",
    "bluegill": "Lepomis macrochirus",
    "chinook_salmon": "Oncorhynchus tshawytscha",
    "pacific_mackerel": "Scomber japonicus"
}

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"
SAMPLES_DIR.mkdir(exist_ok=True)

# Clear old samples
for f in SAMPLES_DIR.iterdir():
    if f.is_file():
        f.unlink()
print("Cleared old samples")

for filename, species in samples.items():
    obs = get_observations(taxon_name=species, quality_grade="research", photos=True, per_page=1)
    if obs['results'] and obs['results'][0].get('photos'):
        url = obs['results'][0]['photos'][0]['url'].replace('square', 'medium')
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(SAMPLES_DIR / f"{filename}.jpg", 'wb') as f:
                f.write(r.content)
            print(f"✓ {filename}")
    else:
        print(f"✗ {filename} — no observations found")

print(f"\nDone — {len(list(SAMPLES_DIR.glob('*.jpg')))} samples in {SAMPLES_DIR}")
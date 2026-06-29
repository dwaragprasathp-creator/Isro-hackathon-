from pathlib import Path
from logger import log

ROOT = Path(__file__).resolve().parent.parent

folders = [
    "data/raw/landsat",
    "data/raw/sentinel",
    "data/raw/population",
    "data/raw/boundary",
    "data/raw/osm",
    "data/processed",
    "outputs",
    "models"
]

log("Checking Project Structure...")

for folder in folders:
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    log(f"OK : {path}")

log("Project Structure Ready")
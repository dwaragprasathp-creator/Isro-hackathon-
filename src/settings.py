from pathlib import Path

# -----------------------------
# Project Information
# -----------------------------
PROJECT_NAME = "Urban Heat Stress Detection"

CITY = "Hyderabad"

# -----------------------------
# Folder Paths
# -----------------------------
ROOT = Path(__file__).resolve().parent.parent

DATA = ROOT / "data"

RAW = DATA / "raw"

PROCESSED = DATA / "processed"

OUTPUTS = ROOT / "outputs"

MODELS = ROOT / "models"

# -----------------------------
# Satellite Data
# -----------------------------
LANDSAT = RAW / "landsat"

BOUNDARY = RAW / "boundary"

POPULATION = RAW / "population"

OSM = RAW / "osm"

SENTINEL = RAW / "sentinel"

print("Settings Loaded Successfully")
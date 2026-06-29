from pathlib import Path

# -------------------------
# Project Directories
# -------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

# Create folders if missing
RAW_DATA.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("Urban Heat Stress Detection Project")
print("=" * 50)

print("Project Root :", PROJECT_ROOT)
print("Raw Data     :", RAW_DATA)
print("Processed    :", PROCESSED_DATA)

print("\nFolder check completed successfully.")
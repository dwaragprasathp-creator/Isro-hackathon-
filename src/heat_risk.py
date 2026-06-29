from pathlib import Path
import rasterio
import numpy as np

processed = Path("data/processed")

# Load LST
with rasterio.open(processed / "lst.tif") as src:
    lst = src.read(1)
    profile = src.profile

# Create risk map
risk = np.zeros(lst.shape, dtype=np.uint8)

# Ignore invalid pixels
valid = np.isfinite(lst)

risk[(lst >= 25) & (lst < 35) & valid] = 1      # Low
risk[(lst >= 35) & (lst < 40) & valid] = 2      # Moderate
risk[(lst >= 40) & (lst < 45) & valid] = 3      # High
risk[(lst >= 45) & valid] = 4                   # Extreme

profile.update(
    dtype=rasterio.uint8,
    count=1,
    compress="lzw"
)

outfile = processed / "heat_risk.tif"

with rasterio.open(outfile, "w", **profile) as dst:
    dst.write(risk, 1)

# Print statistics
unique, counts = np.unique(risk[valid], return_counts=True)

print("=" * 60)
print("HEAT RISK MAP GENERATED")
print("=" * 60)

labels = {
    1: "Low",
    2: "Moderate",
    3: "High",
    4: "Extreme"
}

for value, count in zip(unique, counts):
    if value in labels:
        print(f"{labels[value]:10}: {count} pixels")

print(f"\nSaved: {outfile}")
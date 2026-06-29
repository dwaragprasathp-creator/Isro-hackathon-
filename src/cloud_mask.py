from pathlib import Path
import rasterio
import numpy as np

processed = Path("data/processed")

qa_path = processed / "qa.tif"

with rasterio.open(qa_path) as src:
    qa = src.read(1)
    profile = src.profile

# Landsat Collection 2 QA_PIXEL bits
CLOUD = 1 << 3
CLOUD_SHADOW = 1 << 4
SNOW = 1 << 5

mask = (
    ((qa & CLOUD) == 0)
    & ((qa & CLOUD_SHADOW) == 0)
    & ((qa & SNOW) == 0)
)

profile.update(dtype=rasterio.uint8)

output = processed / "cloud_mask.tif"

with rasterio.open(output, "w", **profile) as dst:
    dst.write(mask.astype("uint8"), 1)

print("=" * 60)
print("Cloud Mask Created Successfully")
print("=" * 60)
print("Output:", output)
print("Clear Pixels:", np.sum(mask))
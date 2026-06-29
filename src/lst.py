from pathlib import Path
import rasterio
import numpy as np

processed = Path("data/processed")

# Read Thermal Band
with rasterio.open(processed / "thermal.tif") as src:
    thermal = src.read(1).astype(np.float32)
    profile = src.profile

# Read Cloud Mask
with rasterio.open(processed / "cloud_mask.tif") as src:
    cloud = src.read(1).astype(bool)

# NoData → NaN
thermal = np.where(thermal == 0, np.nan, thermal)

# Apply Cloud Mask
thermal = np.where(cloud, thermal, np.nan)

# Landsat Collection 2 Surface Temperature Scale Factor
# ST = DN × 0.00341802 + 149.0 (Kelvin)
lst_kelvin = thermal * 0.00341802 + 149.0

# Kelvin → Celsius
lst_celsius = lst_kelvin - 273.15

# Remove unrealistic temperatures
lst_celsius[(lst_celsius < -20) | (lst_celsius > 80)] = np.nan

profile.update(
    dtype=rasterio.float32,
    count=1,
    compress="lzw"
)

outfile = processed / "lst.tif"

with rasterio.open(outfile, "w", **profile) as dst:
    dst.write(lst_celsius.astype(rasterio.float32), 1)

print("=" * 60)
print("LAND SURFACE TEMPERATURE GENERATED")
print("=" * 60)
print(f"Minimum : {np.nanmin(lst_celsius):.2f} °C")
print(f"Maximum : {np.nanmax(lst_celsius):.2f} °C")
print(f"Mean    : {np.nanmean(lst_celsius):.2f} °C")
print(f"Saved   : {outfile}")
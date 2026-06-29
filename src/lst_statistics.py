import rasterio
import numpy as np

with rasterio.open("data/processed/lst.tif") as src:
    lst = src.read(1)

print("=" * 40)
print("LST Statistics")
print("=" * 40)

print("Minimum :", round(np.nanmin(lst), 2), "°C")
print("Maximum :", round(np.nanmax(lst), 2), "°C")
print("Mean    :", round(np.nanmean(lst), 2), "°C")
print("Std Dev :", round(np.nanstd(lst), 2), "°C")
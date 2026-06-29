import rasterio
import matplotlib.pyplot as plt

with rasterio.open("data/processed/uhi.tif") as src:
    uhi = src.read(1)

plt.figure(figsize=(10,8))
plt.imshow(uhi, cmap="jet")
plt.colorbar(label="UHI Intensity (°C)")
plt.title("Urban Heat Island - Hyderabad")
plt.axis("off")
plt.show()
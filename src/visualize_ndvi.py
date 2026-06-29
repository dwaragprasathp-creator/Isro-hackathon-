import rasterio
import matplotlib.pyplot as plt

with rasterio.open("data/processed/ndvi.tif") as src:
    ndvi = src.read(1)

plt.figure(figsize=(8,8))
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar(label="NDVI")
plt.title("Hyderabad NDVI")
plt.axis("off")
plt.show()
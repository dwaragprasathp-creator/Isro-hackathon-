import rasterio
import matplotlib.pyplot as plt

with rasterio.open("data/processed/heat_risk.tif") as src:
    risk = src.read(1)

plt.figure(figsize=(8, 8))
plt.imshow(risk, cmap="RdYlGn_r")
plt.title("Heat Risk Map - Hyderabad")
plt.colorbar(label="Risk Level")
plt.axis("off")
plt.show()
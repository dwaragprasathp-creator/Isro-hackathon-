import rasterio
import matplotlib.pyplot as plt

with rasterio.open("data/processed/lst.tif") as src:
    lst = src.read(1)

plt.figure(figsize=(8,8))
plt.imshow(lst, cmap="hot")
plt.colorbar(label="Temperature (°C)")
plt.title("Hyderabad Land Surface Temperature")
plt.axis("off")
plt.show()
from pathlib import Path
import rasterio

LANDSAT = Path("data/raw/landsat")

scene = None

for folder in LANDSAT.iterdir():
    if folder.is_dir():
        scene = folder
        break

if scene is None:
    raise Exception("No Landsat Scene Found!")

print("=" * 60)
print("LANDSAT SCENE")
print("=" * 60)
print(scene)

bands = {}

for tif in scene.glob("*.TIF"):
    name = tif.stem

    if "SR_B2" in name:
        bands["Blue"] = tif

    elif "SR_B3" in name:
        bands["Green"] = tif

    elif "SR_B4" in name:
        bands["Red"] = tif

    elif "SR_B5" in name:
        bands["NIR"] = tif

    elif "SR_B6" in name:
        bands["SWIR1"] = tif

    elif "SR_B7" in name:
        bands["SWIR2"] = tif

    elif "ST_B10" in name:
        bands["Thermal"] = tif

print("\nDetected Bands\n")

for k, v in bands.items():
    print(k, ":", v.name)

print("\nOpening Red Band...")

with rasterio.open(bands["Red"]) as src:

    print("\nRaster Information")
    print("------------------")

    print("Width :", src.width)
    print("Height:", src.height)
    print("CRS   :", src.crs)
    print("Resolution :", src.res)
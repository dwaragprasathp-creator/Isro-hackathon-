import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import FancyArrowPatch

# ==========================================================
# AI Urban Heat Island Decision Support System
# ISRO Hackathon 2026
# ==========================================================

INPUT = Path("data/processed")
OUTPUT = Path("outputs/maps")

OUTPUT.mkdir(
    parents=True,
    exist_ok=True
)

maps = {

    "ndvi.tif":{

        "title":"Normalized Difference Vegetation Index",

        "cmap":"YlGn",

        "unit":"NDVI"

    },

    "ndwi.tif":{

        "title":"Normalized Difference Water Index",

        "cmap":"Blues",

        "unit":"NDWI"

    },

    "ndbi.tif":{

        "title":"Normalized Difference Built-up Index",

        "cmap":"cividis",

        "unit":"NDBI"

    },

    "lst.tif":{

        "title":"Land Surface Temperature",

        "cmap":"turbo",

        "unit":"°C"

    },

    "heat_risk.tif":{

        "title":"Urban Heat Risk Map",

        "cmap":"Reds",

        "unit":"Risk"

    }

}

print("="*60)
print("EXPORTING PRESENTATION MAPS")
print("="*60)# ==========================================================
# EXPORT EACH MAP
# ==========================================================

for filename, info in maps.items():

    raster_path = INPUT / filename

    if not raster_path.exists():

        print(f"❌ Missing : {filename}")

        continue

    print(f"Processing : {filename}")

    with rasterio.open(raster_path) as src:

        image = src.read(1)

        bounds = src.bounds

        transform = src.transform

    image = np.where(np.isfinite(image), image, np.nan)

    minimum = np.nanmin(image)

    maximum = np.nanmax(image)

    mean = np.nanmean(image)

    fig = plt.figure(

        figsize=(12,10),

        facecolor="white"

    )

    ax = fig.add_subplot(111)

    im = ax.imshow(

        image,

        cmap=info["cmap"]

    )

    ax.set_xticks([])

    ax.set_yticks([])

    ax.set_title(

        info["title"],

        fontsize=18,

        weight="bold",

        pad=20

    )

    # ------------------------------------------
    # North Arrow
    # ------------------------------------------

    arrow = FancyArrowPatch(

        (0.93,0.12),

        (0.93,0.23),

        mutation_scale=25,

        color="black",

        transform=ax.transAxes

    )

    ax.add_patch(arrow)

    ax.text(

        0.93,

        0.25,

        "N",

        transform=ax.transAxes,

        ha="center",

        fontsize=14,

        fontweight="bold"

    )

    # ------------------------------------------
    # Color Bar
    # ------------------------------------------

    cbar = plt.colorbar(

        im,

        ax=ax,

        shrink=0.75,

        pad=0.02

    )

    cbar.set_label(

        info["unit"],

        fontsize=12

    )

    # ------------------------------------------
    # Statistics
    # ------------------------------------------

    stats = (

        f"Minimum : {minimum:.2f}\n"

        f"Mean     : {mean:.2f}\n"

        f"Maximum : {maximum:.2f}"

    )

    ax.text(

        1.04,

        0.60,

        stats,

        transform=ax.transAxes,

        fontsize=11,

        bbox=dict(

            facecolor="white",

            edgecolor="black",

            alpha=0.9

        )

    )    # ------------------------------------------
    # Scale Bar (Approximate)
    # ------------------------------------------

    ax.plot(

        [0.05, 0.20],

        [0.05, 0.05],

        transform=ax.transAxes,

        color="black",

        linewidth=4

    )

    ax.text(

        0.125,

        0.02,

        "Approx. Scale",

        transform=ax.transAxes,

        ha="center",

        fontsize=10

    )

    # ------------------------------------------
    # Footer
    # ------------------------------------------

    plt.figtext(

        0.5,

        0.02,

        "AI Urban Heat Island Decision Support System | ISRO Hackathon 2026\nGenerated using Landsat, SRTM DEM, ERA5 and Physics-Informed Machine Learning",

        ha="center",

        fontsize=11,

        color="gray"

    )

    # ------------------------------------------
    # Layout
    # ------------------------------------------

    plt.tight_layout()

    outfile = OUTPUT / f"{raster_path.stem}_Final.png"

    plt.savefig(

        outfile,

        dpi=600,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close(fig)

    print(f"✓ Saved : {outfile}")

print("\n" + "=" * 60)
print("ALL MAPS EXPORTED SUCCESSFULLY")
print("=" * 60)

print("\nOutput Folder:")
print(OUTPUT)

print("\nGenerated Maps:")

for file in OUTPUT.glob("*_Final.png"):

    print("✓", file.name)
import ee
import geemap
from pathlib import Path

ee.Initialize(project="heatstressai")

# Hyderabad ROI
roi = ee.Geometry.Rectangle([78.30, 17.30, 78.60, 17.55])

# WorldPop Population
population = (
    ee.ImageCollection("WorldPop/GP/100m/pop")
    .filterDate("2020-01-01", "2020-12-31")
    .first()
    .clip(roi)
)

output = Path("data/raw/worldpop")
output.mkdir(parents=True, exist_ok=True)

outfile = output / "population.tif"

geemap.ee_export_image(
    population,
    filename=str(outfile),
    scale=100,
    region=roi
)

print("=" * 60)
print("WORLDPOP DOWNLOADED")
print("=" * 60)
print(outfile)
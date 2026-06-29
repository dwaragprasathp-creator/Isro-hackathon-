import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path

print("=" * 60)
print("ERA5 METEOROLOGICAL PROCESSOR")
print("=" * 60)

# --------------------------------------------------
# Load ERA5 Dataset
# --------------------------------------------------
ds = xr.open_dataset("data/raw/era5/era5_hyderabad.nc")

# --------------------------------------------------
# Convert Kelvin -> Celsius
# --------------------------------------------------
t2m = ds["t2m"] - 273.15
d2m = ds["d2m"] - 273.15

# --------------------------------------------------
# Wind Components
# --------------------------------------------------
u10 = ds["u10"]
v10 = ds["v10"]

# Wind Speed (m/s)
wind_speed = np.sqrt(u10**2 + v10**2)

# --------------------------------------------------
# Relative Humidity
# --------------------------------------------------
es = 6.112 * np.exp((17.67 * t2m) / (t2m + 243.5))
e = 6.112 * np.exp((17.67 * d2m) / (d2m + 243.5))

relative_humidity = (e / es) * 100

# --------------------------------------------------
# Average Over Time
# --------------------------------------------------
air_temp = t2m.mean(dim="valid_time")
humidity = relative_humidity.mean(dim="valid_time")
wind = wind_speed.mean(dim="valid_time")

# --------------------------------------------------
# Convert to DataFrame
# --------------------------------------------------
rows = []

for lat in air_temp.latitude.values:
    for lon in air_temp.longitude.values:

        rows.append({

            "latitude": float(lat),

            "longitude": float(lon),

            "air_temperature": float(
                air_temp.sel(latitude=lat, longitude=lon)
            ),

            "humidity": float(
                humidity.sel(latitude=lat, longitude=lon)
            ),

            "wind_speed": float(
                wind.sel(latitude=lat, longitude=lon)
            )

        })

df = pd.DataFrame(rows)

# --------------------------------------------------
# Save
# --------------------------------------------------
output = Path("data/processed")
output.mkdir(exist_ok=True)

outfile = output / "era5_processed.csv"

df.to_csv(outfile, index=False)

print()
print(df)

print()
print("=" * 60)
print("ERA5 PROCESSING COMPLETED")
print("=" * 60)

print("Saved :", outfile)
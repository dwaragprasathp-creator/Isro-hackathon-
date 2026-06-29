import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path

era5 = xr.open_dataset("data/raw/era5/era5_hyderabad.nc")

# Average over 24 hours
t2m = era5["t2m"].mean(dim="valid_time") - 273.15
d2m = era5["d2m"].mean(dim="valid_time") - 273.15
u10 = era5["u10"].mean(dim="valid_time")
v10 = era5["v10"].mean(dim="valid_time")

# Wind Speed
wind = np.sqrt(u10**2 + v10**2)

# Relative Humidity
humidity = 100 * np.exp(
    (17.625 * d2m) / (243.04 + d2m)
    - (17.625 * t2m) / (243.04 + t2m)
)

df = pd.DataFrame({
    "latitude": t2m.latitude.values.repeat(len(t2m.longitude)),
    "longitude": np.tile(t2m.longitude.values, len(t2m.latitude)),
    "air_temperature": t2m.values.flatten(),
    "dew_point": d2m.values.flatten(),
    "wind_speed": wind.values.flatten(),
    "humidity": humidity.values.flatten()
})

output = Path("data/processed")
output.mkdir(exist_ok=True)

outfile = output / "era5_features.csv"

df.to_csv(outfile, index=False)

print("="*60)
print("ERA5 FEATURES CREATED")
print("="*60)
print(df.head())
print()
print("Saved:", outfile)
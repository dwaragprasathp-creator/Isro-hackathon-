import xarray as xr

print("="*60)
print("ERA5 DATASET INFORMATION")
print("="*60)

ds = xr.open_dataset("data/raw/era5/era5_hyderabad.nc")

print(ds)

print("\nVariables")
print("-"*40)

for var in ds.data_vars:
    print(var)

print("\nCoordinates")
print("-"*40)

print(ds.coords)

print("\nDimensions")
print("-"*40)

print(ds.dims)
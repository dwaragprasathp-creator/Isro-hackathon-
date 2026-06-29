import pandas as pd

print("=" * 60)
print("MERGING ERA5 METEOROLOGICAL FEATURES")
print("=" * 60)

# Load datasets
feature_stack = pd.read_csv("data/processed/feature_stack.csv")
era5 = pd.read_csv("data/processed/era5_features.csv")

# Display ERA5 values
print("\nERA5 Statistics")
print(era5.describe())

# Add average meteorological values
feature_stack["air_temperature"] = era5["air_temperature"].mean()
feature_stack["humidity"] = era5["humidity"].mean()
feature_stack["wind_speed"] = era5["wind_speed"].mean()

outfile = "data/processed/feature_stack_ai.csv"

feature_stack.to_csv(outfile, index=False)

print("\nMerged Successfully")
print("Rows :", len(feature_stack))
print("Columns :", feature_stack.columns.tolist())
print("Saved :", outfile)
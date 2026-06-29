import pandas as pd
from scipy.ndimage import uniform_filter

print("="*60)
print("FEATURE ENGINEERING")
print("="*60)

df = pd.read_csv("data/processed/feature_stack_ai.csv")

# -------------------------------------------------
# Convert to square grid
# -------------------------------------------------
height = 995
width = 1350

# Ensure correct number of pixels
expected = height * width

df = df.iloc[:expected].copy()

# -------------------------------------------------
# Helper
# -------------------------------------------------
def local_mean(column):

    image = df[column].values.reshape(height, width)

    return uniform_filter(
        image,
        size=5,
        mode="nearest"
    ).flatten()

# -------------------------------------------------
# New Features
# -------------------------------------------------

print("Computing Local NDVI...")
df["local_ndvi"] = local_mean("ndvi")

print("Computing Local NDBI...")
df["local_ndbi"] = local_mean("ndbi")

print("Computing Local LST...")
df["local_lst"] = local_mean("lst")

print("Computing Thermal Anomaly...")
df["thermal_anomaly"] = (
    df["lst"] -
    df["local_lst"]
)

# -------------------------------------------------
# Save
# -------------------------------------------------

df.to_csv(
    "data/processed/feature_stack_ai.csv",
    index=False
)

print()
print("Feature Engineering Completed")
print(df.head())
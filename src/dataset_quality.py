import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("DATA QUALITY CHECK")
print("="*60)

df = pd.read_csv("data/processed/feature_stack_ai.csv")

print("\nDataset Shape")
print(df.shape)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nLST Statistics")
print(df["lst"].describe())

plt.figure(figsize=(8,5))
plt.hist(df["lst"], bins=60)
plt.xlabel("Land Surface Temperature")
plt.ylabel("Pixel Count")
plt.title("Distribution of LST")

plt.tight_layout()
plt.savefig("data/processed/lst_distribution.png", dpi=300)

print("\nHistogram Saved")
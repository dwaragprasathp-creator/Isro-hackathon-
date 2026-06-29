import pandas as pd
import matplotlib.pyplot as plt

print("="*60)
print("DATASET ANALYSIS")
print("="*60)

df = pd.read_csv("data/processed/feature_stack_ai.csv")

print(df.describe())

print("\nCorrelation Matrix\n")

corr = df.corr(numeric_only=True)

print(corr)

plt.figure(figsize=(8,6))
plt.imshow(corr, cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.tight_layout()

plt.savefig("data/processed/correlation_matrix.png", dpi=300)

print("\nCorrelation matrix saved.")
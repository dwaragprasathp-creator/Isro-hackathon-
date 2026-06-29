import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 60)
print("EXPLAINABLE AI (SHAP)")
print("=" * 60)

# Load Dataset
df = pd.read_csv("data/processed/feature_stack_ai.csv")

# Representative sample
df = df.sample(1000, random_state=42)

X = df[
    [
        "ndvi",
        "ndwi",
        "ndbi",
        "elevation",
        "air_temperature",
        "humidity",
        "wind_speed"
    ]
]

print("Loading model...")
model = joblib.load("models/physics_model.pkl")

print("Creating SHAP Explainer...")
explainer = shap.TreeExplainer(model)

print("Computing SHAP Values...")
shap_values = explainer.shap_values(X)

output = Path("data/processed")
output.mkdir(exist_ok=True)

plt.figure(figsize=(10,6))
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()

plt.savefig(
    output/"shap_summary.png",
    dpi=300
)

print()
print("SHAP completed successfully.")
print("Saved:", output/"shap_summary.png")
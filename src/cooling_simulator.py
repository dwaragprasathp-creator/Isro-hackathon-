import pandas as pd
import joblib
from pathlib import Path

print("=" * 60)
print("AI COOLING SCENARIO SIMULATOR")
print("=" * 60)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/processed/feature_stack_ai.csv")
model = joblib.load("models/physics_model.pkl")

# -----------------------------
# Match Training Features
# -----------------------------
features = model.feature_names_in_.tolist()

print("\nFeatures Used by Model:")
print(features)

# Baseline Prediction
baseline = model.predict(df[features]).mean()

# -----------------------------
# Cooling Scenarios
# -----------------------------
scenarios = {

    "Neem Plantation": {
        "category": "Traditional",
        "ndvi": 0.25,
        "cost": 250000,
        "feasibility": "High"
    },

    "Sacred Grove": {
        "category": "Traditional",
        "ndvi": 0.35,
        "cost": 900000,
        "feasibility": "Medium"
    },

    "Urban Waterbody Restoration": {
        "category": "Traditional",
        "ndwi": 0.30,
        "cost": 1800000,
        "feasibility": "Medium"
    },

    "Pond Restoration": {
        "category": "Traditional",
        "ndwi": 0.25,
        "cost": 1200000,
        "feasibility": "High"
    },

    "Lime Plaster": {
        "category": "Traditional",
        "ndbi": -0.10,
        "cost": 650000,
        "feasibility": "Very High"
    },

    "White Lime Roof": {
        "category": "Traditional",
        "ndbi": -0.15,
        "cost": 800000,
        "feasibility": "High"
    },

    "Clay Tile Roof": {
        "category": "Traditional",
        "ndbi": -0.12,
        "cost": 850000,
        "feasibility": "High"
    },

    "Courtyard Houses": {
        "category": "Traditional",
        "ndbi": -0.08,
        "cost": 3000000,
        "feasibility": "Low"
    },

    "Green Roof": {
        "category": "Modern",
        "ndvi": 0.20,
        "cost": 2500000,
        "feasibility": "Medium"
    },

    "Cool Roof": {
        "category": "Modern",
        "ndbi": -0.20,
        "cost": 1200000,
        "feasibility": "High"
    },

    "Vertical Garden": {
        "category": "Modern",
        "ndvi": 0.15,
        "cost": 2200000,
        "feasibility": "Medium"
    },

    "Urban Forest": {
        "category": "Modern",
        "ndvi": 0.30,
        "cost": 4500000,
        "feasibility": "Medium"
    }
}
# -----------------------------
# Literature-based Cooling Range (Planning Estimates)
# -----------------------------
cooling_reference = {

    "Urban Forest": 3.5,
    "Green Roof": 2.0,
    "Cool Roof": 1.8,
    "Vertical Garden": 1.5,

    "Urban Waterbody Restoration": 2.8,
    "Pond Restoration": 2.3,

    "Neem Plantation": 2.0,
    "Sacred Grove": 3.0,

    "Lime Plaster": 1.2,
    "White Lime Roof": 1.5,
    "Clay Tile Roof": 1.3,
    "Courtyard Houses": 1.0
}
feasibility_score = {

    "Very High":5,

    "High":4,

    "Medium":3,

    "Low":2

}

results = []

for name, info in scenarios.items():

    sim = df.copy()

    # -----------------------------
    # Vegetation Improvement
    # -----------------------------
    if "ndvi" in info:

        gain = info["ndvi"] * (1 - sim["ndvi"])

        sim["ndvi"] = (
            sim["ndvi"] + gain
        ).clip(-1, 1)

    # -----------------------------
    # Water Improvement
    # -----------------------------
    if "ndwi" in info:

        gain = info["ndwi"] * (1 - sim["ndwi"])

        sim["ndwi"] = (
            sim["ndwi"] + gain
        ).clip(-1, 1)

    # -----------------------------
    # Built-up Reduction
    # -----------------------------
    if "ndbi" in info:

        reduction = abs(info["ndbi"])

        sim["ndbi"] = (
            sim["ndbi"] * (1 - reduction)
        ).clip(-1, 1)

    # -----------------------------
    # AI Prediction
    # -----------------------------
    pred = model.predict(
        sim[features]
    ).mean()

    ai_cooling = max(0, baseline - pred)

    reference = cooling_reference[name]

    cooling = round((0.6 * reference) + (0.4 * ai_cooling), 2)

    # -----------------------------
    # Overall Score
    # -----------------------------
    # -----------------------------
    # Urban Suitability Bonus
    # -----------------------------
    urban_bonus = 10 if info["category"] == "Modern" else 0

    overall = (

        cooling * 50

        +

        feasibility_score[
            info["feasibility"]
        ] * 10

        +

        urban_bonus

         -

        info["cost"] / 1000000

    )

    # -----------------------------
    # Save Results
    # -----------------------------
    results.append({

        "Technique": name,

        "Category": info["category"],

        "Average Temperature (°C)": round(pred, 2),

        "Estimated Cooling (°C)": round(cooling, 2),

        "Estimated Cost (₹)": info["cost"],

        "Feasibility": info["feasibility"],

        "Overall Score": round(overall, 2)

    })
    # -----------------------------
# Convert Results to DataFrame
# -----------------------------
result = pd.DataFrame(results)
result = result.sort_values(
    by="Overall Score",
    ascending=False
    )

output = Path("data/processed")
output.mkdir(exist_ok=True)

result.to_csv(
    output / "cooling_scenarios.csv",
    index=False
)

print("=" * 60)
print("Simulation Finished")
print("=" * 60)

print(result.head())


outfile = output / "cooling_scenarios.csv"

print("Saving to:", outfile)

result.to_csv(outfile, index=False)

print("File saved successfully!")
import pandas as pd

print("=" * 60)
print("AI RECOMMENDATION ENGINE")
print("=" * 60)

df = pd.read_csv("data/processed/feature_stack.csv")

results = []

for idx, row in df.iterrows():

    recommendations = []

    reasons = []

    total_cooling = 0

    total_cost = 0

    priority_score = 0

    # -----------------------------
    # Vegetation
    # -----------------------------
    if row["ndvi"] < 0.20:

        recommendations.append("Neem Plantation")
        recommendations.append("Sacred Grove")

        reasons.append(
            "Very low vegetation detected."
        )

        total_cooling += 4.5

        total_cost += 250000

        priority_score += 3

    elif row["ndvi"] < 0.35:

        recommendations.append("Urban Forest")

        reasons.append(
            "Moderate vegetation deficit."
        )

        total_cooling += 3

        total_cost += 450000

        priority_score += 2

    # -----------------------------
    # Water
    # -----------------------------
    if row["ndwi"] < 0:

        recommendations.append(
            "Temple Tank Restoration"
        )

        recommendations.append(
            "Village Pond Restoration"
        )

        reasons.append(
            "Water availability is low."
        )

        total_cooling += 2.5

        total_cost += 1200000

        priority_score += 2

    # -----------------------------
    # Built-up
    # -----------------------------
    if row["ndbi"] > 0.25:

        recommendations.append("White Lime Roof")
        recommendations.append("Cool Roof")
        recommendations.append("Clay Tile Roof")

        reasons.append(
            "Dense built-up area detected."
        )

        total_cooling += 4

        total_cost += 800000

        priority_score += 3

    elif row["ndbi"] > 0.10:

        recommendations.append("Green Roof")

        reasons.append(
            "Moderate built-up density."
        )

        total_cooling += 2

        total_cost += 2500000

        priority_score += 1

    # -----------------------------
    # Elevation
    # -----------------------------
    if row["elevation"] > 600:

        recommendations.append("Wind Corridor")

        reasons.append(
            "High elevation favours ventilation."
        )

        total_cooling += 1

        priority_score += 1

    # -----------------------------
    # Priority
    # -----------------------------
    if priority_score >= 7:

        priority = "Very High"

    elif priority_score >= 5:

        priority = "High"

    elif priority_score >= 3:

        priority = "Medium"

    else:

        priority = "Low"

    # -----------------------------
    # Confidence
    # -----------------------------
    confidence = min(
        95,
        60 + priority_score * 5
    )

    results.append({

        "NDVI": row["ndvi"],

        "NDWI": row["ndwi"],

        "NDBI": row["ndbi"],

        "LST": row["lst"],

        "Recommendations":
            ", ".join(sorted(set(recommendations))),

        "Reason":
            " | ".join(reasons),

        "Expected Cooling (°C)":
            round(total_cooling,2),

        "Estimated Cost (₹)":
            total_cost,

        "Priority":
            priority,

        "Confidence (%)":
            confidence

    })

result = pd.DataFrame(results)

result.to_csv(
    "data/processed/final_recommendations.csv",
    index=False
)

print(result.head())

print()

print("Final Recommendation File Created Successfully")
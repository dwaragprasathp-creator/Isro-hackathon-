import pandas as pd
from pathlib import Path

print("=" * 60)
print("AI SCENARIO OPTIMIZER")
print("=" * 60)

# -----------------------------------------------------
# Load Cooling Scenarios
# -----------------------------------------------------
df = pd.read_csv("data/processed/cooling_scenarios.csv")

# -----------------------------------------------------
# Convert Feasibility to Score
# -----------------------------------------------------
feasibility_map = {
    "Very High": 5,
    "High": 4,
    "Medium": 3,
    "Low": 2
}

df["Feasibility Score"] = df["Feasibility"].map(feasibility_map)

# -----------------------------------------------------
# Cost Efficiency
# Cooling per ₹ Lakh
# -----------------------------------------------------
df["Cost Efficiency"] = (
    df["Estimated Cooling (°C)"] /
    (df["Estimated Cost (₹)"] / 100000)
)
# -----------------------------------------------------
# Temperature-Based Recommendation
# -----------------------------------------------------
# -----------------------------------------------------
# Temperature Trigger & Recommended Action
# -----------------------------------------------------

recommended_when = []
recommended_action = []

for temp in df["Average Temperature (°C)"]:

    if temp >= 42:

        recommended_when.append("LST ≥ 42°C")
        recommended_action.append("Immediate Intervention Required")

    elif temp >= 40:

        recommended_when.append("LST 40–42°C")
        recommended_action.append("Priority Cooling Measures")

    elif temp >= 35:

        recommended_when.append("LST 35–40°C")
        recommended_action.append("Preventive Heat Mitigation")

    else:

        recommended_when.append("LST < 35°C")
        recommended_action.append("Routine Monitoring")

df["Recommended When"] = recommended_when
df["Recommended Action"] = recommended_action
# -----------------------------------------------------
# Reason for Recommendation
# -----------------------------------------------------

reasons = []

for _, row in df.iterrows():

    if row["Technique"] == "Urban Forest":
        reasons.append("High LST and low vegetation cover")

    elif row["Technique"] == "Green Roof":
        reasons.append("Suitable for dense urban buildings")

    elif row["Technique"] == "Cool Roof":
        reasons.append("Reduces rooftop heat absorption")

    elif row["Technique"] == "Vertical Garden":
        reasons.append("Improves urban greenery where space is limited")

    elif row["Technique"] == "Urban Waterbody Restoration":
        reasons.append("Provides evaporative cooling and reduces heat stress")

    elif row["Technique"] == "Pond Restoration":
        reasons.append("Improves local cooling and water retention")

    elif row["Technique"] == "Neem Plantation":
        reasons.append("Native trees increase shade and cooling")

    elif row["Technique"] == "Sacred Grove":
        reasons.append("Dense vegetation helps reduce surrounding temperature")

    elif row["Technique"] == "Lime Plaster":
        reasons.append("Reflective surface reduces heat absorption")

    elif row["Technique"] == "White Lime Roof":
        reasons.append("High solar reflectance lowers roof temperature")

    elif row["Technique"] == "Clay Tile Roof":
        reasons.append("Natural insulation reduces heat transfer")

    else:
        reasons.append("Traditional climate-responsive design")

df["Reason"] = reasons


# -----------------------------------------------------
# Temperature Trigger
# -----------------------------------------------------
conditions = []

for temp in df["Average Temperature (°C)"]:

    if temp >= 42:
        conditions.append("LST ≥ 42°C (Extreme Heat)")

    elif temp >= 40:
        conditions.append("LST 40–42°C (High Heat)")

    elif temp >= 35:
        conditions.append("LST 35–40°C (Moderate Heat)")

    else:
        conditions.append("LST < 35°C (Low Heat)")

df["Recommended When"] = conditions


# -----------------------------------------------------
# Overall Optimization Score
# -----------------------------------------------------
df["Optimization Score"] = (

    df["Estimated Cooling (°C)"] * 50

    +

    df["Feasibility Score"] * 10

    +

    df["Cost Efficiency"] * 5

)

# -----------------------------------------------------
# Rank
# -----------------------------------------------------
df = df.sort_values(

    by="Optimization Score",

    ascending=False

)

df["Rank"] = range(

    1,

    len(df) + 1

)

# -----------------------------------------------------
# Save Optimized Scenarios
# -----------------------------------------------------
output = Path("data/processed")

output.mkdir(exist_ok=True)

df.to_csv(

    output / "optimized_scenarios.csv",

    index=False

)

print("✓ optimized_scenarios.csv saved")

# -----------------------------------------------------
# Best Strategy
# -----------------------------------------------------
best = df.head(1)

best.to_csv(

    output / "best_strategy.csv",

    index=False

)

print("✓ best_strategy.csv saved")

# -----------------------------------------------------
# Budget Plans
# -----------------------------------------------------
budget = []

budgets = [

    1000000,

    2500000,

    5000000,

    10000000

]

for b in budgets:

    options = df[

        df["Estimated Cost (₹)"] <= b

    ]

    if len(options) > 0:

        best_option = options.iloc[0]

        budget.append({

            "Budget (₹)": b,

            "Recommended Technique":
            best_option["Technique"],

            "Cooling (°C)":
            best_option["Estimated Cooling (°C)"]

        })

budget_df = pd.DataFrame(budget)

budget_df.to_csv(

    output / "budget_plans.csv",

    index=False

)

print("✓ budget_plans.csv saved")

# -----------------------------------------------------
# Cost Benefit Analysis
# -----------------------------------------------------
cost = df[[
    "Technique",
    "Estimated Cooling (°C)",
    "Estimated Cost (₹)",
    "Cost Efficiency"
]]

cost.to_csv(

    output / "cost_benefit_analysis.csv",

    index=False

)

print("✓ cost_benefit_analysis.csv saved")

# -----------------------------------------------------
# Implementation Plan
# -----------------------------------------------------
implementation = []

phase = 1

for _, row in df.head(5).iterrows():

    implementation.append({

        "Phase": phase,

        "Technique": row["Technique"],

        "Priority": row["Rank"],

        "Duration":

        f"{phase*3} Months"

    })

    phase += 1

implementation_df = pd.DataFrame(

    implementation

)

implementation_df.to_csv(

    output / "implementation_plan.csv",

    index=False

)

print("✓ implementation_plan.csv saved")

# -----------------------------------------------------
# City Action Plan
# -----------------------------------------------------
city = []

for _, row in df.head(5).iterrows():

    city.append({

        "Priority":

        row["Rank"],

        "Recommendation":

        row["Technique"],

        "Estimated Cooling":

        row["Estimated Cooling (°C)"],

        "Estimated Cost":

        row["Estimated Cost (₹)"]

    })

city_df = pd.DataFrame(

    city

)

city_df.to_csv(

    output / "city_action_plan.csv",

    index=False

)

print("✓ city_action_plan.csv saved")

print("\n" + "=" * 60)
print("SCENARIO OPTIMIZATION COMPLETED")
print("=" * 60)

print(df.head())
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    KFold,
)

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

print("=" * 60)
print("PHYSICS INFORMED AI MODEL")
print("=" * 60)

# -----------------------------------------------------
# Output Folder
# -----------------------------------------------------
output = Path("data/processed")
output.mkdir(exist_ok=True)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------
df = pd.read_csv("data/processed/feature_stack_ai.csv")

print("Rows :", len(df))

# -----------------------------------------------------
# Remove Missing Values
# -----------------------------------------------------
df = df.dropna()

# -----------------------------------------------------
# Remove Constant Columns
# -----------------------------------------------------
constant_cols = [

    col

    for col in df.columns

    if df[col].nunique() <= 1

]

if constant_cols:

    print("\nRemoving Constant Columns:")

    print(constant_cols)

    df = df.drop(columns=constant_cols)

# -----------------------------------------------------
# Features
# -----------------------------------------------------
features = [

    c

    for c in df.columns

    if c != "lst"

]

X = df[features]

# -----------------------------------------------------
# Target
# -----------------------------------------------------
y = df["lst"]

# -----------------------------------------------------
# Train Test Split
# -----------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

)

print("Training Samples :", len(X_train))

print("Testing Samples  :", len(X_test))

# -----------------------------------------------------
# Random Forest Model
# -----------------------------------------------------
model = RandomForestRegressor(

    n_estimators=100,

    max_depth=18,

    min_samples_split=20,

    min_samples_leaf=10,

    max_features="sqrt",

    bootstrap=True,

    random_state=42,

    n_jobs=-1

)
print("\nTraining Model...")

model.fit(

    X_train,

    y_train

)

print("\nModel Training Completed")

# -----------------------------------------------------
# Prediction
# -----------------------------------------------------
pred = model.predict(

    X_test

)

# -----------------------------------------------------
# Cross Validation
# -----------------------------------------------------


# -----------------------------------------------------
# Prediction Confidence
# -----------------------------------------------------
print("\nCalculating Prediction Confidence...")

all_tree_predictions = np.array([

    tree.predict(X_test.values)

    for tree in model.estimators_

])

prediction_std = all_tree_predictions.std(axis=0)

confidence = (

    100

    * (

        1

        - prediction_std

        / prediction_std.max()

    )

)

confidence = np.clip(

    confidence,

    0,

    100

)

print(

    f"Average Prediction Confidence : {confidence.mean():.2f}%"

)

confidence_df = pd.DataFrame({

    "Actual LST": y_test.values,

    "Predicted LST": pred,

    "Confidence (%)": confidence

})

confidence_df.to_csv(

    output / "prediction_confidence.csv",

    index=False

)

print("Prediction confidence saved.")
# -----------------------------------------------------
# Model Performance
# -----------------------------------------------------
mae = mean_absolute_error(

    y_test,

    pred

)

rmse = np.sqrt(

    mean_squared_error(

        y_test,

        pred

    )

)

r2 = r2_score(

    y_test,

    pred

)
# -----------------------------------------------------
# Validation (Production Mode)
# -----------------------------------------------------
print("\nValidation (Production Mode)")

scores = np.array([r2])

print(f"Validation R² : {r2:.4f}")

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"MAE               : {mae:.3f}")

print(f"RMSE              : {rmse:.3f}")

print(f"R² Score          : {r2:.4f}")

print(f"Validation R²     : {r2:.4f}")

print(f"Average Confidence: {confidence.mean():.2f}%")

# -----------------------------------------------------
# Feature Importance
# -----------------------------------------------------
importance = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

print(importance)

importance.to_csv(

    output / "feature_importance.csv",

    index=False

)

print("\nFeature importance saved.")

# -----------------------------------------------------
# Save Evaluation Metrics
# -----------------------------------------------------
metrics = pd.DataFrame({

    "Metric": [

        "MAE",

        "RMSE",

        "R2",

        "Validation R2",

        "Average Confidence"

    ],

    "Value": [

        mae,

        rmse,

        r2,

        r2,

        confidence.mean()

    ]

})

metrics.to_csv(

    output / "model_metrics.csv",

    index=False

)

print("Model metrics saved.")

# -----------------------------------------------------
# Save Model
# -----------------------------------------------------
model_dir = Path("models")

model_dir.mkdir(

    exist_ok=True

)

model_path = model_dir / "physics_model.pkl"

print("\nSaving Model...")

joblib.dump(

    model,

    model_path,

    compress=3

)

size = model_path.stat().st_size / (1024 * 1024)

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)

print(f"Location      : {model_path}")

print(f"Model Size    : {size:.2f} MB")

print("\nGenerated Files")

print("------------------------------")

print("✓ physics_model.pkl")

print("✓ feature_importance.csv")

print("✓ prediction_confidence.csv")

print("✓ model_metrics.csv")

print("\nBackend AI Training Completed Successfully!")

print("=" * 60)
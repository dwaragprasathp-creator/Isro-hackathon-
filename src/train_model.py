from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

processed = Path("data/processed")

df = pd.read_csv(processed / "training_dataset.csv")

X = df[["ndvi", "ndwi", "ndbi", "lst"]]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("=" * 60)
print("MODEL TRAINED")
print("=" * 60)
print("Accuracy:", accuracy_score(y_test, pred))
print()
print(classification_report(y_test, pred))

models = Path("models")
models.mkdir(exist_ok=True)

joblib.dump(model, models / "heat_risk_rf.pkl")

print("Model saved:", models / "heat_risk_rf.pkl")
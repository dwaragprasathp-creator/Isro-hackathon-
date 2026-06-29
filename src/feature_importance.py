import joblib
import matplotlib.pyplot as plt

model = joblib.load("models/heat_risk_rf.pkl")

features = ["NDVI", "NDWI", "NDBI", "LST"]

plt.figure(figsize=(6,4))
plt.bar(features, model.feature_importances_)

plt.title("Random Forest Feature Importance")
plt.ylabel("Importance")
plt.tight_layout()

plt.show()
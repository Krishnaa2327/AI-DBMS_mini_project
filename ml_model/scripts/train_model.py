# ml_model/scripts/train_model.py
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]  # ml_model/
DATA_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"
SAVED_DIR = ROOT / "saved_models"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SAVED_DIR.mkdir(parents=True, exist_ok=True)

# load
df = pd.read_csv(DATA_DIR / "cleaned_disease_dataset.csv")
with open(DATA_DIR / "feature_info.json", "r") as f:
    feature_info = json.load(f)
feature_cols = feature_info["all_features"]  # list of 29 feature names
target_col = feature_info.get("target_column", "disease")

X = df[feature_cols]
y = df[target_col]

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# baseline model
rf = RandomForestClassifier(random_state=42, n_jobs=-1)

# small grid search (fast)
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_leaf": [1, 2]
}
gs = GridSearchCV(rf, param_grid, cv=3, n_jobs=-1, verbose=1)
gs.fit(X_train, y_train)

best = gs.best_estimator_
y_pred = best.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)
cm = confusion_matrix(y_test, y_pred).tolist()

# save model and artifacts
model_path = SAVED_DIR / "rf_model_v1.joblib"
joblib.dump(best, model_path)

# Save metadata
meta = {
    "model_path": str(model_path),
    "accuracy": acc,
    "best_params": gs.best_params_
}
with open(REPORTS_DIR / "metrics.json", "w") as f:
    json.dump({"accuracy": acc, "classification_report": report, "confusion_matrix": cm, "best_params": gs.best_params_}, f, indent=2)

print("Trained model saved to:", model_path)
print("Accuracy:", acc)

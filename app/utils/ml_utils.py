# app/utils/ml_utils.py
import joblib
import json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # repo root
MODEL_PATH = ROOT / "ml_model" / "saved_models" / "rf_model_v1.joblib"
FEATURE_INFO = ROOT / "ml_model" / "data" / "processed" / "feature_info.json"
DISEASE_MAP = ROOT / "ml_model" / "data" / "processed" / "disease_mapping.json"

# Load once
_model = None
_feature_cols = None
_disease_map = None  # numeric->label mapping if exists

def load_resources():
    global _model, _feature_cols, _disease_map
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _feature_cols is None:
        with open(FEATURE_INFO, "r") as f:
            info = json.load(f)
            _feature_cols = info["feature_columns"]
    if _disease_map is None and DISEASE_MAP.exists():
        with open(DISEASE_MAP, "r") as f:
            _disease_map = json.load(f)
    return _model, _feature_cols, _disease_map

def build_feature_vector(input_features: dict):
    """
    input_features: dict {feature_name: value}
    returns 2D numpy array shaped (1, n_features)
    """
    _, feature_cols, _ = load_resources()
    vec = []
    for c in feature_cols:
        vec.append(input_features.get(c, 0))
    return np.array([vec])

def predict(input_features: dict, top_k:int=3):
    model, _, disease_map = load_resources()
    X = build_feature_vector(input_features)
    probs = model.predict_proba(X)[0]
    classes = model.classes_
    # get top_k
    idx = probs.argsort()[-top_k:][::-1]
    results = []
    for i in idx:
        label = classes[i]
        prob = float(probs[i])
        if disease_map:
            # if mapping numeric -> name
            label = disease_map.get(str(label), label)
        results.append({"disease": str(label), "probability": prob})
    return results

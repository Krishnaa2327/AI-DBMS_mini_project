# app/main.py
import streamlit as st
import json
from app.utils import ml_utils
from database.db_config import get_connection
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Smart Hospital", layout="wide")
st.title("🏥 Smart Hospital — Disease Predictor (Phase 2)")

# load feature info to build symptom list
ROOT = Path(__file__).resolve().parents[2]
feature_info_path = ROOT / "ml_model" / "data" / "processed" / "feature_info.json"
if feature_info_path.exists():
    feature_info = json.loads(feature_info_path.read_text())
    feature_cols = feature_info["feature_columns"]
else:
    st.error("feature_info.json not found. Ask your teammate to create it.")
    feature_cols = []

# simple patient form
with st.form("patient_form"):
    st.subheader("Patient details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["M","F","Other"])
    st.subheader("Symptoms / Clinical indicators")
    # We assume symptom-like features are in feature_cols; show checkboxes for boolean features
    selected = {}
    cols = st.columns(3)
    for i, feat in enumerate(feature_cols):
        # treat numeric features differently if needed; here assume boolean 0/1
        cb = cols[i % 3].checkbox(feat.replace("_"," "), key=feat)
        selected[feat] = 1 if cb else 0
    submitted = st.form_submit_button("Predict Disease")
    if submitted:
        # add demographic features if present in feature_cols
        if "age" in feature_cols:
            selected["age"] = age
        if "sex_male" in feature_cols:
            selected["sex_male"] = 1 if gender == "M" else 0
        # call ML
        results = ml_utils.predict(selected, top_k=3)
        st.success("Predictions (top 3):")
        for r in results:
            st.write(f"- **{r['disease']}** — probability: {r['probability']:.2f}")
        # persist prediction to DB
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            import json, datetime
            try:
                cursor.execute(
                    "INSERT INTO predictions (patient_name, patient_age, patient_gender, input_features, predicted_labels, probabilities, model_version, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        name,
                        int(age),
                        gender,
                        json.dumps(selected),
                        json.dumps([r['disease'] for r in results]),
                        json.dumps([r['probability'] for r in results]),
                        "rf_model_v1",
                        datetime.datetime.now()
                    )
                )
                conn.commit()
                st.info("Prediction saved to DB (predictions table).")
            except Exception as e:
                st.error("Failed to save prediction to DB: " + str(e))
            finally:
                cursor.close()
                conn.close()

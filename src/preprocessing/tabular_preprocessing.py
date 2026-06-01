"""
Tabular Data Preprocessing Module
Handles preprocessing for diabetes and heart disease datasets.
Loads the real fitted scalers saved alongside the trained Random Forest models.

IMPORTANT: The scalers were fitted on pandas DataFrames with named columns
(from train_models.py), so we must pass DataFrames here too — not raw numpy
arrays — to avoid sklearn feature-name mismatch warnings and ensure correct
scaling.
"""

import pickle
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# ─── Feature column order (must match train_models.py exactly) ────────────────
DIABETES_FEATURES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

HEART_FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Dataset medians for diabetes zero-replacement (matches train_models.py logic)
DIABETES_MEDIANS = {
    'Glucose': 117, 'BloodPressure': 72,
    'SkinThickness': 23, 'Insulin': 79, 'BMI': 32
}


# ─── Scaler Loading ────────────────────────────────────────────────────────────

def _load_scaler(path: str, feature_names: list) -> StandardScaler:
    """Load a pickled scaler; fit a fallback if file is missing or corrupt."""
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                scaler = pickle.load(f)
            return scaler
        except Exception as e:
            print(f"⚠ Could not load scaler from {path}: {e}")

    # Fallback: fit a scaler on rough typical-range rows so the app still works
    print(f"⚠ Using fallback scaler for {path}")
    scaler = StandardScaler()
    if len(feature_names) == 8:   # diabetes
        typical = pd.DataFrame([
            [3, 120, 70, 20,  80, 30.0, 0.50, 30],
            [1,  90, 60, 15,  50, 25.0, 0.30, 25],
            [8, 180, 90, 40, 200, 40.0, 1.00, 50],
        ], columns=feature_names)
    else:                          # heart (13 features)
        typical = pd.DataFrame([
            [50, 1, 2, 120, 200, 0, 0, 150, 0, 1.0, 1, 0, 2],
            [35, 0, 0, 110, 180, 0, 0, 170, 0, 0.0, 0, 0, 1],
            [65, 1, 3, 140, 250, 1, 1, 130, 1, 2.5, 2, 2, 3],
        ], columns=feature_names)
    scaler.fit(typical)
    return scaler


_diabetes_scaler = _load_scaler(
    "models/tabular/diabetes_scaler.pkl", DIABETES_FEATURES)
_heart_scaler = _load_scaler(
    "models/tabular/heart_disease_scaler.pkl", HEART_FEATURES)


# ─── Public Preprocessing Functions ──────────────────────────────────────────

def preprocess_tabular_data(data, data_type="diabetes"):
    if data_type == "diabetes":
        return preprocess_diabetes_data(data)
    elif data_type == "heart_disease":
        return preprocess_heart_disease_data(data)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def preprocess_diabetes_data(data: dict) -> np.ndarray:
    """
    Preprocess a single patient's diabetes parameters.

    Builds a properly-named DataFrame (matching training columns),
    replaces physiologically impossible zeros with dataset medians,
    and scales with the real fitted StandardScaler.
    """
    # Build single-row DataFrame with correct column order
    row = pd.DataFrame([{f: data.get(f, 0) for f in DIABETES_FEATURES}],
                       columns=DIABETES_FEATURES).astype(float)

    # Replace impossible zeros with dataset medians (same as train_models.py)
    for col, med in DIABETES_MEDIANS.items():
        row.loc[row[col] == 0, col] = med

    return _diabetes_scaler.transform(row)


def preprocess_heart_disease_data(data: dict) -> np.ndarray:
    """
    Preprocess a single patient's cardiac parameters.

    Builds a properly-named DataFrame (matching training columns)
    and scales with the real fitted StandardScaler.
    """
    row = pd.DataFrame([{f: data.get(f, 0) for f in HEART_FEATURES}],
                       columns=HEART_FEATURES).astype(float)
    return _heart_scaler.transform(row)


# ─── Utilities ─────────────────────────────────────────────────────────────────

def handle_missing_values(df, strategy='median'):
    if strategy == 'median':
        return df.fillna(df.median())
    elif strategy == 'mean':
        return df.fillna(df.mean())
    elif strategy == 'mode':
        return df.fillna(df.mode().iloc[0])
    raise ValueError(f"Unknown strategy: {strategy}")

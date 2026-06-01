"""
Tabular ML Models
Handles predictions for diabetes and heart disease using ML models
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import pickle
import os

def predict_diabetes(data):
    """
    Predict diabetes risk from health parameters
    
    Args:
        data: Dictionary of health parameters
    
    Returns:
        (probability, prediction)
    """
    from src.preprocessing.tabular_preprocessing import preprocess_diabetes_data
    
    # Preprocess data
    processed_data = preprocess_diabetes_data(data)
    
    # Load or create model (demo: using mock model)
    model = get_diabetes_model()
    
    # Predict
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0][1] * 100  # Probability of positive class
    
    return probability, prediction

def predict_heart_disease(data):
    """
    Predict heart disease risk from cardiac parameters
    
    Args:
        data: Dictionary of cardiac health parameters
    
    Returns:
        (probability, prediction)
    """
    from src.preprocessing.tabular_preprocessing import preprocess_heart_disease_data
    
    # Preprocess data
    processed_data = preprocess_heart_disease_data(data)
    
    # Load or create model (demo: using mock model)
    model = get_heart_disease_model()
    
    # Predict
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0][1] * 100
    
    return probability, prediction

def get_diabetes_model():
    """
    Load trained diabetes prediction model
    
    Loads real trained Random Forest model if available,
    otherwise falls back to mock model for demo
    """
    model_path = "models/tabular/diabetes_model.pkl"
    
    if os.path.exists(model_path):
        try:
            print("✓ Loading REAL trained diabetes model")
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"⚠ Failed to load saved diabetes model ({e}); using mock model")

    print("⚠ Using MOCK diabetes model - run train_models.py to train real model")
    # Create demo model with synthetic training data
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Mock training data (8 features)
    # Negative cases
    X_neg = np.random.randn(50, 8) - 0.5
    y_neg = np.zeros(50)

    # Positive cases
    X_pos = np.random.randn(50, 8) + 0.5
    y_pos = np.ones(50)

    X_train = np.vstack([X_neg, X_pos])
    y_train = np.hstack([y_neg, y_pos])

    model.fit(X_train, y_train)

    return model

def get_heart_disease_model():
    """
    Load trained heart disease prediction model
    
    Loads real trained Random Forest model if available,
    otherwise falls back to mock model for demo
    """
    model_path = "models/tabular/heart_disease_model.pkl"
    
    if os.path.exists(model_path):
        try:
            print("✓ Loading REAL trained heart disease model")
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"⚠ Failed to load saved heart disease model ({e}); using mock model")

    print("⚠ Using MOCK heart disease model - run train_models.py to train real model")
    # Create demo model with synthetic training data
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Mock training data (13 features)
    # Negative cases
    X_neg = np.random.randn(50, 13) - 0.5
    y_neg = np.zeros(50)

    # Positive cases
    X_pos = np.random.randn(50, 13) + 0.5
    y_pos = np.ones(50)

    X_train = np.vstack([X_neg, X_pos])
    y_train = np.hstack([y_neg, y_pos])

    model.fit(X_train, y_train)

    return model

def train_model(X_train, y_train, model_type='random_forest'):
    """
    Train a new model on provided data
    
    Args:
        X_train: Training features
        y_train: Training labels
        model_type: 'random_forest' or 'logistic_regression'
    
    Returns:
        Trained model
    """
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    elif model_type == 'logistic_regression':
        model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    return model

def save_model(model, filepath):
    """
    Save trained model to disk
    
    Args:
        model: Trained scikit-learn model
        filepath: Path to save model
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

def load_model(filepath):
    """
    Load trained model from disk
    
    Args:
        filepath: Path to saved model
    
    Returns:
        Loaded model
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)

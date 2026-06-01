"""
NLP-based Symptom Analysis for VitalLens
Weighted keyword-to-disease scoring across all four supported conditions.
"""

from typing import Dict, List

# ─── Symptom-Disease Keyword Maps ─────────────────────────────────────────────
# Each keyword carries a weight: higher = stronger indicator
SYMPTOM_MAP: Dict[str, Dict[str, float]] = {
    # ── Diabetes ──────────────────────────────────────────────────────────────
    "thirst":              {"diabetes": 0.85},
    "frequent urination":  {"diabetes": 0.90},
    "urination":           {"diabetes": 0.80},
    "polyuria":            {"diabetes": 0.90},
    "polydipsia":          {"diabetes": 0.90},
    "polyphagia":          {"diabetes": 0.80},
    "excessive hunger":    {"diabetes": 0.75},
    "weight loss":         {"diabetes": 0.60, "brain_tumor": 0.25},
    "fatigue":             {"diabetes": 0.45, "heart_disease": 0.40, "pneumonia": 0.35},
    "blurred vision":      {"diabetes": 0.70, "brain_tumor": 0.50},
    "slow healing":        {"diabetes": 0.75},
    "tingling":            {"diabetes": 0.65},
    "numbness":            {"diabetes": 0.65, "brain_tumor": 0.30},
    "dark skin":           {"diabetes": 0.55},
    "yeast infection":     {"diabetes": 0.60},
    "dry mouth":           {"diabetes": 0.55},

    # ── Heart Disease ─────────────────────────────────────────────────────────
    "chest pain":          {"heart_disease": 0.90},
    "chest":               {"heart_disease": 0.60, "pneumonia": 0.55},
    "palpitations":        {"heart_disease": 0.75},
    "heart":               {"heart_disease": 0.55},
    "irregular heartbeat": {"heart_disease": 0.80},
    "shortness of breath": {"heart_disease": 0.75, "pneumonia": 0.70},
    "breathlessness":      {"heart_disease": 0.70, "pneumonia": 0.65},
    "swelling":            {"heart_disease": 0.65},
    "edema":               {"heart_disease": 0.70},
    "leg swelling":        {"heart_disease": 0.65},
    "dizziness":           {"heart_disease": 0.55, "brain_tumor": 0.45},
    "lightheadedness":     {"heart_disease": 0.60, "brain_tumor": 0.35},
    "fainting":            {"heart_disease": 0.65, "brain_tumor": 0.40},
    "syncope":             {"heart_disease": 0.70},
    "cold sweat":          {"heart_disease": 0.65},
    "nausea":              {"heart_disease": 0.45, "brain_tumor": 0.40, "pneumonia": 0.25},
    "jaw pain":            {"heart_disease": 0.70},
    "arm pain":            {"heart_disease": 0.65},
    "shoulder pain":       {"heart_disease": 0.55},

    # ── Pneumonia / COVID ─────────────────────────────────────────────────────
    "cough":               {"pneumonia": 0.80},
    "dry cough":           {"pneumonia": 0.85},
    "productive cough":    {"pneumonia": 0.80},
    "fever":               {"pneumonia": 0.75},
    "high fever":          {"pneumonia": 0.85},
    "chills":              {"pneumonia": 0.70},
    "sputum":              {"pneumonia": 0.75},
    "mucus":               {"pneumonia": 0.65},
    "breathing difficulty":{"pneumonia": 0.80, "heart_disease": 0.45},
    "oxygen":              {"pneumonia": 0.60},
    "pneumonia":           {"pneumonia": 0.95},
    "covid":               {"pneumonia": 0.90},
    "loss of taste":       {"pneumonia": 0.70},
    "anosmia":             {"pneumonia": 0.70},
    "loss of smell":       {"pneumonia": 0.70},
    "pleurisy":            {"pneumonia": 0.75},
    "wheezing":            {"pneumonia": 0.65},
    "respiratory":         {"pneumonia": 0.55},
    "lung":                {"pneumonia": 0.50},

    # ── Brain Tumor ───────────────────────────────────────────────────────────
    "headache":            {"brain_tumor": 0.65, "pneumonia": 0.15},
    "severe headache":     {"brain_tumor": 0.80},
    "morning headache":    {"brain_tumor": 0.85},
    "vision":              {"brain_tumor": 0.55},
    "vision loss":         {"brain_tumor": 0.75},
    "double vision":       {"brain_tumor": 0.70},
    "seizure":             {"brain_tumor": 0.85},
    "seizures":            {"brain_tumor": 0.85},
    "epilepsy":            {"brain_tumor": 0.80},
    "memory loss":         {"brain_tumor": 0.70},
    "confusion":           {"brain_tumor": 0.60},
    "personality change":  {"brain_tumor": 0.65},
    "cognitive":           {"brain_tumor": 0.55},
    "weakness":            {"brain_tumor": 0.55, "heart_disease": 0.35},
    "speech difficulty":   {"brain_tumor": 0.75},
    "hearing loss":        {"brain_tumor": 0.60},
    "balance":             {"brain_tumor": 0.60},
    "coordination":        {"brain_tumor": 0.60},
    "vomiting":            {"brain_tumor": 0.55, "pneumonia": 0.20},
    "mri":                 {"brain_tumor": 0.40},
    "tumor":               {"brain_tumor": 0.90},
    "glioma":              {"brain_tumor": 0.95},
    "meningioma":          {"brain_tumor": 0.95},
    "pituitary":           {"brain_tumor": 0.90},
}

DISEASES = ["diabetes", "heart_disease", "pneumonia", "brain_tumor"]
# Cap for accumulated scores (maps to ~100% probability)
SCORE_CAP = 2.0


def predict_from_symptoms(tokens: List[str]) -> Dict[str, float]:
    """
    Compute disease risk probabilities from preprocessed symptom tokens.

    Uses weighted keyword matching across a comprehensive symptom→disease map.
    Scores are accumulated, capped, and returned as 0-100 percentages.

    Returns:
        dict: {disease: probability_0_to_100}
    """
    if not tokens:
        return {d: 0.0 for d in DISEASES}

    # Reconstruct low-cased text for phrase matching
    text = " ".join(tokens).lower()

    scores: Dict[str, float] = {d: 0.0 for d in DISEASES}

    # Check each symptom keyword / phrase
    for keyword, disease_weights in SYMPTOM_MAP.items():
        if keyword in text:
            for disease, weight in disease_weights.items():
                scores[disease] += weight

    # Normalise to 0-100%, capping at SCORE_CAP → 100%
    result = {}
    for disease, score in scores.items():
        pct = min(score / SCORE_CAP, 1.0) * 100.0
        result[disease] = round(pct, 2)

    return result

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
from config import (
    MODEL_PATH,
    SCALER_PATH,
    FEATURE_NAMES,
    FEATURE_LABELS,
    FEATURE_CONSTRAINTS
)

_cached_model = None
_cached_scaler = None

def get_model_and_scaler():
    """Loads and caches the model and scaler from disk."""
    global _cached_model, _cached_scaler

    if _cached_model is None or _cached_scaler is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler file not found at: {SCALER_PATH}")

        _cached_model = joblib.load(MODEL_PATH)
        _cached_scaler = joblib.load(SCALER_PATH)

    return _cached_model, _cached_scaler

def validate_inputs(raw_inputs: Dict[str, Any]) -> Tuple[bool, str, Dict[str, float]]:
    """
    Validates that all expected features are present, numeric, and within physical/academic boundaries.
    Returns (is_valid, error_message, cleaned_inputs).
    """
    cleaned: Dict[str, float] = {}

    for feat in FEATURE_NAMES:
        if feat not in raw_inputs:
            return False, f"Missing required feature: '{feat}'", {}

        val = raw_inputs[feat]
        try:
            val_float = float(val)
        except (ValueError, TypeError):
            label = FEATURE_LABELS.get(feat, feat)
            return False, f"Invalid value for '{label}'. Must be a valid numeric value.", {}

        constraints = FEATURE_CONSTRAINTS[feat]
        min_val = constraints["min"]
        max_val = constraints["max"]

        if val_float < min_val or val_float > max_val:
            label = FEATURE_LABELS.get(feat, feat)
            return (
                False,
                f"Value for '{label}' ({val_float}) is outside allowable range [{min_val}, {max_val}].",
                {}
            )

        cleaned[feat] = val_float

    return True, "", cleaned

def compute_feature_attributions(
    model,
    scaler,
    cleaned_inputs: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Computes exact linear contributions (log-odds impact) for Logistic Regression:
    Contribution_j = beta_j * ((x_j - mean_j) / scale_j)
    """
    input_df = pd.DataFrame([cleaned_inputs], columns=FEATURE_NAMES)
    scaled_values = scaler.transform(input_df)[0]
    coefficients = model.coef_[0]

    contributions = []
    total_abs = sum(abs(coef * scaled_val) for coef, scaled_val in zip(coefficients, scaled_values))
    total_abs = max(total_abs, 1e-6)

    for i, feat in enumerate(FEATURE_NAMES):
        z_score = float(scaled_values[i])
        coef = float(coefficients[i])
        raw_contrib = coef * z_score
        relative_pct = (abs(raw_contrib) / total_abs) * 100

        if raw_contrib > 0.05:
            impact_direction = "Positive Driver"
        elif raw_contrib < -0.05:
            impact_direction = "Negative Driver"
        else:
            impact_direction = "Neutral"

        contributions.append({
            "feature": feat,
            "label": FEATURE_LABELS.get(feat, feat),
            "input_value": cleaned_inputs[feat],
            "mean": float(scaler.mean_[i]),
            "scale": float(scaler.scale_[i]),
            "coefficient": coef,
            "z_score": z_score,
            "contribution": raw_contrib,
            "relative_percentage": round(relative_pct, 1),
            "direction": impact_direction
        })

    # Sort contributions by absolute impact descending
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    return contributions

def predict_placement(raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    End-to-end validated placement prediction with probability, confidence,
    risk level, and explainable feature contributions.
    """
    is_valid, err_msg, cleaned = validate_inputs(raw_inputs)
    if not is_valid:
        raise ValueError(err_msg)

    model, scaler = get_model_and_scaler()

    # Create DataFrame with exact column names to match model & scaler metadata
    input_df = pd.DataFrame([cleaned], columns=FEATURE_NAMES)
    scaled_array = scaler.transform(input_df)
    scaled_df = pd.DataFrame(scaled_array, columns=FEATURE_NAMES)

    # Scikit-Learn predictions
    raw_pred = model.predict(scaled_df)[0]
    proba = model.predict_proba(scaled_df)[0]

    # Model classes: ['Not Placed', 'Placed']
    # Index 1 corresponds to 'Placed'
    placed_prob = float(proba[1] * 100)
    confidence = float(max(proba) * 100)

    # Risk level classification
    if placed_prob >= 80.0:
        risk_level = "Very Low Risk"
        risk_color = "#10b981"  # Emerald
    elif placed_prob >= 60.0:
        risk_level = "Low Risk"
        risk_color = "#3b82f6"  # Blue
    elif placed_prob >= 40.0:
        risk_level = "Medium Risk"
        risk_color = "#f59e0b"  # Amber
    else:
        risk_level = "High Risk"
        risk_color = "#ef4444"  # Red

    overall_score = (
        cleaned["attendance"]
        + cleaned["previous_score"]
        + cleaned["exam_score"]
    ) / 3.0

    attributions = compute_feature_attributions(model, scaler, cleaned)

    return {
        "prediction_result": str(raw_pred),
        "is_placed": (raw_pred == "Placed"),
        "placement_probability": round(placed_prob, 2),
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "overall_score": round(overall_score, 2),
        "inputs": cleaned,
        "attributions": attributions
    }

import pytest
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.prediction import validate_inputs, predict_placement
from config import FEATURE_NAMES

def test_validate_inputs_success():
    valid = {
        "study_hours": 6,
        "attendance": 80,
        "sleep_hours": 7,
        "internet_usage": 4,
        "assignments_completed": 12,
        "previous_score": 70,
        "exam_score": 85.0
    }
    is_valid, msg, cleaned = validate_inputs(valid)
    assert is_valid is True
    assert msg == ""
    assert len(cleaned) == 7
    assert cleaned["exam_score"] == 85.0

def test_validate_inputs_missing_feature():
    invalid = {
        "study_hours": 6,
        "attendance": 80
    }
    is_valid, msg, _ = validate_inputs(invalid)
    assert is_valid is False
    assert "Missing required feature" in msg

def test_validate_inputs_out_of_range():
    invalid = {
        "study_hours": 6,
        "attendance": 150,  # Max is 100
        "sleep_hours": 7,
        "internet_usage": 4,
        "assignments_completed": 12,
        "previous_score": 70,
        "exam_score": 85.0
    }
    is_valid, msg, _ = validate_inputs(invalid)
    assert is_valid is False
    assert "outside allowable range" in msg

def test_predict_placement_placed_case():
    inputs = {
        "study_hours": 8,
        "attendance": 90,
        "sleep_hours": 7,
        "internet_usage": 3,
        "assignments_completed": 20,
        "previous_score": 85,
        "exam_score": 95.0
    }
    result = predict_placement(inputs)
    assert result["prediction_result"] in ["Placed", "Not Placed"]
    assert 0.0 <= result["placement_probability"] <= 100.0
    assert 0.0 <= result["confidence"] <= 100.0
    assert result["risk_level"] in ["Very Low Risk", "Low Risk", "Medium Risk", "High Risk"]
    assert len(result["attributions"]) == 7
    assert result["prediction_result"] == "Placed"

def test_predict_placement_not_placed_case():
    inputs = {
        "study_hours": 1,
        "attendance": 35,
        "sleep_hours": 4,
        "internet_usage": 14,
        "assignments_completed": 1,
        "previous_score": 30,
        "exam_score": 35.0
    }
    result = predict_placement(inputs)
    assert result["prediction_result"] == "Not Placed"
    assert result["placement_probability"] < 50.0
    assert result["risk_level"] in ["High Risk", "Medium Risk"]

import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent

# Data directory
DATA_DIR = BASE_DIR / "data"
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
MODEL_PATH = BASE_DIR / "placement_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
LOCAL_DATASET_PATH = DATA_DIR / "student_dataset_10000_rows.csv"
FALLBACK_DATASET_PATH = Path(r"C:\Users\karth\Downloads\student_dataset_10000_rows.csv")

def get_dataset_path() -> Path:
    """Returns the existing dataset path, prioritizing local project data/ folder."""
    if LOCAL_DATASET_PATH.exists():
        return LOCAL_DATASET_PATH
    if FALLBACK_DATASET_PATH.exists():
        return FALLBACK_DATASET_PATH
    raise FileNotFoundError(
        f"Placement dataset not found at {LOCAL_DATASET_PATH} or {FALLBACK_DATASET_PATH}"
    )

DATABASE_PATH = DATA_DIR / "placementiq.db"

# Feature schema and ordering required by model & scaler
FEATURE_NAMES = [
    "study_hours",
    "attendance",
    "sleep_hours",
    "internet_usage",
    "assignments_completed",
    "previous_score",
    "exam_score"
]

FEATURE_LABELS = {
    "study_hours": "Study Hours (hrs/day)",
    "attendance": "Attendance (%)",
    "sleep_hours": "Sleep Hours (hrs/day)",
    "internet_usage": "Internet Usage (hrs/day)",
    "assignments_completed": "Assignments Completed (count)",
    "previous_score": "Previous Academic Score (%)",
    "exam_score": "Examination Score (%)"
}

FEATURE_CONSTRAINTS = {
    "study_hours": {"min": 0, "max": 24, "default": 6, "step": 1},
    "attendance": {"min": 0, "max": 100, "default": 75, "step": 1},
    "sleep_hours": {"min": 0, "max": 16, "default": 7, "step": 1},
    "internet_usage": {"min": 0, "max": 24, "default": 5, "step": 1},
    "assignments_completed": {"min": 0, "max": 50, "default": 10, "step": 1},
    "previous_score": {"min": 0, "max": 100, "default": 65, "step": 1},
    "exam_score": {"min": 0.0, "max": 100.0, "default": 75.0, "step": 0.5}
}

APP_TITLE = "PlacementIQ"
APP_SUBTITLE = "Intelligent Student Placement Analytics Platform"
VERSION = "2.0.0"

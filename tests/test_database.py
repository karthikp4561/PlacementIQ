import pytest
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.database import (
    init_db,
    create_user,
    save_prediction,
    get_user_predictions,
    get_prediction_by_id,
    delete_prediction,
    get_admin_system_metrics
)

def test_database_isolation_and_predictions():
    init_db()
    # Create two distinct test students
    u1_name = f"stu1_{uuid.uuid4().hex[:6]}"
    u2_name = f"stu2_{uuid.uuid4().hex[:6]}"

    create_user(u1_name, f"{u1_name}@test.com", "Student One", "Pass@123")
    create_user(u2_name, f"{u2_name}@test.com", "Student Two", "Pass@123")

    from utils.database import authenticate_user
    user1 = authenticate_user(u1_name, "Pass@123")
    user2 = authenticate_user(u2_name, "Pass@123")

    assert user1 is not None and user2 is not None

    sample_inputs = {
        "study_hours": 6, "attendance": 80, "sleep_hours": 7,
        "internet_usage": 4, "assignments_completed": 10,
        "previous_score": 65, "exam_score": 75.0
    }

    # Save prediction for Student 1
    p1_id = save_prediction(
        user_id=user1["id"],
        inputs=sample_inputs,
        prediction_result="Placed",
        placement_probability=85.5,
        confidence=85.5,
        risk_level="Low Risk"
    )

    # Save prediction for Student 2
    p2_id = save_prediction(
        user_id=user2["id"],
        inputs=sample_inputs,
        prediction_result="Not Placed",
        placement_probability=25.0,
        confidence=75.0,
        risk_level="High Risk"
    )

    # Student 1 fetches their history
    s1_history = get_user_predictions(user1["id"])
    assert any(p["id"] == p1_id for p in s1_history)
    assert not any(p["id"] == p2_id for p in s1_history)  # Isolation verified!

    # Student 1 attempts to directly fetch Student 2's prediction by ID
    isolated_fetch = get_prediction_by_id(p2_id, user_id=user1["id"])
    assert isolated_fetch is None  # Student 1 cannot view Student 2's record!

    # Admin metrics should include both
    metrics = get_admin_system_metrics()
    assert metrics["total_predictions"] >= 2

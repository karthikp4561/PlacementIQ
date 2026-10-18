import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.prediction import predict_placement
from utils.recommendations import generate_recommendations
from utils.report import generate_pdf_report

def test_generate_pdf_report():
    sample = {
        'study_hours': 6,
        'attendance': 85,
        'sleep_hours': 7,
        'internet_usage': 4,
        'assignments_completed': 12,
        'previous_score': 70,
        'exam_score': 82.5
    }
    pred_res = predict_placement(sample)
    recs = generate_recommendations(sample, pred_res['prediction_result'], pred_res['placement_probability'])
    user = {'username': 'test_student', 'email': 'student@test.com', 'full_name': 'Test Student', 'role': 'student'}

    pdf_bytes = generate_pdf_report(user, pred_res, recs)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF")

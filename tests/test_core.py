import pytest
from core import queries, ml_inference

def test_queries_kpis():
    kpis = queries.get_overall_kpis()
    assert isinstance(kpis, dict)
    assert 'attendance_rate' in kpis
    assert 'completion_rate' in kpis

def test_ml_inference():
    result = ml_inference.predict(attendance_rate=0.9, pretest_score=80.0, durasi_hari=5)
    assert isinstance(result, dict)
    assert 'probability' in result
    assert 'status_lulus' in result
    assert isinstance(result['probability'], float)
    assert isinstance(result['status_lulus'], bool)

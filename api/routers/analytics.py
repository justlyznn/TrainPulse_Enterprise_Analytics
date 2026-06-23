from fastapi import APIRouter
from core import queries

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.get("/kpis")
def get_kpis():
    return queries.get_overall_kpis()

@router.get("/attendance-trend")
def get_attendance_trend():
    return queries.get_attendance_trend()

@router.get("/completion-by-category")
def get_completion_by_category():
    return queries.get_completion_by_category()

@router.get("/attendance-by-department")
def get_attendance_by_department():
    return queries.get_attendance_by_department()

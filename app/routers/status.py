
from fastapi import APIRouter

from app.database.engine import check_availability

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/status")
def status_check():
    check_availability()
    return {"status": "ok"}
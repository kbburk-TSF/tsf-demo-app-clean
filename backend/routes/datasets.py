from fastapi import APIRouter
router = APIRouter()

@router.get("/air_quality")
def air_quality():
    # Minimal stub endpoint
    return {"pm25": [12, 11, 13], "days": 3}

from fastapi import APIRouter
router = APIRouter()
@router.get('/')
def forecast():
    return {'message': 'Forecast placeholder'}

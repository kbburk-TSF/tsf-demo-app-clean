from fastapi import APIRouter
from sqlalchemy import text
from backend.db import engine

router = APIRouter()

@router.get('/preview')
def preview_seasonal(limit: int = 5):
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM ME_S_MR30 LIMIT :limit'), {'limit': limit})
        rows = [dict(row._mapping) for row in result]
    return {'preview': rows}

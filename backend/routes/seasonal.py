from fastapi import APIRouter
from sqlalchemy import text
from backend.db import engine

router = APIRouter()

@router.get("/preview")
def preview(limit: int = 5):
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT date, value FROM ME_S_MR30 ORDER BY date ASC LIMIT :lim"), {"lim": limit}).mappings().all()
    return {"rows": [dict(r) for r in rows]}

# --- Bootstrap seasonal table & sample data on first boot (Railway-friendly) ---
import os as _os
from sqlalchemy import text as _text
try:
    from backend.db import engine as _engine
except Exception:
    # Fallback import if layout differs
    from ..db import engine as _engine  # type: ignore

def _bootstrap_seasonal_table():
    csv_path = _os.path.join(_os.path.dirname(__file__), "..", "data", "seasonal_models", "ME-S-MR30.csv")
    csv_path = _os.path.abspath(csv_path)
    # Normalize path relative to repo root if needed
    if not _os.path.exists(csv_path):
        csv_path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", "data", "seasonal_models", "ME-S-MR30.csv"))

    with _engine.begin() as conn:
        conn.execute(_text("""
            CREATE TABLE IF NOT EXISTS ME_S_MR30 (
                id SERIAL PRIMARY KEY,
                date DATE,
                value DOUBLE PRECISION
            );
        """))
        cnt = conn.execute(_text("SELECT COUNT(*) FROM ME_S_MR30")).scalar()
        if cnt == 0 and _os.path.exists(csv_path):
            import csv
            with open(csv_path, newline="") as f:
                rdr = csv.DictReader(f)
                rows = []
                for r in rdr:
                    try:
                        rows.append({"date": r.get("date") or r.get("Date") or r.get("DATE"), "value": float(r.get("value") or r.get("Value") or r.get("VALUE"))})
                    except Exception:
                        continue
            # Chunked insert
            for i in range(0, len(rows), 1000):
                chunk = rows[i:i+1000]
                if chunk:
                    conn.execute(_text("INSERT INTO ME_S_MR30 (date, value) VALUES (:date, :value)"), chunk)

# invoke bootstrap
try:
    _bootstrap_seasonal_table()
except Exception as _e:
    # Avoid crashing the API if seed load fails; log to stdout
    print("Seasonal bootstrap warning:", _e)
# --- end bootstrap ---

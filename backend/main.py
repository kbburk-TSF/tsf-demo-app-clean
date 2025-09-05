import csv
import io
import asyncio
import os
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import engine, Base, get_db
import models

# ✅ Create database tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Allow frontend to connect
origins = [
    "https://tsf-demo-frontend.onrender.com",  # frontend Render URL
    "http://localhost:3000",                   # optional local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend connected. Upload CSV to populate datasets."}

# ✅ In-memory progress tracker
progress_store = {}

@app.post("/upload-csv/")
async def upload_csv(
    dataset: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload CSV → parse rows → insert into Postgres via SQLAlchemy.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    task_id = f"{dataset}_{file.filename}"
    progress_store[task_id] = "Starting upload..."

    # ✅ Read CSV into memory
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.reader(io.StringIO(decoded))

    headers = next(reader, None)
    if not headers:
        raise HTTPException(status_code=400, detail="CSV has no headers")

    progress_store[task_id] = "Inserting rows into database..."

    # ✅ Example: Save rows into a table (adjust model to your schema)
    for i, row in enumerate(reader, start=1):
        record = models.DatasetRow(
            dataset=dataset,
            row_data=str(row)  # ⚠️ Simplified: store whole row as text
        )
        db.add(record)

        if i % 100 == 0:
            db.commit()
            progress_store[task_id] = f"Inserted {i} rows..."

    db.commit()
    progress_store[task_id] = f"✅ Upload complete. Inserted {i} rows."
    return {"task_id": task_id}

@app.get("/progress/{task_id}")
def get_progress(task_id: str):
    return {"status": progress_store.get(task_id, "Unknown task")}

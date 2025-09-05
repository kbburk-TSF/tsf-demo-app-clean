import os
import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import engine, Base, get_db  # ✅ fixed: absolute imports

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Allow frontend to connect
origins = [
    "https://tsf-demo-frontend.onrender.com",  # your deployed frontend
    "http://localhost:3000",                   # optional local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple health check
@app.get("/")
def root():
    return {"message": "Backend connected. Upload CSV to populate datasets."}

# In-memory progress store
progress_store = {}

@app.post("/upload-csv/")
async def upload_csv(
    dataset: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload CSV and simulate processing with progress tracking.
    """
    task_id = f"{dataset}_{file.filename}"
    progress_store[task_id] = "Starting upload..."

    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    save_path = f"uploads/{task_id}"

    # Save the uploaded file
    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    # Simulate step-by-step processing
    steps = ["Validating CSV", "Cleaning data", "Saving to DB", "Done"]
    for step in steps:
        progress_store[task_id] = step
        await asyncio.sleep(2)  # simulate time-consuming work

    progress_store[task_id] = f"✅ Upload and processing complete for {file.filename}"
    return {"task_id": task_id}

@app.get("/progress/{task_id}")
def get_progress(task_id: str):
    """
    Return latest progress update.
    """
    return {"status": progress_store.get(task_id, "Unknown task")}

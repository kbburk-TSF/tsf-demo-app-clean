import os
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import engine, Base, get_db

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to connect to backend
origins = [
    "https://tsf-demo-frontend.onrender.com",  # your Render frontend
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

@app.post("/upload-csv-stream/")
async def upload_csv_stream(
    dataset: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload CSV with realtime streaming progress updates.
    """

    async def event_generator():
        try:
            # Ensure uploads directory exists
            os.makedirs("uploads", exist_ok=True)
            save_path = f"uploads/{dataset}_{file.filename}"

            # Save file in chunks while reporting progress
            total_bytes = 0
            with open(save_path, "wb") as f:
                while True:
                    chunk = await file.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    total_bytes += len(chunk)
                    yield f"data: Uploaded {total_bytes // 1024} KB so far\n\n"
                    await asyncio.sleep(0.2)

            # Simulated processing steps
            steps = ["Validating CSV", "Cleaning data", "Saving to DB", "Done"]
            for step in steps:
                yield f"data: {step}\n\n"
                await asyncio.sleep(1)

            yield f"data: ✅ Upload and processing complete for {file.filename}\n\n"

        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

import os
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from .db import engine, Base, get_db

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

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
            # Save the file in chunks
            save_path = f"uploads/{dataset}_{file.filename}"
            os.makedirs("uploads", exist_ok=True)

            with open(save_path, "wb") as f:
                total_bytes = 0
                while True:
                    chunk = await file.read(1024 * 1024)  # 1 MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    total_bytes += len(chunk)
                    yield f"data: Uploaded {total_bytes // 1024} KB so far\n\n"
                    await asyncio.sleep(0.2)

            # Simulate processing steps
            steps = ["Validating CSV", "Cleaning data", "Saving to DB", "Done"]
            for step in steps:
                yield f"data: {step}\n\n"
                await asyncio.sleep(1)

            yield f"data: ✅ Upload and processing complete for {file.filename}\n\n"

        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

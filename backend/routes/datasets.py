from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/air_quality")
def air_quality():
    # Minimal stub endpoint
    return {"pm25": [12, 11, 13], "days": 3}

@router.post("/datasets/upload")
async def upload_dataset(dataset: str = Form(...), file: UploadFile = File(...)):
    """
    Handle dataset upload (CSV).
    """
    try:
        # Save file to uploads folder
        file_location = os.path.join(UPLOAD_DIR, f"{dataset}_{file.filename}")
        with open(file_location, "wb") as f:
            contents = await file.read()
            f.write(contents)

        return {"message": f"File '{file.filename}' uploaded successfully for dataset '{dataset}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

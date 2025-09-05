from fastapi import FastAPI, UploadFile, File
import pandas as pd
from sqlalchemy import create_engine
import os

app = FastAPI()

# Database URL from Render env variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)

@app.get("/")
def root():
    return {"message": "Backend is running on Render!"}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        if DATABASE_URL:
            df.to_sql("air_quality", engine, if_exists="append", index=False)
        return {"rows": len(df), "columns": list(df.columns)}
    except Exception as e:
        return {"error": str(e)}

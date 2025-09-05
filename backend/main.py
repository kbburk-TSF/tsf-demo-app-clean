import os
import io
import csv
import datetime
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import engine, Base, get_db
from .models import AirQuality, Finance, FlightPerformance

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend connected. Upload CSV to populate datasets."}


@app.post("/upload-csv/")
async def upload_csv(
    dataset: str = Form(...),  # which dataset: "air_quality", "finance", "flight_performance"
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a CSV file and insert rows into the chosen dataset.
    """
    try:
        content = await file.read()
        decoded = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))

        rows_added = 0

        if dataset == "air_quality":
            for row in reader:
                record = AirQuality(
                    date_local=datetime.datetime.strptime(row["Date Local"], "%Y-%m-%d").date(),
                    parameter_name=row["Parameter Name"],
                    arithmetic_mean=float(row["Arithmetic Mean"]),
                    local_site_name=row.get("Local Site Name"),
                    state_name=row.get("State Name"),
                    county_name=row.get("County Name"),
                    city_name=row.get("City Name"),
                    cbsa_name=row.get("CBSA Name"),
                )
                db.add(record)
                rows_added += 1

        elif dataset == "finance":
            for row in reader:
                record = Finance(
                    date=datetime.datetime.strptime(row["DATE"], "%Y-%m-%d").date(),
                    stock_price=float(row["STOCK_PRICE"]),
                )
                db.add(record)
                rows_added += 1

        elif dataset == "flight_performance":
            for row in reader:
                record = FlightPerformance(
                    date=datetime.datetime.strptime(row["DATE"], "%Y-%m-%d").date(),
                    passenger_count=int(row["PASSENGER_COUNT"]),
                )
                db.add(record)
                rows_added += 1

        else:
            raise HTTPException(status_code=400, detail="Invalid dataset type.")

        db.commit()
        return {"message": f"Successfully added {rows_added} rows to {dataset}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

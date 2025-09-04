import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import datasets, forecast, seasonal

app = FastAPI(title="TSF Demo Engine")

# CORS for browser-based frontends; tighten this later if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TSF Demo Engine API running"}

# mount routers
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
app.include_router(seasonal.router, prefix="/seasonal", tags=["seasonal"])

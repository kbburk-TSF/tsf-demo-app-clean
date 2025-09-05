from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from .db import Base
import datetime


# -------------------------
# Air Quality (Realistic Schema)
# -------------------------
class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, index=True)
    date_local = Column(Date, nullable=False)  # "Date Local"
    parameter_name = Column(String, nullable=False)  # e.g. PM2.5, Ozone
    arithmetic_mean = Column(Float, nullable=False)  # "Arithmetic Mean"

    # Location info
    local_site_name = Column(String, nullable=True)
    state_name = Column(String, nullable=True)
    county_name = Column(String, nullable=True)
    city_name = Column(String, nullable=True)
    cbsa_name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# -------------------------
# Finance (Dummy Schema)
# -------------------------
class Finance(Base):
    __tablename__ = "finance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    stock_price = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# -------------------------
# Flight Performance (Dummy Schema)
# -------------------------
class FlightPerformance(Base):
    __tablename__ = "flight_performance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    passenger_count = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

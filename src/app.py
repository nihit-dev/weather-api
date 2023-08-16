from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Weather, WeatherStats
from typing import Optional
import datetime

app = FastAPI()

# Simulate database connection
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class WeatherQueryParams(BaseModel):
    """Pydantic model for query parameters used in weather_home endpoint."""
    page: Optional[int] = Query(1, description="Page number")
    date: Optional[datetime.date] = Query(None, description="Date filter (YYYY-MM-DD)")
    station: Optional[str] = Query(None, description="Station filter")


class WeatherStatsQueryParams(BaseModel):
    """Pydantic model for query parameters used in stats endpoint."""
    page: Optional[int] = Query(1, description="Page number")
    year: Optional[int] = Query(None, description="Year filter")
    station: Optional[str] = Query(None, description="Station filter")


# Endpoints
@app.get("/api/weather/")
async def weather_home(params: WeatherQueryParams = Depends()):
    """
    Endpoint to fetch weather data based on query parameters.

    Parameters:
        params (WeatherQueryParams): Pydantic model for query parameters.

    Returns:
        List[dict]: List of dictionaries containing weather data.
    """

    db = SessionLocal()
    result = db.query(Weather)
    if params.date:
        result = result.filter(Weather.date == params.date)
    if params.station:
        result = result.filter(Weather.station_id == params.station)
    result = result.offset((params.page - 1) * 100).limit(100).all()
    return [r.as_dict() for r in result]


@app.get("/api/weather/stats/")
async def stats(params: WeatherStatsQueryParams = Depends()):
    """
    Endpoint to fetch weather statistics based on query parameters.

    Parameters:
        params (WeatherStatsQueryParams): Pydantic model for query parameters.

    Returns:
        List[dict]: List of dictionaries containing weather statistics.
    """
    db = SessionLocal()
    query = db.query(WeatherStats)
    if params.year:
        query = query.filter(WeatherStats.year == int(params.year))
    if params.station:
        query = query.filter(WeatherStats.station_id == params.station)
    result = query.offset((params.page - 1) * 100).limit(100).all()
    return [r.as_dict() for r in result]

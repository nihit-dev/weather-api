from fastapi import FastAPI
from fastapi.testclient import TestClient
from app import WeatherStatsQueryParams, WeatherQueryParams
import json
from app import app


client = TestClient(app)


def test_read_main():
    params = WeatherQueryParams(
        page=1,
        date="1985-01-01",
        station="USC00257715"
    )
    response = client.get(
        "/api/weather/", params=params.model_dump())
    assert response.status_code == 200
    assert response.json() == [{"id": 1,
                                "station_id": "USC00257715",
                                "date": "1985-01-01",
                                "max_temp": -8.3,
                                "min_temp": -14.4,
                                "precipitation": 0.0
                                }]


def test_weather_stat():
    params = WeatherStatsQueryParams(
        page=1,
        year=1985,
        station="USC00110072"
    )
    response = client.get(
        "/api/weather/stats", params=params.model_dump())
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "avg_max_temp": 15.33,
        "avg_min_temp": 4.33,
        "total_precipitation": 780.1,
        "year": 1985,
        "station_id": "USC00110072"
    }]

# Import necessary modules
import datetime
import os
import csv
from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import sessionmaker
from models import Base, Weather, WeatherStats

# Database settings
DATABASE_URL = "sqlite:///./database.db"  # Change this to your database URL
engine = create_engine(DATABASE_URL)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# Replace invalid data values
def replaceifinvalid(x):
    """Replace invalid data value with None or valid value."""
    if x == "-9999":
        return None
    return int(x) / 10


# Truncate the Weather and WeatherStats tables
def truncate_tables(session):
    """Truncate the Weather and WeatherStats tables."""
    try:
        session.query(Weather).delete()
        session.query(WeatherStats).delete()
        session.commit()
    except Exception as e:
        print("An error occurred while truncating tables:", e)
        session.rollback()


# Ingest data from files into the database
def ingest_file(session, station, filepath):
    """Ingest weather data from a file into the database."""
    with open(filepath, "r") as file:
        reader = csv.reader(file, delimiter="\t")

        weather_list = [
            Weather(
                station_id=station,
                date=datetime.datetime.strptime(x[0], "%Y%m%d"),
                max_temp=replaceifinvalid(x[1]),
                min_temp=replaceifinvalid(x[2]),
                precipitation=replaceifinvalid(x[3]),
            )
            for x in reader
        ]

        session.bulk_save_objects(weather_list)
        session.commit()


# Ingest data from multiple files
def ingest_items(weather_data):
    """Ingest weather data from multiple files into the database."""
    Session = sessionmaker(bind=engine)  # Define your SQLAlchemy session
    session = Session()
    truncate_tables(session)  # Truncate tables before ingesting data

    for file_data in os.listdir(weather_data):
        if file_data.endswith(".txt"):
            station = file_data[:11]
            filepath = os.path.join(weather_data, file_data)
            print("Inserting ", file_data)
            ingest_file(session, station, filepath)

    session.close()


# Calculate and store aggregated weather statistics
def calculate_weather_stats():
    """Calculate and store aggregated weather statistics."""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        query = session.query(
            extract("year", Weather.date).label("year"),
            Weather.station_id,
            func.round(func.avg(Weather.max_temp), 2).label("avg_max_temp"),
            func.round(func.avg(Weather.min_temp), 2).label("avg_min_temp"),
            func.round(func.sum(Weather.precipitation),
                       2).label("total_precipitation"),
        ).group_by(extract("year", Weather.date), Weather.station_id)

        for result in query:
            weather_stats = WeatherStats(
                year=result.year,
                station_id=result.station_id,
                avg_max_temp=result.avg_max_temp,
                avg_min_temp=result.avg_min_temp,
                total_precipitation=result.total_precipitation,
            )
            session.add(weather_stats)

        session.commit()
    except Exception as e:
        print("An error occurred:", e)
        session.rollback()
    finally:
        session.close()


# Call the functions to ingest data and calculate statistics
ingest_items("../wx_data")
calculate_weather_stats()

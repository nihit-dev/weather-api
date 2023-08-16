from sqlalchemy import Column, Integer, String, DATE, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String)
    date = Column(DATE)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precipitation = Column(Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




class WeatherStats(Base):
    __tablename__ = "weather_stats"
    id = Column(Integer, primary_key=True, index=True)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)
    year = Column(Integer)
    station_id = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

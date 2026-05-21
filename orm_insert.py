import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, Integer, Float, String, DateTime

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = "Karachi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

res = requests.get(url)

data = res.json()


row = {
    "city": data["name"],
    "temp": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather": data["weather"][0]["description"],
}

row["timestamp"] = datetime.now()


class Base(DeclarativeBase):
    pass

class weatherLog(Base):
    __tablename__="weather_log"
    id=Column(Integer, primary_key=True)
    city=Column(String)
    temp = Column(Float)
    humidity = Column(Integer)
    weather = Column(String)
    timestamp = Column(DateTime)


obj=weatherLog(city=row["city"], temp=row["temp"],humidity=row["humidity"], weather=row["weather"], timestamp=row["timestamp"])

engine=create_engine(os.getenv("DB_URL"))

with Session(engine) as session:
    session.add(obj)
    session.commit()
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))

# fetch data here (same as before)
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


with engine.connect() as conn:
    conn.execute(text("insert into weather_log (city, temp, humidity, weather, timestamp) values(:city, :temp, :humidity, :weather, :timestamp)"), {"city": row["city"], "temp":row["temp"], "humidity":row["humidity"], "weather":row["weather"], "timestamp":row["timestamp"]})
    conn.commit()
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_URL = os.getenv("DB_URL")
CITY = "Karachi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"



def extract():    
    

    res = requests.get(url)
    data = res.json()

    logger.info(f"Fetched weather for {CITY}: {data['main']['temp']}°C")
    return data

def transform(data):
    row = {
    "city": data["name"],
    "temp": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather": data["weather"][0]["description"],
    "timestamp": datetime.now(),
    }
    return row

def load(row):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO weather_log (city, temp, humidity, weather, timestamp) VALUES (%s, %s, %s, %s, %s)",
    (row["city"], row["temp"], row["humidity"], row["weather"], row["timestamp"]),
    )

    conn.commit()
    conn.close()

    logger.info("Row inserted into DB successfully")


try:
    obj_extract = extract()
    obj_transform =transform(obj_extract)
    load(obj_transform)

except Exception as e:
    logger.error(f"something went wrong: {e}")
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
print(os.getenv("DB_URL"))
conn=psycopg2.connect(os.getenv("DB_URL"))
cursor=conn.cursor()


print("KEY:", os.getenv("API_KEY"))

API_KEY = os.getenv("API_KEY")
CITY = "Karachi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

res = requests.get(url)
logger.info(f"Fetched weather for {CITY}: {data['main']['temp']} degree celsisus")

print(res)
print()

data = res.json()
#print(res.text)
print()
# print(data)

print(data["main"]["temp"])
print(data["main"]["humidity"])
print(data["weather"][0]["description"])

data = res.json()

row = {
    "city": data["name"],
    "temp": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather": data["weather"][0]["description"],
}
print(row)

print()

row["timestamp"] = datetime.now()

print(row)

df = pd.DataFrame([row])
print(df)

cursor.execute("insert into weather_log (city, temp, humidity, weather, timestamp) values (%s, %s, %s, %s, %s)", (row["city"], row["temp"], row["humidity"], row["weather"], row["timestamp"]))

conn.commit()
conn.close()

logger.info("Row inserted into db successfully")
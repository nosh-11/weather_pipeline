from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import requests
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = Variable.get("API_KEY")
DB_URL = Variable.get("DB_URL")
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

def run_pipeline(**context):
    data = extract()
    row = transform(data)
    load(row)

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="* * * * *",
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="run_pipeline", python_callable=run_pipeline)
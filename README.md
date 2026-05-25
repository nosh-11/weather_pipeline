# Weather Pipeline

A learning exercise to build an end-to-end ETL pipeline using Python, Airflow, and PostgreSQL.

An automated ETL pipeline that fetches real-time weather data for Karachi and loads it into a PostgreSQL database, orchestrated with Apache Airflow.

## Tech Stack
- **Python** — ETL logic
- **Apache Airflow** — orchestration and scheduling
- **PostgreSQL (Neon)** — cloud database
- **psycopg2** — database connectivity
- **OpenWeatherMap API** — weather data source

## Pipeline Architecture
Extract → Transform → Load

1. **Extract** — fetches current weather data from OpenWeatherMap API
2. **Transform** — structures raw JSON into a clean row
3. **Load** — inserts the row into PostgreSQL

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Airflow and add the following variables under Admin → Variables:
   - `API_KEY` — OpenWeatherMap API key
   - `DB_URL` — PostgreSQL connection string
4. Create the table in your database:
```sql
CREATE TABLE weather_log (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    temp FLOAT,
    humidity INT,
    weather VARCHAR(200),
    timestamp TIMESTAMP
);
```
5. Place `weather_dag.py` in your Airflow dags folder
6. Enable the DAG in the Airflow UI

## DAG
- **DAG ID:** `weather_pipeline`
- **Schedule:** Every minute
- **Task:** `run_pipeline` — runs the full ETL in a single task

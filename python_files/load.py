import os
from datetime import date

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

from location import loc
from ingest import extract_daily_weather

load_dotenv()

DDL = """
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.weather_daily (
  city TEXT NOT NULL,
  country TEXT,
  day DATE NOT NULL,
  temp_max DOUBLE PRECISION,
  temp_min DOUBLE PRECISION,
  wind_speed DOUBLE PRECISION,
  PRIMARY KEY (city, day)
);
"""

INSERT_SQL = """
INSERT INTO raw.weather_daily (city, country, day, temp_max, temp_min, wind_speed)
VALUES %s
ON CONFLICT (city, day) DO NOTHING;
"""

def run(initial_backfill_days=1000):
    base_url = os.getenv("url")
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )

    try:
        with conn.cursor() as cur:
            cur.execute(DDL)
        conn.commit()

        today = date.today()

        for city, meta in loc.items():
            with conn.cursor() as cur:
                cur.execute("SELECT MAX(day) FROM raw.weather_daily WHERE city=%s;", (city,))
                (watermark,) = cur.fetchone()

            days_back = initial_backfill_days if watermark is None else max((today - watermark).days, 0)

            if days_back == 0:
                print(f" {city} up-to-date")
                continue

            rows = extract_daily_weather(
                base_url=base_url,
                city=city,
                country=meta.get("country", ""),
                lat=float(meta["lat"]),
                lon=float(meta["lon"]),
                days_back=days_back,
            )

            with conn.cursor() as cur:
                execute_values(cur, INSERT_SQL, rows, page_size=1000)
            conn.commit()

            print(f" {city}: loaded {len(rows)} rows (days_back={days_back})")

    finally:
        conn.close()

if __name__ == "__main__":
    run(1000)
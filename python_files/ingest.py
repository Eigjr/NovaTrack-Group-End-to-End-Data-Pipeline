# ingest.py
import requests
from datetime import date, timedelta
from typing import List, Tuple

DAILY_FIELDS = "temperature_2m_max,temperature_2m_min,wind_speed_10m_max"


def extract_daily_weather(
    base_url: str,
    city: str,
    country: str,
    lat: float,
    lon: float,
    days_back: int = 1000,
) -> List[Tuple[str, str, str, float, float, float]]:
    """
    Extract last N days weather data from REST API.

    Returns rows:
    (city, country, day, temp_max, temp_min, wind_speed)
    """

    #  compute extraction window here
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": DAILY_FIELDS,
        "timezone": "UTC",
    }

    resp = requests.get(base_url, params=params, timeout=30)
    resp.raise_for_status()

    daily = resp.json()["daily"]

    rows = []

    for i, day in enumerate(daily["time"]):
        rows.append(
            (
                city,
                country,
                day,
                daily["temperature_2m_max"][i],
                daily["temperature_2m_min"][i],
                daily["wind_speed_10m_max"][i],
            )
        )

    return rows
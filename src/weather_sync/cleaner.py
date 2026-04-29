from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from .config import CityConfig


def normalize_daily_forecast(raw_data: Dict[str, Any], city: CityConfig) -> List[Dict[str, Any]]:
    """Convert Open-Meteo daily forecast JSON to database-ready records."""
    daily = raw_data.get("daily", {})
    if not daily or "time" not in daily:
        return []

    df = pd.DataFrame(daily)
    if df.empty:
        return []

    rename_map = {
        "time": "weather_date",
        "temperature_2m_max": "temperature_max",
        "temperature_2m_min": "temperature_min",
        "precipitation_sum": "precipitation_sum",
        "wind_speed_10m_max": "wind_speed_max",
    }
    df = df.rename(columns=rename_map)

    required_columns = [
        "weather_date",
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "wind_speed_max",
    ]
    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df = df[required_columns]
    df["city"] = city.name
    df["latitude"] = city.latitude
    df["longitude"] = city.longitude
    df["source"] = "Open-Meteo"

    df["weather_date"] = pd.to_datetime(df["weather_date"], errors="coerce").dt.date
    numeric_columns = ["temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["weather_date"])
    df = df.drop_duplicates(subset=["city", "weather_date"], keep="last")

    return df.to_dict(orient="records")

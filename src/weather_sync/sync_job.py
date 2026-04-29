from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.engine import Engine

from .api_client import OpenMeteoClient
from .cleaner import normalize_daily_forecast
from .config import CityConfig, DEFAULT_CITIES, get_settings
from .db import create_tables, insert_sync_log, upsert_weather_records

logger = logging.getLogger(__name__)


def sync_weather(engine: Engine, cities: Optional[Dict[str, CityConfig]] = None) -> int:
    """Run one weather synchronization task."""
    task_name = "open_meteo_daily_weather_sync"
    start_time = datetime.now()
    settings = get_settings()
    client = OpenMeteoClient(settings)
    target_cities = cities or DEFAULT_CITIES
    synced_count = 0

    try:
        create_tables(engine)
        for city in target_cities.values():
            raw = client.fetch_daily_forecast(city)
            records = normalize_daily_forecast(raw, city)
            count = upsert_weather_records(engine, records)
            synced_count += count
            logger.info("Synced city=%s, rows=%s", city.name, count)

        insert_sync_log(
            engine=engine,
            task_name=task_name,
            start_time=start_time,
            end_time=datetime.now(),
            status="SUCCESS",
            synced_count=synced_count,
        )
        logger.info("Sync task finished successfully, total rows=%s", synced_count)
        return synced_count
    except Exception as exc:
        logger.exception("Sync task failed")
        insert_sync_log(
            engine=engine,
            task_name=task_name,
            start_time=start_time,
            end_time=datetime.now(),
            status="FAILED",
            synced_count=synced_count,
            error_message=str(exc),
        )
        raise

from __future__ import annotations

import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from weather_sync.config import get_settings
from weather_sync.db import get_engine
from weather_sync.sync_job import sync_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def run_scheduler() -> None:
    settings = get_settings()
    engine = get_engine(settings.database_url)
    scheduler = BlockingScheduler(timezone=settings.app_timezone)

    scheduler.add_job(
        sync_weather,
        trigger="cron",
        hour=settings.schedule_hour,
        minute=settings.schedule_minute,
        args=[engine],
        id="open_meteo_daily_weather_sync",
        replace_existing=True,
    )

    logging.info(
        "Scheduler started. Daily sync time: %02d:%02d %s",
        settings.schedule_hour,
        settings.schedule_minute,
        settings.app_timezone,
    )
    scheduler.start()


if __name__ == "__main__":
    run_scheduler()

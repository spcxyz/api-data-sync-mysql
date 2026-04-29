from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class CityConfig:
    name: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Settings:
    database_url: str
    open_meteo_base_url: str
    app_timezone: str
    forecast_days: int
    request_timeout: int
    schedule_hour: int
    schedule_minute: int


DEFAULT_CITIES: Dict[str, CityConfig] = {
    "武汉": CityConfig(name="武汉", latitude=30.5928, longitude=114.3055),
    "北京": CityConfig(name="北京", latitude=39.9042, longitude=116.4074),
    "上海": CityConfig(name="上海", latitude=31.2304, longitude=121.4737),
    "广州": CityConfig(name="广州", latitude=23.1291, longitude=113.2644),
}


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://root:root@localhost:3306/weather_sync?charset=utf8mb4",
        ),
        open_meteo_base_url=os.getenv(
            "OPEN_METEO_BASE_URL",
            "https://api.open-meteo.com/v1/forecast",
        ),
        app_timezone=os.getenv("APP_TIMEZONE", "Asia/Shanghai"),
        forecast_days=int(os.getenv("FORECAST_DAYS", "7")),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "10")),
        schedule_hour=int(os.getenv("SCHEDULE_HOUR", "8")),
        schedule_minute=int(os.getenv("SCHEDULE_MINUTE", "30")),
    )

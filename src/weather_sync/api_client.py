from __future__ import annotations

import logging
from typing import Any, Dict

import requests

from .config import CityConfig, Settings

logger = logging.getLogger(__name__)


class OpenMeteoClient:
    """Simple client for Open-Meteo Forecast API."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def fetch_daily_forecast(self, city: CityConfig) -> Dict[str, Any]:
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "forecast_days": self.settings.forecast_days,
            "timezone": self.settings.app_timezone,
        }
        logger.info("Fetching Open-Meteo data: city=%s, params=%s", city.name, params)
        response = requests.get(
            self.settings.open_meteo_base_url,
            params=params,
            timeout=self.settings.request_timeout,
        )
        response.raise_for_status()
        data = response.json()
        if "daily" not in data:
            raise ValueError(f"Open-Meteo response has no daily field: {data}")
        return data

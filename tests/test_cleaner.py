from weather_sync.cleaner import normalize_daily_forecast
from weather_sync.config import CityConfig


def test_normalize_daily_forecast():
    raw = {
        "daily": {
            "time": ["2026-04-29", "2026-04-30"],
            "temperature_2m_max": [25.2, 26.1],
            "temperature_2m_min": [15.8, 16.4],
            "precipitation_sum": [0.0, 1.2],
            "wind_speed_10m_max": [12.5, 10.4],
        }
    }
    city = CityConfig(name="武汉", latitude=30.5928, longitude=114.3055)
    records = normalize_daily_forecast(raw, city)

    assert len(records) == 2
    assert records[0]["city"] == "武汉"
    assert records[0]["temperature_max"] == 25.2
    assert str(records[0]["weather_date"]) == "2026-04-29"

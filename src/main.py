from __future__ import annotations

import logging

from weather_sync.config import get_settings
from weather_sync.db import get_engine
from weather_sync.sync_job import sync_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main() -> None:
    settings = get_settings()
    engine = get_engine(settings.database_url)
    count = sync_weather(engine)
    print(f"Sync finished. Rows affected: {count}")


if __name__ == "__main__":
    main()

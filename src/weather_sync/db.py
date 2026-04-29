from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    desc,
    select,
)
from sqlalchemy.engine import Engine
from sqlalchemy.sql import func

metadata = MetaData()

weather_daily = Table(
    "weather_daily",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("city", String(50), nullable=False),
    Column("latitude", Numeric(10, 6)),
    Column("longitude", Numeric(10, 6)),
    Column("weather_date", Date, nullable=False),
    Column("temperature_max", Numeric(6, 2)),
    Column("temperature_min", Numeric(6, 2)),
    Column("precipitation_sum", Numeric(8, 2)),
    Column("wind_speed_max", Numeric(8, 2)),
    Column("source", String(50), default="Open-Meteo"),
    Column("created_time", DateTime, server_default=func.now()),
    Column("updated_time", DateTime, server_default=func.now(), onupdate=func.now()),
    UniqueConstraint("city", "weather_date", name="uk_city_date"),
)

sync_log = Table(
    "sync_log",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("task_name", String(100), nullable=False),
    Column("start_time", DateTime, nullable=False),
    Column("end_time", DateTime),
    Column("status", String(20), nullable=False),
    Column("synced_count", Integer, default=0),
    Column("error_message", Text),
    Column("created_time", DateTime, server_default=func.now()),
)


def get_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True, future=True)


def create_tables(engine: Engine) -> None:
    metadata.create_all(engine)


def upsert_weather_records(engine: Engine, records: Iterable[Dict[str, Any]]) -> int:
    records_list = list(records)
    if not records_list:
        return 0

    dialect = engine.dialect.name
    now = datetime.now()
    for record in records_list:
        record["updated_time"] = now

    with engine.begin() as conn:
        if dialect == "mysql":
            from sqlalchemy.dialects.mysql import insert as mysql_insert

            stmt = mysql_insert(weather_daily).values(records_list)
            update_columns = {
                "latitude": stmt.inserted.latitude,
                "longitude": stmt.inserted.longitude,
                "temperature_max": stmt.inserted.temperature_max,
                "temperature_min": stmt.inserted.temperature_min,
                "precipitation_sum": stmt.inserted.precipitation_sum,
                "wind_speed_max": stmt.inserted.wind_speed_max,
                "source": stmt.inserted.source,
                "updated_time": now,
            }
            conn.execute(stmt.on_duplicate_key_update(**update_columns))
        elif dialect == "sqlite":
            from sqlalchemy.dialects.sqlite import insert as sqlite_insert

            stmt = sqlite_insert(weather_daily).values(records_list)
            update_columns = {
                "latitude": stmt.excluded.latitude,
                "longitude": stmt.excluded.longitude,
                "temperature_max": stmt.excluded.temperature_max,
                "temperature_min": stmt.excluded.temperature_min,
                "precipitation_sum": stmt.excluded.precipitation_sum,
                "wind_speed_max": stmt.excluded.wind_speed_max,
                "source": stmt.excluded.source,
                "updated_time": now,
            }
            conn.execute(
                stmt.on_conflict_do_update(
                    index_elements=["city", "weather_date"],
                    set_=update_columns,
                )
            )
        else:
            conn.execute(weather_daily.insert(), records_list)

    return len(records_list)


def insert_sync_log(
    engine: Engine,
    task_name: str,
    start_time: datetime,
    end_time: datetime,
    status: str,
    synced_count: int,
    error_message: Optional[str] = None,
) -> None:
    with engine.begin() as conn:
        conn.execute(
            sync_log.insert().values(
                task_name=task_name,
                start_time=start_time,
                end_time=end_time,
                status=status,
                synced_count=synced_count,
                error_message=error_message,
            )
        )


def query_latest_weather(engine: Engine, city: str) -> Optional[Dict[str, Any]]:
    stmt = (
        select(weather_daily)
        .where(weather_daily.c.city == city)
        .order_by(desc(weather_daily.c.weather_date))
        .limit(1)
    )
    with engine.connect() as conn:
        row = conn.execute(stmt).mappings().first()
        return dict(row) if row else None


def query_weather_range(
    engine: Engine,
    city: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    stmt = select(weather_daily).where(weather_daily.c.city == city)
    if start_date:
        stmt = stmt.where(weather_daily.c.weather_date >= start_date)
    if end_date:
        stmt = stmt.where(weather_daily.c.weather_date <= end_date)
    stmt = stmt.order_by(weather_daily.c.weather_date)

    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(stmt).mappings().all()]


def query_sync_logs(engine: Engine, limit: int = 10) -> List[Dict[str, Any]]:
    stmt = select(sync_log).order_by(desc(sync_log.c.start_time)).limit(limit)
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(stmt).mappings().all()]

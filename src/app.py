from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query

from weather_sync.config import get_settings
from weather_sync.db import (
    create_tables,
    get_engine,
    query_latest_weather,
    query_sync_logs,
    query_weather_range,
)

settings = get_settings()
engine = get_engine(settings.database_url)
create_tables(engine)

app = FastAPI(title="API Data Sync MySQL Demo", version="1.0.0")


def serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, (date, datetime)):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "api-data-sync-mysql"}


@app.get("/weather/latest")
def latest_weather(city: str = Query(..., description="城市名称，例如：武汉")) -> Dict[str, Any]:
    row = query_latest_weather(engine, city)
    if not row:
        raise HTTPException(status_code=404, detail=f"No weather data found for city={city}")
    return serialize_row(row)


@app.get("/weather")
def weather_range(
    city: str = Query(..., description="城市名称，例如：武汉"),
    start_date: Optional[str] = Query(None, description="开始日期，格式 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式 YYYY-MM-DD"),
) -> List[Dict[str, Any]]:
    rows = query_weather_range(engine, city=city, start_date=start_date, end_date=end_date)
    return [serialize_row(row) for row in rows]


@app.get("/sync/logs")
def sync_logs(limit: int = Query(10, ge=1, le=100)) -> List[Dict[str, Any]]:
    rows = query_sync_logs(engine, limit=limit)
    return [serialize_row(row) for row in rows]

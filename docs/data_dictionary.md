# 数据字典

## weather_daily：每日天气数据表

| 字段名 | 类型 | 说明 | 备注 |
|---|---|---|---|
| id | BIGINT | 主键 ID | 自增 |
| city | VARCHAR(50) | 城市名称 | 与 weather_date 组成唯一索引 |
| latitude | DECIMAL(10,6) | 纬度 | API 请求参数 |
| longitude | DECIMAL(10,6) | 经度 | API 请求参数 |
| weather_date | DATE | 天气日期 | 与 city 组成唯一索引 |
| temperature_max | DECIMAL(6,2) | 最高气温 | 单位：摄氏度 |
| temperature_min | DECIMAL(6,2) | 最低气温 | 单位：摄氏度 |
| precipitation_sum | DECIMAL(8,2) | 降水量合计 | 单位：mm |
| wind_speed_max | DECIMAL(8,2) | 最大风速 | 单位：km/h |
| source | VARCHAR(50) | 数据来源 | 默认 Open-Meteo |
| created_time | DATETIME | 创建时间 | 默认当前时间 |
| updated_time | DATETIME | 更新时间 | 更新时自动刷新 |

唯一索引：`uk_city_date(city, weather_date)`，用于避免同一城市同一天的数据重复写入。

## sync_log：同步日志表

| 字段名 | 类型 | 说明 | 备注 |
|---|---|---|---|
| id | BIGINT | 主键 ID | 自增 |
| task_name | VARCHAR(100) | 任务名称 | 如 open_meteo_daily_weather_sync |
| start_time | DATETIME | 任务开始时间 | 必填 |
| end_time | DATETIME | 任务结束时间 | 任务结束后写入 |
| status | VARCHAR(20) | 任务状态 | SUCCESS / FAILED |
| synced_count | INT | 同步条数 | 每次任务写入或更新的数据条数 |
| error_message | TEXT | 异常信息 | 失败时记录 |
| created_time | DATETIME | 创建时间 | 默认当前时间 |

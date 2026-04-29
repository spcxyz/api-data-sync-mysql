# API 字段映射说明

## 数据源

Open-Meteo Forecast API：`https://api.open-meteo.com/v1/forecast`

## 请求参数

| 参数 | 示例 | 说明 |
|---|---|---|
| latitude | 30.5928 | 城市纬度 |
| longitude | 114.3055 | 城市经度 |
| daily | temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max | 每日天气变量 |
| forecast_days | 7 | 预测天数 |
| timezone | Asia/Shanghai | 时区 |

## 返回字段到数据库字段的映射

| API 返回字段 | 数据库字段 | 清洗方式 |
|---|---|---|
| daily.time | weather_date | 转换为 DATE |
| daily.temperature_2m_max | temperature_max | 转换为数值 |
| daily.temperature_2m_min | temperature_min | 转换为数值 |
| daily.precipitation_sum | precipitation_sum | 转换为数值 |
| daily.wind_speed_10m_max | wind_speed_max | 转换为数值 |
| 城市配置 name | city | 字段补充 |
| 城市配置 latitude | latitude | 字段补充 |
| 城市配置 longitude | longitude | 字段补充 |
| 固定值 Open-Meteo | source | 字段补充 |

## 数据质量处理

- 日期字段使用 `pandas.to_datetime` 统一格式。
- 数值字段使用 `pandas.to_numeric` 转换，无法转换时置为空。
- 丢弃日期为空的数据。
- 按 `city + weather_date` 去重，保留最后一条。

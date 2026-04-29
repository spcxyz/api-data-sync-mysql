# 第三方 API 数据同步与 MySQL 入库系统

> 项目实现了从第三方 API 拉取数据、清洗标准化、写入 MySQL、记录同步日志、提供查询接口、使用 Postman 测试的完整链路。

## 1. 项目背景

在业务数据分析或数据平台建设中，常见问题包括：第三方 API 返回字段不统一、人工同步效率低、入库过程缺少运行记录、接口数据异常不易排查。该项目以 Open-Meteo 天气数据为示例，构建一个可复用的数据同步流程，用于展示 API 对接、JSON 解析、数据清洗、数据库入库、定时任务和接口封装能力。

## 2. 技术栈

- Python：requests、pandas、logging、python-dotenv
- 数据库：MySQL、SQLAlchemy、PyMySQL
- 定时任务：APScheduler
- API 服务：FastAPI、Uvicorn
- 接口测试：Postman / Apifox
- 数据源：Open-Meteo Forecast API

## 3. 系统流程

```text
第三方 API 数据拉取
        ↓
JSON 返回结果解析
        ↓
字段清洗、缺失值处理、日期格式标准化
        ↓
MySQL 批量入库 / 增量更新 / 唯一索引去重
        ↓
同步日志记录：开始时间、结束时间、状态、同步条数、异常信息
        ↓
FastAPI 查询接口
        ↓
Postman 接口测试与结果校验
```

## 4. 核心功能

1. **API 数据拉取**：基于 `requests` 调用 Open-Meteo API，支持城市坐标、天气变量、时区、预测天数等参数封装。
2. **数据清洗与标准化**：使用 `pandas` 处理字段筛选、字段重命名、日期格式转换、数值类型转换和缺失值。
3. **MySQL 入库与去重**：基于 `SQLAlchemy` 写入 MySQL，设置 `city + weather_date` 唯一索引，避免重复写入。
4. **同步日志记录**：设计 `sync_log` 表，记录任务运行状态、同步条数和异常信息，便于排查问题。
5. **定时任务调度**：使用 `APScheduler` 支持每日自动同步，模拟企业中的数据同步任务。
6. **接口封装与测试**：使用 `FastAPI` 提供健康检查、最新天气、历史天气和同步日志查询接口。

## 5. 项目目录

```text
api-data-sync-mysql
├── README.md
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── sql
│   └── init.sql
├── src
│   ├── app.py
│   ├── main.py
│   ├── scheduler.py
│   └── weather_sync
│       ├── __init__.py
│       ├── api_client.py
│       ├── cleaner.py
│       ├── config.py
│       ├── db.py
│       └── sync_job.py
├── docs
│   ├── api_mapping.md
│   ├── data_dictionary.md
│   ├── interview_notes.md
│   └── resume_points.md
└── tests
    └── test_cleaner.py
```

## 6. 快速启动

### 6.1 启动 MySQL

```bash
docker compose up -d mysql
```

或使用本地 MySQL，创建数据库：

```sql
CREATE DATABASE weather_sync DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6.2 安装依赖

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 6.3 配置环境变量

复制 `.env.example` 为 `.env`，按需修改数据库连接：

```bash
cp .env.example .env
```

默认配置：

```text
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/weather_sync?charset=utf8mb4
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast
APP_TIMEZONE=Asia/Shanghai
```

### 6.4 初始化并同步数据

```bash
python -m src.main
```

运行后会自动建表，并同步默认城市的未来 7 天天气数据。

### 6.5 启动接口服务

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

## 7. API 接口说明

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| GET | `/weather/latest?city=武汉` | 查询指定城市最新天气 |
| GET | `/weather?city=武汉&start_date=2026-04-29&end_date=2026-05-05` | 按城市与日期范围查询天气 |
| GET | `/sync/logs?limit=10` | 查询最近同步日志 |

## 8. 数据表说明

项目包含两张核心表：

- `weather_daily`：存储每日天气数据。
- `sync_log`：记录每次同步任务的运行状态。

详细字段见：`docs/data_dictionary.md`。

## 9. Postman 测试建议

建议保存以下截图，用于 README 或面试展示：

1. `/health` 返回 `ok` 的截图。
2. `/weather/latest?city=武汉` 返回最新天气的截图。
3. `/sync/logs` 返回同步日志的截图。
4. MySQL 中 `weather_daily` 和 `sync_log` 表有数据的截图。
5. 终端日志中显示同步条数和运行状态的截图。

## 10. 后续可扩展方向

- 增加失败重试次数配置与邮件/企业微信告警。
- 支持更多第三方 API 数据源，例如空气质量、股票行情、招聘信息等。
- 增加 Dockerfile，实现项目一键部署。
- 增加数据质量校验规则，例如空值率、重复率、日期连续性检查。

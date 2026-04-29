# 简历项目描述

## 第三方 API 数据同步与 MySQL 入库系统

技术栈：Python、requests、pandas、MySQL、SQLAlchemy、APScheduler、FastAPI、Postman

- 基于 Python requests 对接第三方公开 API，完成接口参数封装、JSON 数据解析、请求超时处理和异常捕获，提升数据获取流程的稳定性。
- 使用 pandas 对原始数据进行字段筛选、字段命名标准化、缺失值处理、日期格式转换和重复数据去重，形成可直接入库的结构化数据。
- 设计 MySQL 天气数据表与同步日志表，使用 SQLAlchemy 实现批量入库和增量更新，并通过 `city + weather_date` 唯一索引避免重复写入。
- 使用 APScheduler 配置定时同步任务，记录任务开始时间、结束时间、同步条数、运行状态和异常信息，便于后续排查问题。
- 基于 FastAPI 封装健康检查、天气查询、同步日志查询等接口，并使用 Postman 完成参数校验和返回结果检查。

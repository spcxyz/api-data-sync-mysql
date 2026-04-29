CREATE DATABASE IF NOT EXISTS weather_sync DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE weather_sync;

CREATE TABLE IF NOT EXISTS weather_daily (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL COMMENT '城市名称',
    latitude DECIMAL(10, 6) COMMENT '纬度',
    longitude DECIMAL(10, 6) COMMENT '经度',
    weather_date DATE NOT NULL COMMENT '天气日期',
    temperature_max DECIMAL(6, 2) COMMENT '最高气温',
    temperature_min DECIMAL(6, 2) COMMENT '最低气温',
    precipitation_sum DECIMAL(8, 2) COMMENT '降水量合计',
    wind_speed_max DECIMAL(8, 2) COMMENT '最大风速',
    source VARCHAR(50) DEFAULT 'Open-Meteo' COMMENT '数据来源',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_city_date (city, weather_date),
    INDEX idx_city_date (city, weather_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日天气数据表';

CREATE TABLE IF NOT EXISTS sync_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_name VARCHAR(100) NOT NULL COMMENT '任务名称',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    status VARCHAR(20) NOT NULL COMMENT '运行状态：SUCCESS/FAILED/RUNNING',
    synced_count INT DEFAULT 0 COMMENT '同步条数',
    error_message TEXT COMMENT '异常信息',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_task_time (task_name, start_time),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据同步日志表';

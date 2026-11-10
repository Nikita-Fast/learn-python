
-- Создание таблицы проверяемых параметров
CREATE TABLE IF NOT EXISTS parameters (
     id INTEGER PRIMARY KEY,
     name TEXT NOT NULL UNIQUE,
     unit TEXT NOT NULL DEFAULT '',
     min_value REAL DEFAULT NULL,
     max_value REAL DEFAULT NULL,
     validation_type TEXT CHECK (validation_type IN ('range', '<=', '>=', 'none')) DEFAULT 'none'
);


-- Создание таблицы, определяющей для каких каналов ППМ (ppsm) выполняется проверка каждого параметра
-- Если для параметра нет ни одной записи в таблицы, то такой параметр проверяется не на конкретном канале (ppsm),
-- а для всего ППМ, например, параметр Потребляемый ток
CREATE TABLE parameter_ppm_channels (
    parameter_id INTEGER NOT NULL,
    ppsm INTEGER NOT NULL CHECK (ppsm BETWEEN 1 AND 16),
    PRIMARY KEY (parameter_id, ppsm),
    FOREIGN KEY (parameter_id) REFERENCES parameters (id) ON DELETE CASCADE
);


-- Создание таблицы конфигураций измерительных каналов АИВК
CREATE TABLE IF NOT EXISTS measurement_channel_configs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    -- параметры ППМ
    ppsm INTEGER NOT NULL CHECK (ppsm BETWEEN 1 AND 16),
    ppsm_mode TEXT NOT NULL CHECK (ppsm_mode IN ('rx', 'tx')),
    -- параметры ZNA26
    rbw_hz INTEGER NOT NULL CHECK (rbw_hz BETWEEN 1 AND 30_000_000),
    source_level_dbm REAL NOT NULL CHECK (source_level_dbm BETWEEN -120 AND 30),
    calibration_file_name TEXT,
    -- произвольный набор частот до 50001 точек
    freq_points NDARRAY,
    -- К-18
    commutations TEXT -- конфигурация реле в формате JSON
);


CREATE TABLE IF NOT EXISTS raw.weather_hourly (
    id              BIGSERIAL PRIMARY KEY,
    city            TEXT        NOT NULL,
    latitude        NUMERIC(9,4) NOT NULL,
    longitude       NUMERIC(9,4) NOT NULL,
    observed_at     TIMESTAMP   NOT NULL,
    temperature_c   NUMERIC(5,2),
    humidity_pct    NUMERIC(5,2),
    windspeed_kmh   NUMERIC(6,2),
    weathercode     INTEGER,
    source          TEXT        NOT NULL DEFAULT 'open-meteo',
    load_type       TEXT        NOT NULL,
    loaded_at       TIMESTAMP   NOT NULL DEFAULT now(),
    CONSTRAINT uq_city_observed UNIQUE (city, observed_at)
);

CREATE INDEX IF NOT EXISTS idx_weather_city_date
    ON raw.weather_hourly (city, observed_at);

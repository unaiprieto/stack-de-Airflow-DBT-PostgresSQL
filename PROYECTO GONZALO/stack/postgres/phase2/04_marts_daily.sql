DROP TABLE IF EXISTS marts.weather_daily_avg;

CREATE TABLE marts.weather_daily_avg AS
SELECT
    city,
    observed_at::date              AS day,
    ROUND(AVG(temperature_c), 2)   AS avg_temperature_c,
    ROUND(AVG(humidity_pct), 2)    AS avg_humidity_pct,
    ROUND(AVG(windspeed_kmh), 2)   AS avg_windspeed_kmh,
    COUNT(*)                       AS num_readings
FROM staging.vw_weather_clean
GROUP BY city, observed_at::date
ORDER BY city, day;

ALTER TABLE marts.weather_daily_avg
    ADD PRIMARY KEY (city, day);

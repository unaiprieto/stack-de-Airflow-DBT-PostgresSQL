
DROP TABLE IF EXISTS marts.weather_hourly_pattern;

CREATE TABLE marts.weather_hourly_pattern AS
SELECT
    city,
    EXTRACT(HOUR FROM observed_at)::int AS hour_of_day,
    ROUND(AVG(temperature_c), 2)        AS avg_temperature_c,
    ROUND(AVG(humidity_pct), 2)         AS avg_humidity_pct,
    ROUND(AVG(windspeed_kmh), 2)        AS avg_windspeed_kmh,
    COUNT(*)                            AS num_readings
FROM staging.vw_weather_clean
GROUP BY city, EXTRACT(HOUR FROM observed_at)
ORDER BY city, hour_of_day;

ALTER TABLE marts.weather_hourly_pattern
    ADD PRIMARY KEY (city, hour_of_day);

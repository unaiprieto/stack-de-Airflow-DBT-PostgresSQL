SELECT
    city,
    observed_at::date            AS day,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(AVG(humidity_pct), 2)  AS avg_humidity_pct,
    ROUND(AVG(windspeed_kmh), 2) AS avg_windspeed_kmh,
    COUNT(*)                     AS num_readings
FROM {{ ref('stg_weather') }}
GROUP BY city, observed_at::date

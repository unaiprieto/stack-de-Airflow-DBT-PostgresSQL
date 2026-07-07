SELECT DISTINCT
    INITCAP(TRIM(city))  AS city,
    latitude,
    longitude,
    observed_at,
    temperature_c,
    humidity_pct,
    windspeed_kmh,
    weathercode,
    load_type
FROM {{ source('raw', 'weather_hourly') }}
WHERE temperature_c IS NOT NULL

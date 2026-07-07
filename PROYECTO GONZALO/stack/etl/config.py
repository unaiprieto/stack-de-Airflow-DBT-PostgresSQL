import os

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "stack_db")
DB_USER = os.getenv("DB_USER", "stack_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "stack_pass")

LOAD_INTERVAL_MINUTES = int(os.getenv("LOAD_INTERVAL_MINUTES", "15"))

CITIES = [
    {"name": "Madrid",    "lat": 40.4168, "lon": -3.7038},
    {"name": "Salamanca", "lat": 40.9701, "lon": -5.6635},
    {"name": "Barcelona", "lat": 41.3874, "lon": 2.1686},
]

INITIAL_LOAD_DAYS = int(os.getenv("INITIAL_LOAD_DAYS", "7"))

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

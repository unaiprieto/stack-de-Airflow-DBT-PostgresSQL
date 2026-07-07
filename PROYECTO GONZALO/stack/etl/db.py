import time
import psycopg2
from psycopg2.extras import execute_values

import config


def get_connection(retries: int = 20, delay: int = 3):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
            )
            print(f"[db] Conectado a Postgres (intento {attempt})")
            return conn
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"[db] Postgres no disponible aún (intento {attempt}/{retries}): {e}")
            time.sleep(delay)
    raise last_error


def insert_weather_rows(conn, rows, load_type: str):
    if not rows:
        print("[db] No hay filas nuevas que insertar.")
        return 0

    query = """
        INSERT INTO raw.weather_hourly
            (city, latitude, longitude, observed_at, temperature_c,
             humidity_pct, windspeed_kmh, weathercode, source, load_type)
        VALUES %s
        ON CONFLICT (city, observed_at) DO NOTHING
    """

    values = [
        (
            r["city"], r["lat"], r["lon"], r["observed_at"],
            r.get("temperature_c"), r.get("humidity_pct"),
            r.get("windspeed_kmh"), r.get("weathercode"),
            "open-meteo", load_type,
        )
        for r in rows
    ]

    with conn.cursor() as cur:
        execute_values(cur, query, values)
        inserted = cur.rowcount
    conn.commit()
    print(f"[db] Insertadas/actualizadas {len(values)} filas (load_type={load_type}).")
    return inserted

"""
JOB 1 - Carga inicial (histórica)
"""
import datetime as dt
import requests

import config
import db


def fetch_historical(city: dict, days: int) -> list[dict]:
    end_date = dt.date.today()
    start_date = end_date - dt.timedelta(days=days)

    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    resp = requests.get(config.OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    hums = hourly.get("relative_humidity_2m", [])
    winds = hourly.get("wind_speed_10m", [])
    codes = hourly.get("weather_code", [])

    rows = []
    for i, t in enumerate(times):
        rows.append({
            "city": city["name"],
            "lat": city["lat"],
            "lon": city["lon"],
            "observed_at": t.replace("T", " "),
            "temperature_c": temps[i] if i < len(temps) else None,
            "humidity_pct": hums[i] if i < len(hums) else None,
            "windspeed_kmh": winds[i] if i < len(winds) else None,
            "weathercode": codes[i] if i < len(codes) else None,
        })
    return rows


def run():
    print(f"[first_load] Iniciando carga histórica ({config.INITIAL_LOAD_DAYS} días)...")
    conn = db.get_connection()
    try:
        for city in config.CITIES:
            print(f"[first_load] Descargando histórico de {city['name']}...")
            rows = fetch_historical(city, config.INITIAL_LOAD_DAYS)
            db.insert_weather_rows(conn, rows, load_type="initial")
    finally:
        conn.close()
    print("[first_load] Carga inicial completada.")


if __name__ == "__main__":
    run()

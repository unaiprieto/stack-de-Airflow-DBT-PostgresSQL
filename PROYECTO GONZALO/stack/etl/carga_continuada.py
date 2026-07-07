"""
JOB 2 - Carga continuada (incremental)
Hace UNA ejecución de la carga incremental y termina.
El disparo periódico lo gestionará el orquestador (pendiente de añadir).
"""
import requests

import config
import db


def fetch_current(city: dict) -> list[dict]:
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "forecast_days": 1,
        "timezone": "auto",
    }

    resp = requests.get(config.OPEN_METEO_FORECAST_URL, params=params, timeout=30)
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
    print("[carga_continuada] Ejecutando carga incremental...")
    conn = db.get_connection()
    try:
        for city in config.CITIES:
            rows = fetch_current(city)
            db.insert_weather_rows(conn, rows, load_type="incremental")
    finally:
        conn.close()
    print("[carga_continuada] Carga incremental completada.")


if __name__ == "__main__":
    run()

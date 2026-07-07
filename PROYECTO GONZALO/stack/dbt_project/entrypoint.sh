#!/bin/bash
set -e

echo "=== dbt run: crea la vista en staging y las tablas en marts ==="
dbt run --profiles-dir /app --project-dir /app

echo "=== dbt docs generate: genera la documentacion ==="
dbt docs generate --profiles-dir /app --project-dir /app

echo "=== dbt docs serve: levanta la UI en el puerto 8081 ==="
exec dbt docs serve --profiles-dir /app --project-dir /app --host 0.0.0.0 --port 8081

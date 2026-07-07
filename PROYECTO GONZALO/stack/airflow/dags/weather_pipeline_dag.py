from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# IMPORTANTE: ajusta estos dos nombres si en tu docker images / docker network ls
# salen distintos a los que se ven aquí.
DOCKER_NETWORK = "stack_datanet"
ETL_IMAGE = "stack-etl"
DBT_IMAGE = "stack-dbt"

default_args = {
    "owner": "jonan",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="weather_pipeline",
    description="Carga incremental (etl) + refresco de staging/marts (dbt)",
    default_args=default_args,
    schedule_interval="*/15 * * * *",   # cada 15 minutos
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["weather", "etl", "dbt"],
) as dag:

    carga_continuada = BashOperator(
        task_id="carga_continuada",
        bash_command=(
            f"docker run --rm --network {DOCKER_NETWORK} "
            f"-e DB_HOST=db -e DB_PORT=5432 -e DB_NAME=stack_db "
            f"-e DB_USER=stack_user -e DB_PASSWORD=stack_pass "
            f"--entrypoint python {ETL_IMAGE} carga_continuada.py"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"docker run --rm --network {DOCKER_NETWORK} "
            f"--entrypoint dbt {DBT_IMAGE} run "
            f"--profiles-dir /app --project-dir /app"
        ),
    )

    carga_continuada >> dbt_run

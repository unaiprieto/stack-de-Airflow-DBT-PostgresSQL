FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir dbt-core dbt-postgres

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8081

ENTRYPOINT ["./entrypoint.sh"]

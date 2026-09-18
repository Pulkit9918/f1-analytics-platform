FROM apache/airflow:2.9.3-python3.11

USER airflow
RUN pip install --no-cache-dir \
    "click==8.2.1" \
    requests \
    pandas \
    fastf1 \
    "snowflake-connector-python[pandas]" \
    dbt-snowflake
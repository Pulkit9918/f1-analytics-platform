# Airflow DAG for F1 data ingestion and transformation using dbt.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import sys
sys.path.append("/opt/airflow/ingestion")

from jolpica_client import get_races, get_results, get_qualifying, get_pit_stops, get_drivers, get_constructors
from fastf1_client import get_laps, get_stints
from snowflake_loader import load_df

SEASON = 2024
ROUND = 1

def ingest_race_results():
    load_df(get_races(SEASON), "races")
    load_df(get_results(SEASON, ROUND), "results")
    load_df(get_qualifying(SEASON, ROUND), "qualifying")
    load_df(get_pit_stops(SEASON, ROUND), "pit_stops")
    load_df(get_drivers(SEASON), "drivers")
    load_df(get_constructors(SEASON), "constructors")

def ingest_telemetry():
    load_df(get_laps(SEASON, ROUND), "laps")
    load_df(get_stints(SEASON, ROUND), "stints")

def run_dbt_command():
    result = subprocess.run(
        [
            "dbt", "run",
            "--project-dir", "/opt/airflow/dbt_project",
            "--profiles-dir", "/opt/airflow/dbt_project"
        ],
        check=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    return result.returncode

with DAG(
    dag_id="f1_ingestion_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@weekly",
    catchup=False,
    tags=["f1", "ingestion"]
) as dag:

    race_results_task = PythonOperator(
        task_id="ingest_race_results",
        python_callable=ingest_race_results
    )

    telemetry_task = PythonOperator(
        task_id="ingest_telemetry",
        python_callable=ingest_telemetry
    )

    dbt_run_task = PythonOperator(
        task_id="run_dbt",
        python_callable=run_dbt_command
    )

    [race_results_task, telemetry_task] >> dbt_run_task
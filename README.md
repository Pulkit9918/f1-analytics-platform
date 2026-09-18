**Live Dashboard:** https://f1-analytics-platform-s2.streamlit.app

# F1 Race Strategy & Performance Analytics Platform

An end-to-end data platform ingesting Formula 1 timing and results data,
orchestrated by Airflow (Dockerized), transformed through a dbt/Snowflake
warehouse, with automated tests.

## Architecture
Jolpica-F1 API (results, qualifying, pit stops) + FastF1 (lap times, tire
stints) -> Airflow (Dockerized) -> Snowflake RAW -> dbt staging/intermediate/marts.

## Marts
- mart_qualifying_vs_race_pace - grid vs finish position deltas
- mart_tire_stint_performance - lap time degradation per compound
- mart_pit_stop_efficiency - stop duration vs race outcome
- mart_championship_progression - cumulative points per driver per season

## Stack
Python, Airflow, Docker, Snowflake, dbt

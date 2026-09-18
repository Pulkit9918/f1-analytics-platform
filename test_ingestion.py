from ingestion.jolpica_client import get_races, get_results, get_qualifying, get_pit_stops, get_drivers, get_constructors
from ingestion.fastf1_client import get_laps, get_stints
from ingestion.snowflake_loader import load_df
import pandas as pd

season = 2024
rounds_to_load = range(1, 6)  

load_df(get_races(season), "races")
load_df(get_drivers(season), "drivers")
load_df(get_constructors(season), "constructors")

all_results, all_qualifying, all_pit_stops, all_laps, all_stints = [], [], [], [], []

for round_ in rounds_to_load:
    print(f"Fetching round {round_}...")
    all_results.append(get_results(season, round_))
    all_qualifying.append(get_qualifying(season, round_))
    all_pit_stops.append(get_pit_stops(season, round_))
    all_laps.append(get_laps(season, round_))
    all_stints.append(get_stints(season, round_))

load_df(pd.concat(all_results, ignore_index=True), "results")
load_df(pd.concat(all_qualifying, ignore_index=True), "qualifying")
load_df(pd.concat(all_pit_stops, ignore_index=True), "pit_stops")
load_df(pd.concat(all_laps, ignore_index=True), "laps")
load_df(pd.concat(all_stints, ignore_index=True), "stints")
from ingestion.jolpica_client import get_races, get_results, get_qualifying, get_pit_stops, get_drivers, get_constructors
from ingestion.fastf1_client import get_laps, get_stints
from ingestion.snowflake_loader import load_df

season, round_ = 2024, 1

load_df(get_races(season), "races")
load_df(get_results(season, round_), "results")
load_df(get_qualifying(season, round_), "qualifying")
load_df(get_pit_stops(season, round_), "pit_stops")
load_df(get_drivers(season), "drivers")
load_df(get_constructors(season), "constructors")
load_df(get_laps(season, round_), "laps")
load_df(get_stints(season, round_), "stints")
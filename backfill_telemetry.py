from ingestion.fastf1_client import get_laps, get_stints
from ingestion.snowflake_loader import load_df
from ingestion.jolpica_client import get_races
import pandas as pd

TELEMETRY_TARGETS = {
    2025: None,
    2024: [1, 12, 24],
    2023: [1, 12, 22],
}

all_laps, all_stints = [], []

for season, rounds in TELEMETRY_TARGETS.items():
    if rounds is None:
        rounds = range(1, len(get_races(season)) + 1)
    for round_ in rounds:
        print(f"Fetching telemetry: {season} round {round_}...")
        try:
            all_laps.append(get_laps(season, round_))
            all_stints.append(get_stints(season, round_))
        except Exception as e:
            print(f"  Skipped {season} round {round_}: {e}")

load_df(pd.concat(all_laps, ignore_index=True), "laps")
load_df(pd.concat(all_stints, ignore_index=True), "stints")

print("Telemetry backfill complete.")
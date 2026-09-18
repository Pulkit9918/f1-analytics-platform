"""Pulls lap-by-lap timing, tire stints, and telemetry via FastF1
(official F1 timing data, same source broadcasters use)."""

import fastf1
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "fastf1_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))


def get_laps(season: int, round_: int) -> pd.DataFrame:
    session = fastf1.get_session(season, round_, "R")  # 'R' = Race
    session.load(laps=True, telemetry=False, weather=False)
    laps = session.laps

    rows = []
    for _, lap in laps.iterrows():
        rows.append({
            "season": season,
            "round": round_,
            "driver_id": lap["Driver"],
            "lap_number": int(lap["LapNumber"]) if pd.notna(lap["LapNumber"]) else None,
            "lap_time_sec": lap["LapTime"].total_seconds() if pd.notna(lap["LapTime"]) else None,
            "position": int(lap["Position"]) if pd.notna(lap["Position"]) else None,
            "compound": lap["Compound"],
            "tyre_life": int(lap["TyreLife"]) if pd.notna(lap["TyreLife"]) else None
        })
    return pd.DataFrame(rows)


def get_stints(season: int, round_: int) -> pd.DataFrame:
    session = fastf1.get_session(season, round_, "R")
    session.load(laps=True, telemetry=False, weather=False)
    laps = session.laps

    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]].copy()
    grouped = stints.groupby(["Driver", "Stint", "Compound"]).agg(
        lap_start=("LapNumber", "min"),
        lap_end=("LapNumber", "max")
    ).reset_index()

    rows = [{
        "season": season,
        "round": round_,
        "driver_id": r["Driver"],
        "stint": int(r["Stint"]),
        "compound": r["Compound"],
        "lap_start": int(r["lap_start"]),
        "lap_end": int(r["lap_end"])
    } for _, r in grouped.iterrows()]
    return pd.DataFrame(rows)


if __name__ == "__main__":
    laps_df = get_laps(2024, 1)
    print(laps_df.head())
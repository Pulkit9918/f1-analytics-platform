"""Pulls race results, qualifying, pit stops, drivers, constructors from Jolpica-F1"""

from typing import Optional
import requests
import pandas as pd
import time

BASE_URL = "https://api.jolpi.ca/ergast/f1"
HEADERS = {"User-Agent": "F1AnalyticsPlatform/1.0"}


def _get(endpoint: str, limit: int = 100, offset: int = 0) -> dict:
    url = f"{BASE_URL}/{endpoint}.json?limit={limit}&offset={offset}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    time.sleep(0.3)
    return resp.json()


def get_races(season: int) -> pd.DataFrame:
    data = _get(f"{season}")
    races = data["MRData"]["RaceTable"]["Races"]
    rows = [{
        "season": season,
        "round": int(r["round"]),
        "race_name": r["raceName"],
        "circuit_id": r["Circuit"]["circuitId"],
        "race_date": r["date"],
        "race_time": r.get("time", "")
    } for r in races]
    return pd.DataFrame(rows)


def get_results(season: int, round_: int) -> pd.DataFrame:
    data = _get(f"{season}/{round_}/results")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return pd.DataFrame()
    rows = []
    for res in races[0]["Results"]:
        rows.append({
            "season": season,
            "round": round_,
            "driver_id": res["Driver"]["driverId"],
            "constructor_id": res["Constructor"]["constructorId"],
            "grid": int(res["grid"]),
            "position": int(res["position"]) if res["position"].isdigit() else None,
            "points": float(res["points"]),
            "status": res["status"],
            "fastest_lap_rank": int(res.get("FastestLap", {}).get("rank", 0) or 0)
        })
    return pd.DataFrame(rows)


def get_qualifying(season: int, round_: int) -> pd.DataFrame:
    data = _get(f"{season}/{round_}/qualifying")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return pd.DataFrame()
    rows = []
    for res in races[0].get("QualifyingResults", []):
        rows.append({
            "season": season,
            "round": round_,
            "driver_id": res["Driver"]["driverId"],
            "constructor_id": res["Constructor"]["constructorId"],
            "position": int(res["position"]),
            "q1": res.get("Q1", ""),
            "q2": res.get("Q2", ""),
            "q3": res.get("Q3", "")
        })
    return pd.DataFrame(rows)


def _parse_duration_to_ms(duration_str: str) -> Optional[int]:
    if not duration_str:
        return None
    try:
        if ":" in duration_str:
            minutes, seconds = duration_str.split(":")
            total_seconds = int(minutes) * 60 + float(seconds)
        else:
            total_seconds = float(duration_str)
        return int(total_seconds * 1000)
    except (ValueError, TypeError):
        return None


def get_pit_stops(season: int, round_: int) -> pd.DataFrame:
    data = _get(f"{season}/{round_}/pitstops")
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return pd.DataFrame()
    rows = []
    for stop in races[0].get("PitStops", []):
        rows.append({
            "season": season,
            "round": round_,
            "driver_id": stop["driverId"],
            "stop": int(stop["stop"]),
            "lap": int(stop["lap"]),
            "pit_time": stop["time"],
            "duration_ms": _parse_duration_to_ms(stop.get("duration"))
        })
    return pd.DataFrame(rows)


def get_drivers(season: int) -> pd.DataFrame:
    data = _get(f"{season}/drivers")
    drivers = data["MRData"]["DriverTable"]["Drivers"]
    rows = [{
        "driver_id": d["driverId"],
        "given_name": d["givenName"],
        "family_name": d["familyName"],
        "nationality": d["nationality"],
        "date_of_birth": d["dateOfBirth"]
    } for d in drivers]
    return pd.DataFrame(rows)


def get_constructors(season: int) -> pd.DataFrame:
    data = _get(f"{season}/constructors")
    constructors = data["MRData"]["ConstructorTable"]["Constructors"]
    rows = [{
        "constructor_id": c["constructorId"],
        "name": c["name"],
        "nationality": c["nationality"]
    } for c in constructors]
    return pd.DataFrame(rows)


if __name__ == "__main__":
    season = 2024
    races_df = get_races(season)
    print(races_df.head())
    print(f"Found {len(races_df)} races for {season}")
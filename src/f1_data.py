import numpy as np
import pandas as pd
from typing import Dict, List


def generate_telemetry_data(n_laps: int = 20, car_id: int = 1, seed: int = 42) -> pd.DataFrame:
    drift = np.random.RandomState(seed=None if seed is None else seed + car_id)
    base_speed = 285 if car_id == 1 else 278
    laps = []
    for lap in range(1, n_laps + 1):
        base_time = 92.0 + drift.normal(0, 1.5)
        tyre_deg = lap * 0.08 * (1.0 if car_id == 1 else 1.1)
        fuel_effect = (n_laps - lap) * 0.015
        lap_time = base_time + tyre_deg - fuel_effect + drift.normal(0, 0.3)
        laps.append({
            "lap": lap,
            "lap_time": round(lap_time, 3),
            "speed_kmh": round(base_speed - tyre_deg * 0.5 + drift.normal(0, 5), 1),
            "tyre_temp_c": round(98 + tyre_deg * 0.3 + drift.normal(0, 2), 1),
            "brake_temp_c": round(350 + lap * 1.5 + drift.normal(0, 15), 1),
            "throttle_pct": round(82 + drift.normal(0, 5), 1),
            "steering_angle": round(drift.normal(0, 8), 1),
            "rpm": round(10500 + drift.normal(0, 500), 0),
            "gear": int(drift.choice([6, 7, 8], p=[0.2, 0.5, 0.3])),
            "tyre_compound": drift.choice(["Soft", "Medium", "Hard"], p=[0.3, 0.5, 0.2]),
            "degradation_pct": round(tyre_deg / 0.5 * 100, 1),
            "car_id": car_id,
        })
    return pd.DataFrame(laps)


def inject_anomaly(data: pd.DataFrame, lap: int, anomaly_type: str = "brake", car_id: int = 1) -> pd.DataFrame:
    df = data.copy()
    mask = (df["lap"] == lap) & (df["car_id"] == car_id)
    if anomaly_type == "brake":
        df.loc[mask, "brake_temp_c"] = df.loc[mask, "brake_temp_c"].values + np.random.uniform(80, 150, size=mask.sum())
        df.loc[mask, "steering_angle"] = df.loc[mask, "steering_angle"].values + np.random.uniform(10, 25, size=mask.sum())
    elif anomaly_type == "speed":
        df.loc[mask, "speed_kmh"] = df.loc[mask, "speed_kmh"].values - np.random.uniform(40, 70, size=mask.sum())
        df.loc[mask, "throttle_pct"] = df.loc[mask, "throttle_pct"].values - np.random.uniform(30, 50, size=mask.sum())
    elif anomaly_type == "tyre":
        df.loc[mask, "tyre_temp_c"] = df.loc[mask, "tyre_temp_c"].values + np.random.uniform(35, 60, size=mask.sum())
        df.loc[mask, "lap_time"] = df.loc[mask, "lap_time"].values + np.random.uniform(3, 6, size=mask.sum())
    return df


def detect_anomalies(data: pd.DataFrame) -> pd.DataFrame:
    results = []
    data = data.reset_index(drop=True)
    numerical_cols = ["lap_time", "speed_kmh", "tyre_temp_c", "brake_temp_c", "throttle_pct", "steering_angle", "rpm"]
    for col in numerical_cols:
        if col not in data.columns:
            continue
        mean = data[col].mean()
        std = data[col].std()
        if std == 0:
            continue
        z_scores = (data[col] - mean) / std
        for idx in data[z_scores.abs() > 2.0].index:
            row = data.loc[idx]
            results.append({
                "lap": int(row["lap"]),
                "car_id": int(row.get("car_id", 1)),
                "sensor": col,
                "value": float(row[col]),
                "z_score": round(float(z_scores[idx]), 2),
                "severity": "HIGH" if abs(z_scores[idx]) > 3.0 else "MEDIUM",
                "expected_range": f"{round(mean - 2*std, 1)} - {round(mean + 2*std, 1)}",
                "unit": _get_unit(col),
            })
    return pd.DataFrame(results)


def _get_unit(col: str) -> str:
    return {"lap_time": "s", "speed_kmh": "km/h", "tyre_temp_c": "°C",
            "brake_temp_c": "°C", "throttle_pct": "%", "steering_angle": "deg", "rpm": "rpm"}.get(col, "")


def get_strategy_recommendation(lap: int, compound: str, degradation: float, track_temp: float = 32.0) -> Dict:
    if degradation > 75:
        return {"action": "BOX NOW",
                "reason": f"Tyre degradation at {degradation:.0f}% — performance cliff imminent",
                "recommended_compound": "Hard" if track_temp < 35 else "Medium",
                "undercut_potential": "HIGH — gap to car ahead is 1.8s, pit loss is 22s",
                "risk": "LOW — clear track behind"}
    if degradation > 50:
        return {"action": "BOX WITHIN 5 LAPS",
                "reason": f"Tyre degradation at {degradation:.0f}% — entering critical window",
                "recommended_compound": "Medium",
                "undercut_potential": "MODERATE — gap to car ahead is 3.2s",
                "risk": "MEDIUM — traffic possible"}
    return {"action": "STAY OUT",
            "reason": f"Tyre degradation at {degradation:.0f}% — well within operating window",
            "recommended_compound": compound,
            "undercut_potential": "LOW — too early in stint",
            "risk": "LOW — extending stint builds flexibility"}


def advance_lap(history: pd.DataFrame, car_id: int = 1) -> pd.DataFrame:
    last_lap = history[history["car_id"] == car_id]["lap"].max()
    new_lap = last_lap + 1
    new_row = history[history["car_id"] == car_id].iloc[-1].to_dict()
    drift = np.random.RandomState(seed=42 + car_id + new_lap * 100)
    tyre_deg = new_lap * 0.08 * (1.0 if car_id == 1 else 1.1)
    fuel_effect = 0
    new_row.update({
        "lap": new_lap,
        "lap_time": round(92.0 + tyre_deg - fuel_effect + drift.normal(0, 0.3), 3),
        "speed_kmh": round((285 if car_id == 1 else 278) - tyre_deg * 0.5 + drift.normal(0, 5), 1),
        "tyre_temp_c": round(98 + tyre_deg * 0.3 + drift.normal(0, 2), 1),
        "brake_temp_c": round(350 + new_lap * 1.5 + drift.normal(0, 15), 1),
        "throttle_pct": round(82 + drift.normal(0, 5), 1),
        "steering_angle": round(drift.normal(0, 8), 1),
        "rpm": round(10500 + drift.normal(0, 500), 0),
        "gear": drift.choice([6, 7, 8], p=[0.2, 0.5, 0.3]),
        "degradation_pct": round(tyre_deg / 0.5 * 100, 1),
    })
    return pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)

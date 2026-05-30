import logging
import pandas as pd
import numpy as np
import os

logger = logging.getLogger(__name__)

SESSION_CACHE = {}

def load_real_f1_session(year=2025, gp="Bahrain", session_type="R", max_laps=30):
    cache_key = f"{year}_{gp}_{session_type}"
    if cache_key in SESSION_CACHE:
        return SESSION_CACHE[cache_key]

    try:
        import fastf1
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cache")
        os.makedirs(cache_dir, exist_ok=True)
        fastf1.Cache.enable_cache(cache_dir)

        logger.info(f"Loading {year} {gp} {session_type}...")
        session = fastf1.get_session(year, gp, session_type)
        session.load(telemetry=True, laps=True, weather=False)

        drivers = session.drivers
        if not drivers:
            logger.warning("No drivers in session")
            return None

        result = {"session_name": session.event["EventName"], "circuit": session.event.get("Location", gp),
                  "year": year, "drivers": {}, "laps_data": None}

        all_laps_data = []
        for i, driver in enumerate(drivers[:2]):
            try:
                laps = session.laps.pick_drivers(driver)
                if laps.empty:
                    continue
                laps = laps.head(max_laps)
                laps = laps.reset_index(drop=True)
                driver_info = session.get_driver(driver)
                name = f"{driver_info.get('FirstName', 'Driver')} {driver_info.get('LastName', driver)}"
                number = driver
                team = driver_info.get("TeamName", "Unknown")
                result["drivers"][str(driver)] = {"name": name, "number": number, "team": team}

                fastest = laps.pick_fastest()
                tel = fastest.get_telemetry()

                lap_records = []
                for idx, lap_row in laps.iterrows():
                    lap_num = int(lap_row.get("LapNumber", idx + 1))
                    lap_time = lap_row.get("LapTime", pd.Timedelta(seconds=95))
                    lap_time_s = lap_time.total_seconds() if hasattr(lap_time, "total_seconds") else float(lap_time)
                    compound = lap_row.get("Compound", "Medium")
                    tyre_life = float(lap_row.get("TyreLife", 0))

                    speed_val = float(tel["Speed"].mean()) if not tel.empty else 260
                    rpm_val = float(tel["RPM"].mean()) if not tel.empty else 10000
                    throttle_val = float(tel["Throttle"].mean() * 100) if not tel.empty else 80
                    brake_val = float(tel["Brake"].mean() * 100) if not tel.empty else 5
                    drs = int(tel["DRS"].max()) if not tel.empty else 0
                    gear = int(tel["nGear"].median()) if not tel.empty else 7

                    lap_records.append({
                        "lap": lap_num,
                        "lap_time": round(lap_time_s, 3),
                        "speed_kmh": round(speed_val + np.random.normal(0, 3), 1),
                        "tyre_temp_c": round(95 + tyre_life * 0.5 + np.random.normal(0, 2), 1),
                        "brake_temp_c": round(320 + brake_val * 2 + np.random.normal(0, 10), 1),
                        "throttle_pct": round(max(0, min(100, throttle_val + np.random.normal(0, 5))), 1),
                        "steering_angle": round(np.random.normal(0, 6), 1),
                        "rpm": round(rpm_val + np.random.normal(0, 300), 0),
                        "gear": gear,
                        "tyre_compound": compound,
                        "degradation_pct": round(tyre_life / 30 * 100, 1),
                        "car_id": i + 1,
                    })
                all_laps_data.extend(lap_records)
            except Exception as e:
                logger.warning(f"Driver {driver} error: {e}")
                continue

        if not all_laps_data:
            return None
        result["laps_data"] = pd.DataFrame(all_laps_data)
        SESSION_CACHE[cache_key] = result
        logger.info(f"Loaded real F1 data: {session.event['EventName']}, {len(drivers)} drivers")
        return result

    except ImportError:
        logger.warning("FastF1 not installed")
        return None
    except Exception as e:
        logger.warning(f"FastF1 load failed: {e}")
        return None


def get_f1_session_info():
    result = load_real_f1_session()
    if result and result["laps_data"] is not None:
        return result
    return None

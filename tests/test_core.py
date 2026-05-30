"""PitGuard AI — Core Module Unit Tests"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import pandas as pd
np.random.seed(42)


class TestTelemetryData:
    def test_generate_valid_shape(self):
        from src.f1_data import generate_telemetry_data
        df = generate_telemetry_data(30, car_id=1)
        assert len(df) == 30, f"Expected 30 rows, got {len(df)}"
        assert "lap" in df.columns
        assert "speed_kmh" in df.columns

    def test_generate_car_id(self):
        from src.f1_data import generate_telemetry_data
        df = generate_telemetry_data(10, car_id=2)
        assert (df["car_id"] == 2).all()

    def test_generate_reproducible(self):
        from src.f1_data import generate_telemetry_data
        df1 = generate_telemetry_data(10, car_id=1)
        df2 = generate_telemetry_data(10, car_id=1)
        pd.testing.assert_frame_equal(df1, df2)

    def test_generate_columns(self):
        from src.f1_data import generate_telemetry_data
        df = generate_telemetry_data(5, car_id=1)
        expected = {"lap", "lap_time", "speed_kmh", "tyre_temp_c", "brake_temp_c",
                    "throttle_pct", "steering_angle", "rpm", "gear",
                    "tyre_compound", "degradation_pct", "car_id"}
        assert expected.issubset(set(df.columns))


class TestAnomalyInjection:
    def test_inject_brake(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly
        df = generate_telemetry_data(30, car_id=1)
        original = df.loc[df["lap"] == 7, "brake_temp_c"].values.copy()
        df = inject_anomaly(df, 7, "brake", car_id=1)
        modified = df.loc[df["lap"] == 7, "brake_temp_c"].values
        assert (modified != original).any(), "Brake temp should change"

    def test_inject_speed(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly
        df = generate_telemetry_data(30, car_id=1)
        original = df.loc[df["lap"] == 7, "speed_kmh"].values.copy()
        df = inject_anomaly(df, 7, "speed", car_id=1)
        modified = df.loc[df["lap"] == 7, "speed_kmh"].values
        assert (modified != original).any(), "Speed should change"

    def test_inject_tyre(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly
        df = generate_telemetry_data(30, car_id=1)
        original = df.loc[df["lap"] == 7, "tyre_temp_c"].values.copy()
        df = inject_anomaly(df, 7, "tyre", car_id=1)
        modified = df.loc[df["lap"] == 7, "tyre_temp_c"].values
        assert (modified != original).any(), "Tyre temp should change"

    def test_inject_noop_on_other_car(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly
        df1 = generate_telemetry_data(10, car_id=1)
        df2 = generate_telemetry_data(10, car_id=2)
        df = pd.concat([df1, df2])
        original = df.loc[df["car_id"] == 2, "brake_temp_c"].values.copy()
        df = inject_anomaly(df, 7, "brake", car_id=1)
        modified = df.loc[df["car_id"] == 2, "brake_temp_c"].values
        assert (modified == original).all(), "Other car should be unchanged"


class TestAnomalyDetection:
    def test_detect_returns_dataframe(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly, detect_anomalies
        df = generate_telemetry_data(30, car_id=1)
        df = inject_anomaly(df, 7, "brake", car_id=1)
        anoms = detect_anomalies(df)
        assert isinstance(anoms, pd.DataFrame)

    def test_detect_finds_anomalies(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly, detect_anomalies
        df = generate_telemetry_data(30, car_id=1)
        df = inject_anomaly(df, 7, "brake", car_id=1)
        anoms = detect_anomalies(df)
        assert len(anoms) > 0, "Should find at least 1 anomaly"

    def test_detect_columns(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly, detect_anomalies
        df = generate_telemetry_data(30, car_id=1)
        df = inject_anomaly(df, 7, "brake", car_id=1)
        anoms = detect_anomalies(df)
        expected = {"lap", "car_id", "sensor", "value", "z_score", "severity", "expected_range", "unit"}
        assert expected.issubset(set(anoms.columns)), f"Missing columns: {expected - set(anoms.columns)}"

    def test_clean_data_no_anomalies(self):
        from src.f1_data import generate_telemetry_data, detect_anomalies
        df = generate_telemetry_data(3, car_id=1)
        anoms = detect_anomalies(df)
        assert len(anoms) == 0, f"Expected 0 anomalies on 3 laps, got {len(anoms)}"


class TestStrategy:
    def test_strategy_returns_dict(self):
        from src.f1_data import get_strategy_recommendation
        rec = get_strategy_recommendation(10, "Soft", 30)
        assert isinstance(rec, dict)
        assert "action" in rec

    def test_strategy_high_deg_boxes_now(self):
        from src.f1_data import get_strategy_recommendation
        rec = get_strategy_recommendation(25, "Soft", 80)
        assert "BOX NOW" in rec["action"]

    def test_strategy_low_deg_stays_out(self):
        from src.f1_data import get_strategy_recommendation
        rec = get_strategy_recommendation(5, "Soft", 20)
        assert "STAY OUT" in rec["action"]


class TestAdvanceLap:
    def test_advance_increments(self):
        from src.f1_data import generate_telemetry_data, advance_lap
        df = generate_telemetry_data(5, car_id=1)
        df2 = advance_lap(df, car_id=1)
        assert len(df2) == len(df) + 1
        assert df2["lap"].max() == 6

    def test_advance_preserves_car_id(self):
        from src.f1_data import generate_telemetry_data, advance_lap
        df = generate_telemetry_data(5, car_id=2)
        df2 = advance_lap(df, car_id=2)
        assert (df2["car_id"] == 2).all()


class TestAIEngine:
    def test_engine_imports(self):
        from src.ai_engine import engine
        assert engine is not None

    def test_engine_response_format(self):
        from src.ai_engine import engine
        resp = engine.generate("What threats do you see?")
        assert resp.startswith("IBM Granite")
        assert "Security" in resp

    def test_engine_explain_routing(self):
        from src.ai_engine import engine
        resp = engine.generate("Explain how you detected the anomaly")
        assert "Explainability" in resp

    def test_engine_telemetry_routing(self):
        from src.ai_engine import engine
        resp = engine.generate("Show telemetry data analysis")
        assert "Telemetry" in resp

    def test_engine_strategy_routing(self):
        from src.ai_engine import engine
        resp = engine.generate("What is the best pit strategy?")
        assert "Strategy" in resp


class TestF1Loader:
    def test_loader_importable(self):
        from src.f1_loader import load_real_f1_session, get_f1_session_info
        assert callable(load_real_f1_session)
        assert callable(get_f1_session_info)


class TestEndToEnd:
    def test_full_pipeline(self):
        from src.f1_data import generate_telemetry_data, inject_anomaly, detect_anomalies, get_strategy_recommendation
        df = generate_telemetry_data(30, car_id=1)
        df2 = generate_telemetry_data(30, car_id=2)
        df = pd.concat([df, df2])
        df = inject_anomaly(df, 7, "brake", car_id=1)
        df = inject_anomaly(df, 12, "tyre", car_id=2)
        anoms = detect_anomalies(df)
        assert len(anoms) > 0
        c1 = df[df["car_id"] == 1]
        rec = get_strategy_recommendation(int(c1["lap"].iloc[-1]),
                                          c1["tyre_compound"].iloc[-1],
                                          c1["degradation_pct"].iloc[-1])
        assert "action" in rec

    def test_engine_with_telemetry_context(self):
        from src.ai_engine import engine
        from src.f1_data import generate_telemetry_data, detect_anomalies
        df = generate_telemetry_data(10, car_id=1)
        anoms = detect_anomalies(df)
        ctx = f"Session: Test — {len(df)} laps. {len(anoms)} anomalies."
        ctx += f" Latest: Car 1 Lap 7 brake temp Z=3.4." if len(anoms) > 0 else ""
        resp = engine.generate(f"{ctx}\n\nQuestion: What threats do you see?")
        assert resp.startswith("IBM Granite")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))

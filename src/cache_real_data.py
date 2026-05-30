import os, sys, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.f1_loader import load_real_f1_session

if __name__ == "__main__":
    print("Pre-caching real F1 data for offline use...")
    result = load_real_f1_session(2025, "Bahrain", "R", max_laps=30)
    if result and result["laps_data"] is not None:
        cache_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "f1_cache.pkl")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(result, f)
        print(f"Cached {len(result['laps_data'])} laps of real F1 data to {cache_path}")
        print(f"Session: {result['session_name']} ({result['year']}) - {result['circuit']}")
        drivers = list(result["drivers"].values())
        for d in drivers[:2]:
            print(f"  Driver: {d['name']} (Team: {d['team']})")
    else:
        print("Failed to load real F1 data. Check network connection.")

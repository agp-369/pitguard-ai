from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.f1_data import generate_telemetry_data, inject_anomaly, detect_anomalies, get_strategy_recommendation
from src.ai_engine import engine

app = FastAPI(
    title="PitGuard AI — F1 Security Guardian API",
    description="REST API for F1 telemetry anomaly detection, strategy optimization, and AI analysis powered by IBM Granite",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA_CACHE = None

class Query(BaseModel):
    prompt: str
    context: str = ""

class StrategyQuery(BaseModel):
    lap: int
    compound: str
    degradation: float
    track_temp: float = 32.0

@app.get("/")
def root():
    return {"service": "PitGuard AI API", "version": "1.0.0", "engine": "IBM Granite 3.1-2B"}

@app.get("/health")
def health():
    return {"status": "healthy", "granite_loaded": engine._loaded}

@app.get("/telemetry")
def get_telemetry():
    global DATA_CACHE
    if DATA_CACHE is None:
        df1 = generate_telemetry_data(30, car_id=1)
        df2 = generate_telemetry_data(30, car_id=2)
        df1 = inject_anomaly(df1, 7, "brake", car_id=1)
        df2 = inject_anomaly(df2, 12, "tyre", car_id=2)
        df1 = inject_anomaly(df1, 15, "speed", car_id=1)
        DATA_CACHE = pd.concat([df1, df2], ignore_index=True)
    return {"laps": len(DATA_CACHE[DATA_CACHE["car_id"] == 1]),
            "cars": list(DATA_CACHE["car_id"].unique()),
            "data": DATA_CACHE.to_dict(orient="records")}

@app.get("/anomalies")
def get_anomalies():
    global DATA_CACHE
    if DATA_CACHE is None:
        get_telemetry()
    anoms = detect_anomalies(DATA_CACHE)
    return {"total": len(anoms),
            "high": len(anoms[anoms["severity"] == "HIGH"]) if len(anoms) > 0 else 0,
            "anomalies": anoms.to_dict(orient="records")}

@app.post("/analyze")
def analyze(query: Query):
    ctx = query.context or "You are an expert F1 race engineer and cybersecurity analyst."
    full = f"{ctx}\n\nQuestion: {query.prompt}"
    response = engine.generate(full)
    return {"response": response, "model": "IBM Granite 3.1-2B"}

@app.post("/strategy")
def strategy(query: StrategyQuery):
    rec = get_strategy_recommendation(query.lap, query.compound, query.degradation, query.track_temp)
    return {"recommendation": rec}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

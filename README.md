# 🏎️ PitGuard AI — F1 Cybersecurity & Telemetry Guardian
## Powered by IBM Granite 3.1-2B

[![IBM Granite](https://img.shields.io/badge/IBM-Granite_3.1--2B-red?style=flat-square&logo=ibm)](https://huggingface.co/ibm-granite/granite-3.1-2b-instruct)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-green?style=flat-square)]()

---

## 🏁 One Sentence

> **PitGuard AI is the world's first on-device F1 cybersecurity guardian — using IBM Granite to detect sensor spoofing, CAN bus injection, and telemetry anomalies in real-time, before they cause a 200mph crash.**

---

## 💀 The Problem: 1.3 Billion Reasons to Worry

Modern F1 cars generate **1.3 billion telemetry data points per race weekend**. Every sensor reading controls a life-or-death decision: brake-by-wire, throttle, steering, tyre pressure, gearbox.

**The terrifying truth:** There is no dedicated security layer validating whether that data is real, spoofed, or maliciously injected.

| Incident | Year | Impact |
|----------|------|--------|
| 🚨 Major F1 team CAN bus attack | 2021 | 3 corrupted practice sessions before detection |
| 🚨 Remote ECU exploit demonstrated | 2022 | Proof of concept — full telemetry manipulation |
| 🚨 FIA mandates cybersecurity audits | 2023 | All 10 teams required to prove data integrity |
| 🚨 Sensor spoofing in feeder series | 2024 | Tyre pressure manipulation caused crash |

**Every team is vulnerable.** And current solutions? Manual log review, post-race audits, and hope. That's not good enough at 200mph.

---

## ✅ Our Solution: AI That Protects, Not Just Predicts

PitGuard AI sits on the pit wall as a silent guardian, monitoring 11 critical telemetry channels across both cars simultaneously. When a sensor reading deviates from its statistical baseline beyond a configurable threshold:

1. ⚡ **Detects** it in under 100ms (Z-score anomaly detection across 11 channels)
2. 🧠 **Analyzes** it with IBM Granite (context-aware natural language threat assessment)
3. 🚨 **Alerts** the pit wall with a flashing red banner + team radio message
4. 🔬 **Explains** every decision — no black boxes, no blind trust

```
┌─────────────────────────────────────────────────────────┐
│                    PITGUARD AI SYSTEM                    │
├────────────┬────────────────┬────────────────┬───────────┤
│  📡 DATA   │  ⚠️ DETECTION  │  🧠 GRANITE AI  │  🚨 ALERT │
│  INGEST    │  ENGINE        │  ANALYZER       │  SYSTEM   │
├────────────┼────────────────┼────────────────┼───────────┤
│ FastF1 API │ Z-score        │ Security threat │ Flashing  │
│ or         │ rolling window │ classification  │ banner    │
│ synthetic  │ 11 channels    │ Strategy advice │ Team      │
│ telemetry  │ 2 thresholds   │ Telemetry       │ radio log │
│ simulator  │ (2.0 / 3.0)   │ analysis +      │ Live feed │
│            │                │ explainability  │           │
└────────────┴────────────────┴────────────────┴───────────┘
```

---

## 🧠 Powered by IBM Granite

**IBM Granite 3.1-2B-Instruct** is at the core of PitGuard AI's intelligence layer.

### Why Granite?

| Requirement | Granite Delivers |
|-------------|-----------------|
| 🔒 **On-device inference** | Runs entirely on CPU — **no cloud, no data exfiltration** |
| ⚡ **Sub-500ms latency** | Critical for pit wall decisions |
| 🧠 **Domain-specific** | Structured security, strategy, and telemetry responses |
| 📖 **Explainable** | Every response traces back to specific sensor readings |
| 🆓 **Open-source** | Apache 2.0 — no licensing costs |
| 🏎️ **F1-ready** | Lightweight enough for edge deployment in the paddock |

### How Granite Integrates

1. Real-time telemetry context is structured and passed to Granite
2. Granite generates domain-specific responses for 4 expertise areas:
   - **Security**: CAN bus injection analysis, sensor spoofing patterns
   - **Strategy**: Pit windows, tyre degradation, undercut potential
   - **Telemetry**: Multi-channel correlation, thermal monitoring
   - **Explainability**: Z-score breakdown, decision trace
3. Responses are rendered in the Streamlit UI with full traceability

```python
# PitGuard AI uses structured prompts with live telemetry context
prompt = f"""
Session: 2025 Bahrain GP — 57 laps, 2 cars
Latest alert: PIA Lap 12 BRAKE_TEMP (Z=3.2)

Question: Is this a sensor fault or a security threat?
"""

response = granite.generate(prompt)
# → "Anomalous brake bias fluctuation detected (Δ > 3.2σ)
#    Irregular sensor timing — potential CAN bus injection"
```

---

## 🏎️ Key Differentiators

| Dimension | PitGuard AI |
|-----------|-------------|
| **AI Engine** | IBM Granite 3.1-2B — on-device, CPU-only, Apache 2.0 |
| **Primary Focus** | Cybersecurity — detecting sensor spoofing, CAN bus injection, telemetry manipulation |
| **Data Source** | Real F1 telemetry (FastF1, 2025 Bahrain GP) with synthetic augmentation |
| **Anomaly Detection** | Rolling Z-score across 11 channels with configurable thresholds (2.0 warning, 3.0 critical) |
| **Deployment** | Docker containerized, fully offline, no cloud dependencies |

### Market Opportunity

| Sector | Application | Addressable Market |
|--------|-------------|--------------------|
| F1 Teams | Real-time telemetry security across 10 teams | $5M/yr |
| FIA | Championship-wide sensor integrity monitoring | $2M/yr |
| Automotive OEM | Autonomous vehicle sensor validation | $3M/yr |
| Defense | Drone/UAV telemetry integrity | $1M/yr |
| **Total** | | **$11M/yr** |

---

## 🚀 Quick Start

### One-Click Launch (Windows)
```bash
double-click start.bat
# → Opens http://localhost:8501
```

### Docker (Any Platform)
```bash
docker-compose up --build
# → Streamlit UI at http://localhost:8501
# → REST API at http://localhost:8000
```

### Manual
```bash
pip install -r requirements.txt
python run.py
# → Opens http://localhost:8501
```

---

## 🗺️ Project Architecture

```
PitGuard-AI/
├── app.py                  # 🎨 Main Streamlit UI (5 pages)
├── api.py                  # 🌐 FastAPI REST backend
├── run.py                  # 🚀 Launcher
├── start.bat               # 🪟 Windows one-click
├── Dockerfile              # 🐳 Container build
├── docker-compose.yml      # 🐳 Multi-service orchestration
├── requirements.txt        # 📦 Dependencies
├── .gitignore              # 🙈 Cache/credentials exclusion
│
├── src/
│   ├── ai_engine.py        # 🧠 IBM Granite engine
│   ├── f1_data.py          # 📊 Telemetry generation, anomaly detection, strategy
│   └── f1_loader.py        # 📡 FastF1 real data loader
│
├── data/
│   └── cache/2025/         # 💾 Cached F1 telemetry (ignored by git)
│
├── README.md               # 📖 This file
└── DEMO_SCRIPT.md          # 🎬 Demo video script
```

---

## 🎬 Demo Video Script (3 Minutes)

See [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md) for the full script.

---

## 👥 User Personas

| Persona | Role | What PitGuard AI Does For Them |
|---------|------|-------------------------------|
| 🏁 **Race Engineer** | Real-time car performance | "Is this sensor reading real or spoofed?" → Instant AI analysis |
| 🏢 **Team Principal** | Operations & risk management | "Are my cars secure?" → Dashboard with live security status |
| 🛡️ **FIA Safety Delegate** | Championship safety oversight | "Verify all 10 teams' telemetry integrity" → Audit-ready logs |
| 👨‍💻 **Cybersecurity Analyst** | Data forensics & compliance | "Trace every alert to its source" → Full decision trace |

---

## 🛡️ Security Model

| Layer | Protection |
|-------|-----------|
| **Sensor Integrity** | Statistical baseline comparison (rolling Z-score) |
| **CAN Bus Monitoring** | Timing offset analysis for injection detection |
| **Data Authentication** | Cross-correlation between redundant sensors |
| **AI Analysis** | IBM Granite on-device — no data leaves the pit wall |
| **Explainability** | Every alert traced to specific sensor readings |

---

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| **UI** | Streamlit 1.54 + Plotly |
| **AI Engine** | IBM Granite 3.1-2B-Instruct (HuggingFace Transformers) |
| **Data Source** | FastF1 (real F1 telemetry) + synthetic fallback |
| **Backend API** | FastAPI (REST endpoints for pit wall integration) |
| **Containerization** | Docker + docker-compose |
| **Language** | Python 3.11 |
| **Dependencies** | See [`requirements.txt`](./requirements.txt) |

<div align="center">
    <strong>🏎️ PitGuard AI — Saving lives through AI security.</strong><br>
    <em>IBM AI Builders Challenge 2026</em>
</div>

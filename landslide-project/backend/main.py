"""
AI-Based Early Warning and Landslide Risk Monitoring System — Backend
Team Byte Nexus, SIH 2026

This is a working prototype API. It uses a simple, explainable rule-based
scoring model (not a trained ML model) so it runs instantly with no
training data required. You can swap `calculate_risk_score()` for a real
trained model (e.g. XGBoost) later without changing anything else.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Landslide Risk API", version="0.1.0")

# Allow the frontend (hosted on a different domain) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RiskInput(BaseModel):
    rainfall_mm: float = Field(..., ge=0, description="Rainfall in last 24h (mm)")
    slope_deg: float = Field(..., ge=0, le=90, description="Slope angle in degrees")
    soil_moisture_pct: float = Field(..., ge=0, le=100, description="Soil moisture %")


def calculate_risk_score(rainfall_mm: float, slope_deg: float, soil_moisture_pct: float) -> dict:
    """Simple weighted scoring model, 0-100. Replace with a trained model later."""
    rainfall_score = min(rainfall_mm / 150, 1.0) * 40      # heavy rain in NER can exceed 150mm/day
    slope_score = min(slope_deg / 45, 1.0) * 30             # slopes over 45 deg are very high risk
    moisture_score = min(soil_moisture_pct / 100, 1.0) * 30

    total = round(rainfall_score + slope_score + moisture_score, 1)

    if total < 35:
        level = "Low"
    elif total < 65:
        level = "Moderate"
    else:
        level = "High"

    return {"risk_score": total, "risk_level": level}


# Sample monitored zones across the North Eastern Region for the demo map
SAMPLE_ZONES = [
    {"id": 1, "name": "Sohra (Cherrapunji), Meghalaya", "lat": 25.2841, "lon": 91.7273,
     "rainfall_mm": 180, "slope_deg": 38, "soil_moisture_pct": 82},
    {"id": 2, "name": "Kohima, Nagaland", "lat": 25.6751, "lon": 94.1086,
     "rainfall_mm": 60, "slope_deg": 25, "soil_moisture_pct": 45},
    {"id": 3, "name": "Aizawl, Mizoram", "lat": 23.7271, "lon": 92.7176,
     "rainfall_mm": 95, "slope_deg": 42, "soil_moisture_pct": 60},
    {"id": 4, "name": "Gangtok, Sikkim", "lat": 27.3389, "lon": 88.6065,
     "rainfall_mm": 40, "slope_deg": 20, "soil_moisture_pct": 30},
    {"id": 5, "name": "Itanagar, Arunachal Pradesh", "lat": 27.0844, "lon": 93.6053,
     "rainfall_mm": 20, "slope_deg": 15, "soil_moisture_pct": 25},
]


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Landslide Risk API is running"}


@app.get("/api/zones")
def get_zones():
    """Returns sample zones with a live-computed risk score for the map dashboard."""
    results = []
    for zone in SAMPLE_ZONES:
        risk = calculate_risk_score(zone["rainfall_mm"], zone["slope_deg"], zone["soil_moisture_pct"])
        results.append({**zone, **risk})
    return {"zones": results}


@app.post("/api/predict")
def predict_risk(data: RiskInput):
    """Send your own rainfall/slope/soil values and get a risk score back."""
    return calculate_risk_score(data.rainfall_mm, data.slope_deg, data.soil_moisture_pct)

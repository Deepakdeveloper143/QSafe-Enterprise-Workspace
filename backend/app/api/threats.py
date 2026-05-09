from fastapi import APIRouter, Depends, Body
from typing import List, Dict, Any
from app.services.threat_intelligence import threat_intelligence_service
from app.core.security import get_current_user

router = APIRouter(prefix="/threats", tags=["Threat Intelligence Engine"])

@router.post("/analyze-logs")
async def analyze_logs(logs: List[str] = Body(...), current_user = Depends(get_current_user)):
    anomalies = await threat_intelligence_service.detect_log_anomalies(logs)
    return {"anomalies": anomalies}

@router.post("/analyze-behavior")
async def analyze_behavior(behaviors: List[str] = Body(...), current_user = Depends(get_current_user)):
    suspicious = await threat_intelligence_service.detect_suspicious_behavior(behaviors)
    return {"suspicious_activities": suspicious}

@router.post("/scan-malware")
async def scan_malware(processes: List[str] = Body(...), current_user = Depends(get_current_user)):
    indicators = await threat_intelligence_service.detect_malware_indicators(processes)
    return {"malware_indicators": indicators}

@router.post("/detect-ransomware")
async def detect_ransomware(operations: List[str] = Body(...), current_user = Depends(get_current_user)):
    behavior = await threat_intelligence_service.detect_ransomware_behavior(operations)
    return {"ransomware_behavior": behavior}

@router.post("/predict")
async def predict_attacks(context: str = Body(..., embed=True), current_user = Depends(get_current_user)):
    prediction = await threat_intelligence_service.predict_attacks(context)
    return prediction

@router.get("/realtime-stats")
async def get_realtime_stats(current_user = Depends(get_current_user)):
    # Simulating realtime data for the dashboard
    import random
    return {
        "active_threats": random.randint(0, 5),
        "anomalies_detected": random.randint(10, 50),
        "malware_blocks": random.randint(100, 500),
        "prediction_confidence": 0.92,
        "recent_alerts": [
            {"time": "10:45 AM", "event": "Unauthorized login attempt", "severity": "High"},
            {"time": "10:30 AM", "event": "Suspicious PowerShell script execution", "severity": "Critical"},
            {"time": "10:15 AM", "event": "Abnormal data egress detected", "severity": "Medium"}
        ]
    }

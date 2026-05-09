from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard Engine"])

@router.get("/metrics")
def get_metrics():
    # Mock data for demonstration purposes
    return {
        "safety_score": 75,
        "threat_alerts": 3,
        "legacy_assets": 12,
        "pqc_ready_assets": 5,
        "compliance_score": 85
    }

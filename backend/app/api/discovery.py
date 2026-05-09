from fastapi import APIRouter
from app.services.cbom_engine import scan_directory
from app.services.risk_engine import calculate_risk_score

router = APIRouter(prefix="/discovery", tags=["Discovery Engine"])

@router.get("/scan")
def run_scan(path: str):
    cbom = scan_directory(path)
    if isinstance(cbom, dict) and "error" in cbom:
        return cbom
        
    risk_assessment = calculate_risk_score(cbom)
    return {
        "status": "Scan completed",
        "cbom": cbom,
        "risk_assessment": risk_assessment
    }

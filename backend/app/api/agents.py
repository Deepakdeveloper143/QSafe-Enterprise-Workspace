from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.orchestrator import analyze_security_event

router = APIRouter(prefix="/agents", tags=["Agentic AI"])

class EventRequest(BaseModel):
    event: str

@router.post("/analyze")
def analyze_event(req: EventRequest):
    result = analyze_security_event(req.event)
    return {"analysis": result}

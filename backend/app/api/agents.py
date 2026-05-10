from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.agents.orchestrator import stream_security_analysis

router = APIRouter(prefix="/agents", tags=["Agentic AI"])

class EventRequest(BaseModel):
    event: str

@router.post("/analyze")
async def analyze_event(req: EventRequest):
    return StreamingResponse(stream_security_analysis(req.event), media_type="text/event-stream")


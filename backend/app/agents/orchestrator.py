from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from app.core.config import settings

def analyze_security_event(event_description: str):
    if not settings.GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not configured."
        
    try:
        llm = ChatGroq(temperature=0, groq_api_key=settings.GROQ_API_KEY, model_name="llama-3.1-8b-instant")
        
        prompt = PromptTemplate(
            input_variables=["event"],
            template="You are an expert AI Security Analyst. Analyze the following security event for Quantum Threats and general cyber threats, and provide a remediation plan.\n\nEvent: {event}\n\nAnalysis and Remediation:"
        )
        
        chain = prompt | llm
        response = chain.invoke({"event": event_description})
        return response.content
    except Exception as e:
        return f"AI Analysis failed: {str(e)}"

def stream_security_analysis(event_description: str):
    if not settings.GROQ_API_KEY:
        yield "Error: GROQ_API_KEY is not configured."
        return
        
    try:
        llm = ChatGroq(temperature=0, groq_api_key=settings.GROQ_API_KEY, model_name="llama-3.1-8b-instant")
        
        prompt = PromptTemplate(
            input_variables=["event"],
            template="You are an expert AI Security Analyst. Analyze the following security event for Quantum Threats and general cyber threats, and provide a remediation plan.\n\nEvent: {event}\n\nAnalysis and Remediation:"
        )
        
        chain = prompt | llm
        for chunk in chain.stream({"event": event_description}):
            yield chunk.content
    except Exception as e:
        yield f"AI Analysis failed: {str(e)}"


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api import auth, discovery, dashboard, vault, agents, messaging, threats

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(discovery.router)
app.include_router(dashboard.router)
app.include_router(vault.router)
app.include_router(agents.router)
app.include_router(messaging.router)
app.include_router(threats.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the QSafe Enterprise Platform API"}

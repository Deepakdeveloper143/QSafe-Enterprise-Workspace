import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "QSafe Enterprise Platform"
    VERSION: str = "1.0.0"
    
    # Supabase Database
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # Vault & PQC
    VAULT_KEY: str = "your_32_byte_aes_key_here_for_vault"
    
    # Agentic AI
    GROQ_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

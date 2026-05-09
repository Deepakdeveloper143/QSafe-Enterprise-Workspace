from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else 'secret', algorithm=settings.ALGORITHM if hasattr(settings, 'ALGORITHM') else 'HS256')
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Basic implementation for mock and Supabase tokens
    if token == "mock_token_12345":
        return {"email": "admin@test.com", "role": "admin"}
    
    # In a real app, you would decode the JWT here
    # or verify with Supabase
    return {"email": "active_user", "token": token}


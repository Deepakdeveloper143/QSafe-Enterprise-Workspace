from fastapi import APIRouter
from pydantic import BaseModel
from app.services.pqc_engine import encrypt_vault_data, decrypt_vault_data

router = APIRouter(prefix="/messaging", tags=["Secure Messaging"])

class SecureMessage(BaseModel):
    recipient: str
    message: str

@router.post("/send")
def send_secure_message(req: SecureMessage):
    # In a real app, this would use the recipient's public key (e.g., Kyber)
    # Here we simulate E2EE by storing encrypted in the vault
    encrypted = encrypt_vault_data(req.message)
    return {"status": "Message sent securely", "payload": encrypted}

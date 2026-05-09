from fastapi import APIRouter
from app.services.pqc_engine import generate_kyber_keys, encrypt_vault_data, decrypt_vault_data
from pydantic import BaseModel

router = APIRouter(prefix="/vault", tags=["Quantum-Safe Vault"])

class VaultStore(BaseModel):
    data: str

class VaultRetrieve(BaseModel):
    nonce: str
    ciphertext: str

@router.post("/store")
def store_secure_data(req: VaultStore):
    return encrypt_vault_data(req.data)

@router.post("/retrieve")
def retrieve_secure_data(req: VaultRetrieve):
    pt = decrypt_vault_data(req.nonce, req.ciphertext)
    return {"data": pt}

@router.get("/keys/kyber")
def get_pqc_keys():
    return generate_kyber_keys()

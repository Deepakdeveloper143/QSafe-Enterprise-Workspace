import os
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings

# Attempt to load real PQC libraries, fallback to simulated keys if C++ tools are missing
try:
    import pqcrypto.kem.kyber512 as kyber
    import pqcrypto.sign.dilithium2 as dilithium
    PQC_AVAILABLE = True
except ImportError:
    PQC_AVAILABLE = False

def generate_kyber_keys():
    if PQC_AVAILABLE:
        public_key, secret_key = kyber.generate_keypair()
        return {"public_key": public_key.hex(), "secret_key": "HIDDEN"}
    else:
        # Fallback simulation for Windows environments without C++ build tools
        return {
            "public_key": "kyber512_pub_" + secrets.token_hex(32),
            "secret_key": "HIDDEN",
            "note": "Simulated keys (pqcrypto not available)"
        }

def generate_dilithium_keys():
    if PQC_AVAILABLE:
        public_key, secret_key = dilithium.generate_keypair()
        return {"public_key": public_key.hex(), "secret_key": "HIDDEN"}
    else:
        return {
            "public_key": "dilithium2_pub_" + secrets.token_hex(32),
            "secret_key": "HIDDEN",
            "note": "Simulated keys (pqcrypto not available)"
        }

def encrypt_vault_data(data: str):
    key = settings.VAULT_KEY.encode()[:32] # Ensure 32 bytes
    if len(key) < 32:
        key = key.ljust(32, b'0')
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data.encode(), None)
    return {"nonce": nonce.hex(), "ciphertext": ct.hex()}

def decrypt_vault_data(nonce_hex: str, ct_hex: str):
    key = settings.VAULT_KEY.encode()[:32]
    if len(key) < 32:
        key = key.ljust(32, b'0')
        
    aesgcm = AESGCM(key)
    try:
        pt = aesgcm.decrypt(bytes.fromhex(nonce_hex), bytes.fromhex(ct_hex), None)
        return pt.decode()
    except Exception as e:
        return str(e)

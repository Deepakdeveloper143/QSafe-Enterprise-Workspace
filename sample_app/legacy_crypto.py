import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_legacy_rsa_key():
    # RSA is vulnerable to Shor's algorithm on a sufficiently large quantum computer
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key

def hash_password_md5(password: str):
    # MD5 is a broken, legacy hashing algorithm
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

def hash_data_sha1(data: bytes):
    # SHA-1 is also considered weak and deprecated
    m = hashlib.sha1()
    m.update(data)
    return m.hexdigest()

if __name__ == "__main__":
    print("Generating RSA key...")
    key = generate_legacy_rsa_key()
    print("RSA Key generated.")
    
    pwd_hash = hash_password_md5("super_secret_password")
    print(f"MD5 Hash: {pwd_hash}")

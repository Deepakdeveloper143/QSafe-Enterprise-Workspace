import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Enterprise-grade Regex Patterns for Cryptographic Assets
PATTERNS = {
    "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----",
    "Generic Private Key": r"-----BEGIN (.*) PRIVATE KEY-----",
    "MD5 Usage": r"hashlib\.md5\(|md5",
    "SHA1 Usage": r"hashlib\.sha1\(|sha1",
    "Legacy RSA Call": r"rsa\.generate_private_key\(.*key_size=1024",
    "Hardcoded Password": r"password\s*=\s*['\"][^'\"]+['\"]",
    "Hardcoded Secret": r"secret_key\s*=\s*['\"][^'\"]+['\"]",
    "Hardcoded Token": r"token\s*=\s*['\"][^'\"]+['\"]"
}

def analyze_file(file_info):
    root, file = file_info
    full_path = os.path.join(root, file)
    findings = []
    try:
        with open(full_path, "r", errors="ignore") as f:
            content = f.read()
            for label, pattern in PATTERNS.items():
                if re.search(pattern, content, re.IGNORECASE):
                    severity = "Critical" if "Private Key" in label or "Password" in label else "High"
                    findings.append({
                        "asset_type": label,
                        "file": file,
                        "path": full_path,
                        "severity": severity,
                        "migration_priority": "Immediate",
                        "status": "Vulnerable (Legacy)"
                    })
    except Exception:
        pass
    return findings

def scan_directory(path: str):
    if not os.path.exists(path):
        return {"error": f"Path {path} does not exist"}

    IGNORE_DIRS = [".venv", "node_modules", "__pycache__", ".git", ".idea", "dist", "build"]
    files_to_scan = []
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.yaml', '.yml', '.conf', '.json')):
                files_to_scan.append((root, file))

    # High-Performance Parallel Execution
    all_findings = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(analyze_file, files_to_scan)
        for result in results:
            all_findings.extend(result)

    return all_findings


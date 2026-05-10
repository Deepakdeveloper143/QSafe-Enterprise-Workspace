def calculate_risk_score(cbom_findings: list):
    score = 100
    risk_register = []

    for finding in cbom_findings:
        asset = finding.get("asset_type", "").lower()
        if any(tech in asset for tech in ["rsa", "ecc", "md5", "sha1"]):
            score -= 10
            risk_register.append({
                "issue": f"Legacy cryptography detected: {finding.get('asset_type')}",
                "impact": "Vulnerable to Harvest Now, Decrypt Later (HNDL)",
                "action": "Migrate to NIST PQC (Kyber/Dilithium)"
            })
        elif any(secret in asset for secret in ["password", "secret", "token"]):
            score -= 15
            risk_register.append({
                "issue": f"Hardcoded secret detected: {finding.get('asset_type')}",
                "impact": "High risk of credential compromise",
                "action": "Move to secure vault"
            })


    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    return {
        "safety_score": score,
        "risk_register": risk_register,
        "threat_level": "Critical" if score < 50 else "High" if score < 80 else "Low"
    }

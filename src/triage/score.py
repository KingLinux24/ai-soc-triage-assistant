from typing import Any, Dict, List
from .mitre_mapping import MITRE_MAP

def score_incident(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    mitre = []
    score = 0
    for s in signals:
        key = s["signal"]
        m = MITRE_MAP.get(key)
        if not m:
            continue
        score += m["severity_weight"]
        mitre.append({
            "signal": key,
            "technique": m["technique"],
            "name": m["name"]
        })

    # Translate score to severity
    if score >= 6:
        severity = "high"
    elif score >= 3:
        severity = "medium"
    else:
        severity = "low"

    confidence = min(0.95, 0.5 + 0.1 * score)

    recommended_actions = []
    if any(m["technique"] == "T1110" for m in mitre):
        recommended_actions += [
            "Check account lockout and MFA status for impacted user",
            "Review authentication logs for the same source IP across other users",
            "Block or rate-limit suspicious source IP at the edge"
        ]
    if any(m["technique"] == "T1190" for m in mitre):
        recommended_actions += [
            "Inspect web server for suspicious requests and recent configuration changes",
            "Validate that sensitive files are not exposed and rotate any leaked secrets",
            "Check for new admin sessions and anomalous file access"
        ]

    return {
        "severity": severity,
        "confidence": round(confidence, 2),
        "mitre": mitre,
        "recommended_actions": recommended_actions
    }

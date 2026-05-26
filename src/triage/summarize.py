from typing import Any, Dict, List

def summarize_incident(incident: Dict[str, Any], triage: Dict[str, Any]) -> str:
    key = incident["key"]
    signals = incident["signals"]
    time_range = incident["time_range"]

    lines = []
    lines.append(f"Incident {incident['incident_id']} detected for host={key['host']} user={key['user']} src_ip={key['src_ip']}.")
    lines.append(f"Time window: {time_range['start']} to {time_range['end']}.")
    lines.append(f"Severity: {triage['severity']} (confidence {triage['confidence']}).")

    lines.append("Signals observed:")
    for s in signals:
        lines.append(f"- {s['signal']} (count={s.get('count', 0)})")

    if triage.get("mitre"):
        lines.append("Mapped techniques:")
        for m in triage["mitre"]:
            lines.append(f"- {m['technique']} {m['name']} (from {m['signal']})")

    if triage.get("recommended_actions"):
        lines.append("Recommended next actions:")
        for a in triage["recommended_actions"]:
            lines.append(f"- {a}")

    return "\n".join(lines)

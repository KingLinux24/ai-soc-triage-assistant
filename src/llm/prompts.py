def incident_prompt(incident: dict, triage: dict) -> str:
    return f"""
You are a SOC analyst. Write a concise incident summary with:
1) What happened
2) Why it matters
3) Most likely scenario
4) Immediate next steps
5) What to verify next

Return plain text only.

Incident:
{incident}

Triage:
{triage}
""".strip()

import json
from pathlib import Path
from typing import Any, Dict

def write_case(incident: Dict[str, Any], triage: Dict[str, Any], summary: str) -> None:
    out_dir = Path("docs/cases")
    out_dir.mkdir(parents=True, exist_ok=True)

    case = {
        "incident": incident,
        "triage": triage,
        "summary": summary
    }

    json_path = out_dir / f"{incident['incident_id']}.json"
    md_path = out_dir / f"{incident['incident_id']}.md"

    json_path.write_text(json.dumps(case, indent=2), encoding="utf-8")

    md = []
    md.append(f"# {incident['incident_id']}")
    md.append("")
    md.append("## Summary")
    md.append(summary)
    md.append("")
    md.append("## Triage")
    md.append("```json")
    md.append(json.dumps(triage, indent=2))
    md.append("```")
    md.append("")
    md.append("## Key")
    md.append("```json")
    md.append(json.dumps(incident["key"], indent=2))
    md.append("```")
    md.append("")
    md.append("## Signals")
    md.append("```json")
    md.append(json.dumps(incident["signals"], indent=2))
    md.append("```")

    md_path.write_text("\n".join(md), encoding="utf-8")

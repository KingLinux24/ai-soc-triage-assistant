import json
from pathlib import Path
from typing import Any, Dict, List

from src.triage.score import score_incident
from src.triage.summarize import summarize_incident
from src.utils.case_writer import write_case

INCIDENTS = Path("data/processed/incidents.jsonl")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

def run_pipeline(write_cases: bool = True) -> List[Dict[str, Any]]:
    incidents = read_jsonl(INCIDENTS)
    results = []

    for inc in incidents:
        triage = score_incident(inc["signals"])
        summary = summarize_incident(inc, triage)

        if write_cases:
            write_case(inc, triage, summary)

        results.append({
            "incident_id": inc["incident_id"],
            "key": inc["key"],
            "time_range": inc["time_range"],
            "triage": triage,
            "summary": summary
        })

    return results

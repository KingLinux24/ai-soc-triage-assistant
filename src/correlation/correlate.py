import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

IN_PATH = Path("data/processed/normalized_events.jsonl")
OUT_PATH = Path("data/processed/incidents.jsonl")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def parse_ts(ts: str) -> datetime:
    # expecting "...Z"
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def main():
    events = list(read_jsonl(IN_PATH))
    events.sort(key=lambda e: e["timestamp"])

    buckets: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for e in events:
        key = (e.get("host") or "unknown", e.get("user") or "unknown", e.get("src_ip") or "unknown")
        buckets[key].append(e)

    incidents = []
    for (host, user, src_ip), evts in buckets.items():
        if len(evts) < 5:
            continue

        # Simple pattern detection
        failures = [e for e in evts if e["event_type"] == "auth_failure"]
        successes = [e for e in evts if e["event_type"] == "auth_success"]
        suspicious_web = [e for e in evts if e["event_type"] == "web_access" and e.get("raw", {}).get("path") in {"/.env", "/backup.zip", "/admin"}]

        signals = []
        if len(failures) >= 10:
            signals.append({"signal": "possible_bruteforce", "count": len(failures)})
        if len(failures) >= 10 and len(successes) >= 1:
            signals.append({"signal": "bruteforce_then_success", "count": len(successes)})
        if len(suspicious_web) >= 1:
            signals.append({"signal": "suspicious_web_paths", "count": len(suspicious_web)})

        if not signals:
            continue

        start = min(parse_ts(e["timestamp"]) for e in evts).isoformat()
        end = max(parse_ts(e["timestamp"]) for e in evts).isoformat()

        incidents.append({
            "incident_id": f"INC-{abs(hash((host, user, src_ip, start))) % 10_000_000:07d}",
            "key": {"host": host, "user": user, "src_ip": src_ip},
            "time_range": {"start": start, "end": end},
            "signals": signals,
            "events": evts
        })

    with OUT_PATH.open("w", encoding="utf-8") as f:
        for inc in incidents:
            f.write(json.dumps(inc) + "\n")

if __name__ == "__main__":
    main()

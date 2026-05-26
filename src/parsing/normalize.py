import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

IN_PATH = Path("data/raw/sample_logs.jsonl")
OUT_PATH = Path("data/processed/normalized_events.jsonl")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def severity_from_event(evt: Dict[str, Any]) -> str | None:
    et = evt.get("event_type", "")
    if et in {"auth_failure"}:
        return "medium"
    if et in {"auth_success"} and evt.get("src_ip", "").startswith(("198.", "203.", "192.")):
        return "high"
    if et in {"web_access"} and evt.get("path") in {"/.env", "/backup.zip"}:
        return "high"
    return None

def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp": raw.get("timestamp"),
        "source": raw.get("source", "other"),
        "host": raw.get("host"),
        "user": raw.get("user"),
        "src_ip": raw.get("src_ip"),
        "dst_ip": raw.get("dst_ip"),
        "event_type": raw.get("event_type", "unknown"),
        "action": raw.get("path") or raw.get("message"),
        "status": raw.get("status"),
        "severity_hint": severity_from_event(raw),
        "raw": raw
    }

def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

def main():
    rows = [normalize(r) for r in read_jsonl(IN_PATH)]
    write_jsonl(OUT_PATH, rows)

if __name__ == "__main__":
    main()

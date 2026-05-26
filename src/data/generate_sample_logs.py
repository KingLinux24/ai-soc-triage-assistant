import json
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path("data/raw/sample_logs.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

USERS = ["alice", "bob", "carol", "dave"]
HOSTS = ["wkst-01", "wkst-02", "srv-web-01", "srv-db-01"]
IPS = ["10.0.1.10", "10.0.1.11", "10.0.2.20", "10.0.9.99"]
EXT_IPS = ["198.51.100.10", "203.0.113.55", "192.0.2.77"]

def ts(base, minutes):
    return (base + timedelta(minutes=minutes)).isoformat() + "Z"

def main():
    base = datetime.utcnow() - timedelta(days=1)
    rows = []

    # Benign background
    for i in range(200):
        evt = {
            "source": random.choice(["auth", "web", "fw"]),
            "timestamp": ts(base, i),
            "host": random.choice(HOSTS),
            "user": random.choice(USERS),
            "src_ip": random.choice(IPS),
            "dst_ip": random.choice(IPS),
            "message": "normal activity",
            "event_type": "info",
            "status": "success"
        }
        rows.append(evt)

    # Brute force pattern
    attacker_ip = random.choice(EXT_IPS)
    target_user = "alice"
    target_host = "srv-web-01"
    for i in range(30):
        evt = {
            "source": "auth",
            "timestamp": ts(base, 300 + i),
            "host": target_host,
            "user": target_user,
            "src_ip": attacker_ip,
            "dst_ip": "10.0.2.20",
            "message": "Failed login attempt",
            "event_type": "auth_failure",
            "status": "failure"
        }
        rows.append(evt)

    # Successful login after failures
    rows.append({
        "source": "auth",
        "timestamp": ts(base, 340),
        "host": target_host,
        "user": target_user,
        "src_ip": attacker_ip,
        "dst_ip": "10.0.2.20",
        "message": "Successful login",
        "event_type": "auth_success",
        "status": "success"
    })

    # Suspicious web access after login
    for i in range(5):
        rows.append({
            "source": "web",
            "timestamp": ts(base, 345 + i),
            "host": target_host,
            "user": target_user,
            "src_ip": attacker_ip,
            "dst_ip": "10.0.2.20",
            "http_method": "GET",
            "path": random.choice(["/admin", "/.env", "/backup.zip", "/wp-admin"]),
            "status_code": random.choice([200, 401, 403]),
            "message": "web request",
            "event_type": "web_access",
            "status": "info"
        })

    random.shuffle(rows)

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()

from fastapi import FastAPI
from src.api.pipeline import run_pipeline

app = FastAPI(title="AI SOC Triage Assistant", version="1.0")

@app.get("/run")
def run():
    results = run_pipeline(write_cases=True)
    return {"count": len(results), "results": results}

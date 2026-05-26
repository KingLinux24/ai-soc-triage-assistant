import sys
from pathlib import Path

# 1. THIS PATH LOGIC MUST GO FIRST
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 2. NOW IT IS SAFE TO IMPORT FROM SRC
import streamlit as st
from src.api.pipeline import run_pipeline

# Configure the page title and title header
st.title("AI SOC Analyst: Log Summarization and Incident Triage")

# Execution trigger button
if st.button("Run pipeline on sample logs"):
    results = run_pipeline(write_cases=True)
    st.write(f"Incidents generated: {len(results)}")
    
    # Loop through individual incident metrics and render elements
    for r in results:
        st.subheader(r["incident_id"])
        st.json(r["triage"])
        st.text(r["summary"])

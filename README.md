# Disk Scheduling Visualizer (Streamlit)

## Overview
Interactive simulator for disk scheduling algorithms: FCFS, SSTF, SCAN, LOOK.
Shows head movement graphs and metrics (total movement, average seek, throughput).

## Run locally (VS Code terminal)
1. Create and activate a virtual environment:
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate
   - Windows (PowerShell):
     python -m venv venv
     .\\venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run app.py

4. Open http://localhost:8501 in a browser (Streamlit usually opens automatically).

## Demo Inputs
- Example 1: Requests `98, 183, 37, 122, 14, 124, 65, 67`, Head `53`
- Example 2: Requests `55 58 39 18 90 160 150 38`, Head `50`

## Notes
- This is a simulation for learning; it does not change real OS disk schedulers.

# pages/04_History.py
import streamlit as st
import pandas as pd
from utils import fetch_history, history_to_csv

st.set_page_config(page_title="History", layout="wide")
st.title("📁 Saved Runs History")

rows = fetch_history()
if not rows:
    st.info("No saved runs yet. Save runs from Simulation page.")
else:
    df = pd.DataFrame(rows, columns=["id","name","requests","head","algorithm","direction","disk_start","disk_end","seek_ms","total_movement","avg_seek","throughput","timestamp"])
    st.dataframe(df)
    csv = history_to_csv(rows)
    st.download_button("⬇️ Download Full History CSV", csv, file_name="history.csv")

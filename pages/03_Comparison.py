# pages/03_Comparison.py
import streamlit as st
import pandas as pd
import plotly.express as px
from algorithms import fcfs, sstf, scan, look, c_scan, c_look
from utils import compute_disk_metrics

st.set_page_config(page_title="Comparison", layout="wide")
st.title("⚔️ Compare All Algorithms")

# Check inputs
if 'requests' not in st.session_state:
    st.error("No input found. Go to Input page and submit requests.")
    st.stop()

requests = st.session_state['requests']
head = st.session_state['head']
direction = st.session_state['direction']
disk_start = st.session_state['disk_start']
disk_end = st.session_state['disk_end']
seek_time_ms = st.session_state['seek_time_ms']

algos = ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK"]
results = []
for a in algos:
    if a == "FCFS":
        res = fcfs(requests, head)
    elif a == "SSTF":
        res = sstf(requests, head)
    elif a == "SCAN":
        res = scan(requests, head, direction=direction, disk_start=disk_start, disk_end=disk_end)
    elif a == "LOOK":
        res = look(requests, head, direction=direction)
    elif a == "C-SCAN":
        res = c_scan(requests, head, disk_start=disk_start, disk_end=disk_end)
    elif a == "C-LOOK":
        res = c_look(requests, head)
    metrics = compute_disk_metrics(res['path'], len(requests), seek_time_per_cylinder_ms=seek_time_ms)
    results.append((a, res, metrics))

# build DataFrame
comp_df = pd.DataFrame([{"Algorithm": a, "TotalMovement": m["total_head_movement"], "AvgSeek": m["average_seek_distance"], "Throughput": m["throughput_req_per_sec"]} for a, r, m in results])
st.dataframe(comp_df.sort_values("TotalMovement"))

col1, col2 = st.columns(2)
col1.plotly_chart(px.bar(comp_df, x="Algorithm", y="TotalMovement", title="Total Head Movement Comparison", template="plotly_dark"), use_container_width=True)
col2.plotly_chart(px.bar(comp_df, x="Algorithm", y="Throughput", title="Throughput Comparison", template="plotly_dark"), use_container_width=True)

st.markdown("---")
st.subheader("Individual head movement graphs")
cols = st.columns(2)
for idx, (a, r, m) in enumerate(results):
    df = pd.DataFrame({"Step": list(range(len(r['path']))), "Cylinder": r['path']})
    cols[idx % 2].plotly_chart(px.line(df, x="Step", y="Cylinder", title=f"{a} - Path", template="plotly_dark"), use_container_width=True)

# Download comparison table
csv_buf = comp_df.to_csv(index=False)
st.download_button("⬇️ Download Comparison CSV", csv_buf, file_name="comparison.csv")

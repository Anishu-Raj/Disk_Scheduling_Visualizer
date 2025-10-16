# app.py (Enhanced Dashboard UI)
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from algorithms import fcfs, sstf, scan, look, c_scan, c_look
from utils import parse_requests, compute_disk_metrics, init_db, save_run, fetch_history, history_to_csv

# --- Page Setup ---
st.set_page_config(page_title="Disk Scheduling Visualizer", layout="wide")
init_db()

# --- Custom Page Style ---
st.markdown("""
    <style>
    body {
        background-color: #0f172a;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
    }
    .big-title {
        font-size: 40px !important;
        color: #38bdf8;
        text-align: center;
        font-weight: bold;
    }
    .subtext {
        text-align: center;
        font-size: 18px;
        color: #94a3b8;
    }
    .metric-card {
        background: #1e293b;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<p class="big-title">💿 Disk Scheduling Visualizer — Phase 3</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Compare & Visualize OS Disk Scheduling Algorithms in Real-Time</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    requests_text = st.text_area("Enter Disk Requests:", placeholder="e.g. 98, 183, 37, 122, 14, 124, 65, 67")
    head = st.number_input("Initial Head Position:", min_value=0, value=50, step=1)
    algo = st.selectbox("Select Algorithm:", ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK", "COMPARE ALL"])
    direction = st.selectbox("Direction (for SCAN/LOOK):", ["right", "left"])
    disk_start = st.number_input("Disk Start Cylinder:", value=0)
    disk_end = st.number_input("Disk End Cylinder:", value=199)
    seek_time_ms = st.number_input("Seek Time per Cylinder (ms):", value=1.0, step=0.1)
    animate = st.checkbox("Animate Head Movement", value=True)
    anim_speed = st.slider("Animation Speed (sec per step)", 0.05, 0.8, 0.3, 0.05)
    st.markdown("---")
    st.subheader("💾 History & Save")
    save_name = st.text_input("Run Name (optional):", value="")
    run_btn = st.button("🚀 Run Simulation")

# --- Helper Function ---
def run_algorithm(name, requests, head, direction, disk_start, disk_end):
    if name == "FCFS": return fcfs(requests, head)
    if name == "SSTF": return sstf(requests, head)
    if name == "SCAN": return scan(requests, head, direction=direction, disk_start=disk_start, disk_end=disk_end)
    if name == "LOOK": return look(requests, head, direction=direction)
    if name == "C-SCAN": return c_scan(requests, head, disk_start=disk_start, disk_end=disk_end)
    if name == "C-LOOK": return c_look(requests, head)

# --- Tabs for UI Sections ---
tabs = st.tabs(["🏠 Home", "📊 Simulation", "⚔️ Comparison", "📁 History"])

# --- Home Tab ---
with tabs[0]:
    st.markdown("""
        <h3>Welcome!</h3>
        <p>This is an interactive simulation tool to visualize how different disk scheduling algorithms work in Operating Systems.</p>
        <p>You can enter your own disk request sequence, choose an algorithm, and see how the disk head moves step-by-step.</p>
        <ul>
            <li>Supports FCFS, SSTF, SCAN, LOOK, C-SCAN, and C-LOOK</li>
            <li>Compare all algorithms side-by-side</li>
            <li>Animated visualization with performance metrics</li>
            <li>Save and export run history</li>
        </ul>
    """, unsafe_allow_html=True)

# --- Simulation Tab ---
with tabs[1]:
    if run_btn:
        try:
            requests = parse_requests(requests_text)
            if not requests:
                st.error("⚠️ Please enter valid disk requests.")
            else:
                if algo == "COMPARE ALL":
                    st.warning("Use the 'Comparison' tab for full algorithm comparison.")
                else:
                    res = run_algorithm(algo, requests, head, direction, disk_start, disk_end)
                    metrics = compute_disk_metrics(res["path"], len(requests), seek_time_per_cylinder_ms=seek_time_ms)
                    # --- Metric Cards ---
                    col1, col2, col3 = st.columns(3)
                    with col1: st.markdown(f"<div class='metric-card'><h4>Total Head Movement</h4><h2>{metrics['total_head_movement']}</h2></div>", unsafe_allow_html=True)
                    with col2: st.markdown(f"<div class='metric-card'><h4>Avg Seek Distance</h4><h2>{metrics['average_seek_distance']}</h2></div>", unsafe_allow_html=True)
                    with col3: st.markdown(f"<div class='metric-card'><h4>Throughput (req/sec)</h4><h2>{metrics['throughput_req_per_sec']}</h2></div>", unsafe_allow_html=True)

                    st.markdown("---")
                    st.subheader("📈 Disk Head Movement")

                    plot_placeholder = st.empty()
                    path_df = pd.DataFrame({"Step": list(range(len(res["path"]))), "Cylinder": res["path"]})
                    if animate:
                        path_so_far = []
                        for i in range(len(res["path"])):
                            path_so_far.append({"Step": i, "Cylinder": res["path"][i]})
                            df_now = pd.DataFrame(path_so_far)
                            fig = px.line(df_now, x="Step", y="Cylinder", markers=True, title=f"{algo} Head Movement", template="plotly_dark")
                            fig.update_traces(line_color="#38bdf8", marker=dict(size=10, color="#22d3ee"))
                            plot_placeholder.plotly_chart(fig, use_container_width=True)
                            time.sleep(anim_speed)
                    else:
                        fig = px.line(path_df, x="Step", y="Cylinder", markers=True, title=f"{algo} Head Movement", template="plotly_dark")
                        fig.update_traces(line_color="#38bdf8", marker=dict(size=10, color="#22d3ee"))
                        st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Simulation Complete!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Comparison Tab ---
with tabs[2]:
    if run_btn and algo == "COMPARE ALL":
        algos = ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK"]
        results = []
        for a in algos:
            res = run_algorithm(a, parse_requests(requests_text), head, direction, disk_start, disk_end)
            metrics = compute_disk_metrics(res["path"], len(parse_requests(requests_text)), seek_time_per_cylinder_ms=seek_time_ms)
            results.append((a, metrics))

        comp_df = pd.DataFrame([
            {"Algorithm": a, "Total Movement": m["total_head_movement"], "Avg Seek": m["average_seek_distance"], "Throughput": m["throughput_req_per_sec"]}
            for a, m in results
        ])

        st.markdown("### ⚔️ Algorithm Performance Comparison")
        st.dataframe(comp_df)

        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(comp_df, x="Algorithm", y="Total Movement", color="Algorithm", title="Total Head Movement"), use_container_width=True)
        c2.plotly_chart(px.bar(comp_df, x="Algorithm", y="Throughput", color="Algorithm", title="Throughput"), use_container_width=True)

        st.success("✅ Comparison Complete — Check which algorithm performs best!")

# --- History Tab ---
with tabs[3]:
    st.subheader("📁 Saved Runs History")
    if st.button("🔄 Load History"):
        rows = fetch_history()
        if rows:
            hist_df = pd.DataFrame(rows, columns=["id","name","requests","head","algorithm","direction","disk_start","disk_end","seek_ms","total_movement","avg_seek","throughput","timestamp"])
            st.dataframe(hist_df)
            csv_data = history_to_csv(rows)
            st.download_button("⬇️ Download History CSV", csv_data, file_name="history.csv")
        else:
            st.info("No saved runs yet.")

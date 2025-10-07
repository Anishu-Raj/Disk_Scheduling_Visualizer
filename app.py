# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

from algorithms import fcfs, sstf, scan, look
from utils import parse_requests, compute_disk_metrics

# App configuration
st.set_page_config(page_title="Disk Scheduling Visualizer", layout="wide")
st.title("🟦 Disk Scheduling Visualizer")
st.markdown("Interactive simulation for FCFS, SSTF, SCAN, and LOOK algorithms in Operating Systems.")

# Sidebar inputs
with st.sidebar:
    st.header("Input Parameters 🧩")
    st.markdown("Enter your own values below:")

    req_text = st.text_area("Enter Request Sequence (comma or space separated):", 
                            placeholder="Example: 98, 183, 37, 122, 14, 124, 65, 67")

    head = st.number_input("Enter Starting Head Position:", min_value=0, value=50, step=1)

    algo = st.selectbox("Choose Disk Scheduling Algorithm:", ["FCFS", "SSTF", "SCAN", "LOOK"])
    
    if algo in ["SCAN", "LOOK"]:
        direction = st.selectbox("Direction of Head Movement:", ["right", "left"])
    else:
        direction = "right"

    if algo == "SCAN":
        disk_start = st.number_input("Disk Start Cylinder:", value=0, step=1)
        disk_end = st.number_input("Disk End Cylinder:", value=199, step=1)
    else:
        disk_start, disk_end = 0, 199

    seek_time_ms = st.number_input("Seek Time per Cylinder (ms):", value=1.0, step=0.1)

    run = st.button("Run Simulation 🚀")

# Main output area
st.markdown("---")
st.subheader("Simulation Output 🎯")

if run:
    try:
        # Parse input
        requests = parse_requests(req_text)
        if not requests:
            st.error("⚠️ Please enter at least one valid request number.")
        else:
            # Run the selected algorithm
            if algo == "FCFS":
                res = fcfs(requests, head)
            elif algo == "SSTF":
                res = sstf(requests, head)
            elif algo == "SCAN":
                res = scan(requests, head, direction=direction, disk_start=disk_start, disk_end=disk_end)
            else:
                res = look(requests, head, direction=direction)

            # Compute performance metrics
            metrics = compute_disk_metrics(res["path"], len(requests), seek_time_per_cylinder_ms=seek_time_ms)

            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Head Movement (Cylinders)", metrics["total_head_movement"])
            col2.metric("Average Seek Distance (Cylinders)", metrics["average_seek_distance"])
            col3.metric("Throughput (Requests/sec)", metrics["throughput_req_per_sec"])

            # Display servicing order
            st.markdown("### Servicing Order Table 📋")
            df = pd.DataFrame({
                "Order": list(range(1, len(res["order"]) + 1)),
                "Cylinder Number": res["order"]
            })
            st.table(df)

            # Plot disk head movement graph
            st.markdown("### Disk Head Movement Graph 📊")
            path = res["path"]
            plot_df = pd.DataFrame({"Step": list(range(len(path))), "Cylinder": path})
            fig = px.line(plot_df, x="Step", y="Cylinder", markers=True, 
                          title=f"{algo} - Disk Head Movement Visualization",
                          template="plotly_dark")
            fig.update_traces(marker=dict(size=10, color="cyan"))
            st.plotly_chart(fig, use_container_width=True)

            # Additional information
            st.success(f"✅ Simulation Complete! Total Head Movement = {metrics['total_head_movement']} cylinders.")
            st.info("💡 Tip: Try changing request sequences and algorithms to see how the results vary.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("🧠 Enter your input in the sidebar and click **Run Simulation 🚀** to start.")

st.markdown("---")
st.caption("Developed using Python, Streamlit, and Plotly — for Operating Systems PBL Project 💻")

# pages/02_Simulation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from algorithms import fcfs, sstf, scan, look, c_scan, c_look
from utils import compute_disk_metrics, save_run

st.set_page_config(page_title="Simulation", layout="wide")
st.title("📈 Simulation")

# Validate session state
required_keys = ['requests', 'head', 'algo', 'direction', 'disk_start', 'disk_end', 'seek_time_ms', 'animate', 'anim_speed']
for k in required_keys:
    if k not in st.session_state:
        st.error("Input parameters not found. Please go to Input page and submit your inputs.")
        st.stop()

requests = st.session_state['requests']
head = st.session_state['head']
algo = st.session_state['algo']
direction = st.session_state['direction']
disk_start = st.session_state['disk_start']
disk_end = st.session_state['disk_end']
seek_time_ms = st.session_state['seek_time_ms']
animate = st.session_state['animate']
anim_speed = st.session_state['anim_speed']
save_name = st.session_state.get('save_name', '')

def run_algorithm_by_name(name):
    name = name.upper()
    if name == "FCFS":
        return fcfs(requests, head)
    if name == "SSTF":
        return sstf(requests, head)
    if name == "SCAN":
        return scan(requests, head, direction=direction, disk_start=disk_start, disk_end=disk_end)
    if name == "LOOK":
        return look(requests, head, direction=direction)
    if name == "C-SCAN":
        return c_scan(requests, head, disk_start=disk_start, disk_end=disk_end)
    if name == "C-LOOK":
        return c_look(requests, head)
    raise ValueError("Unknown algorithm")

if algo == "COMPARE ALL":
    st.info("You selected 'COMPARE ALL'. Please go to the Comparison page (Pages -> 03_Comparison) to view comparisons.")
else:
    try:
        res = run_algorithm_by_name(algo)
        metrics = compute_disk_metrics(res["path"], len(requests), seek_time_per_cylinder_ms=seek_time_ms)
        # metric cards
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Head Movement (cyl)", metrics['total_head_movement'])
        c2.metric("Avg Seek Distance (cyl)", metrics['average_seek_distance'])
        c3.metric("Throughput (req/sec)", metrics['throughput_req_per_sec'])

        st.markdown("---")
        st.subheader("Servicing Order")
        st.table(pd.DataFrame({"Step": list(range(1,len(res["order"])+1)), "Cylinder": res["order"]}))

        st.markdown("---")
        st.subheader("Disk Head Movement")

        plot_placeholder = st.empty()

        # narration placeholder
        narration = st.empty()

        path = res["path"]
        # animate or static
        if animate:
            path_so_far = []
            for i in range(len(path)):
                path_so_far.append({"Step": i, "Cylinder": path[i]})
                df_now = pd.DataFrame(path_so_far)
                fig = px.line(df_now, x="Step", y="Cylinder", markers=True, title=f"{algo} - Animated", template="plotly_dark")
                fig.update_traces(line_color="#38bdf8", marker=dict(size=10, color="#22d3ee"))
                fig.update_yaxes(range=[min(path)-5, max(path)+5])
                plot_placeholder.plotly_chart(fig, use_container_width=True)
                # narration:
                if i > 0:
                    from_pos = path[i-1]; to_pos = path[i]
                    dist = abs(to_pos - from_pos)
                    narration.markdown(f"➡️ Step {i}: Move head from **{from_pos}** to **{to_pos}** (distance = {dist})")
                else:
                    narration.markdown(f"Start at head position: **{path[0]}**")
                time.sleep(anim_speed)
        else:
            df_full = pd.DataFrame({"Step": list(range(len(path))), "Cylinder": path})
            fig = px.line(df_full, x="Step", y="Cylinder", markers=True, title=f"{algo} - Head Movement", template="plotly_dark")
            fig.update_traces(line_color="#38bdf8", marker=dict(size=10, color="#22d3ee"))
            fig.update_yaxes(range=[min(path)-5, max(path)+5])
            st.plotly_chart(fig, use_container_width=True)

        st.success("✅ Simulation complete")
        # Save to DB option
        if st.button("💾 Save Run to History"):
            name = save_name if save_name else f"{algo}_run"
            save_run(name, st.session_state['requests_text'], head, algo, direction, disk_start, disk_end, seek_time_ms, metrics)
            st.success("Saved run to history.")

        # allow download of path CSV
        path_df = pd.DataFrame({"Step": list(range(len(path))), "Cylinder": path})
        csv_data = path_df.to_csv(index=False)
        st.download_button("⬇️ Download Path CSV", csv_data, file_name="run_path.csv")

    except Exception as e:
        st.error(f"Error running algorithm: {e}")

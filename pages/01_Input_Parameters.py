# pages/01_Input_Parameters.py
import streamlit as st
from utils import parse_requests

st.set_page_config(page_title="Input Parameters", layout="wide")

st.title("⚙️ Input Parameters")

with st.form("input_form"):
    req_text = st.text_area("Enter Disk Requests (comma or space separated):", placeholder="98, 183, 37, 122, 14, 124, 65, 67")
    head = st.number_input("Initial Head Position:", min_value=0, value=50, step=1)
    algo = st.selectbox("Choose Algorithm:", ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK", "COMPARE ALL"])
    direction = st.selectbox("Direction (for SCAN/LOOK):", ["right", "left"])
    disk_start = st.number_input("Disk Start Cylinder:", value=0, step=1)
    disk_end = st.number_input("Disk End Cylinder:", value=199, step=1)
    seek_time_ms = st.number_input("Seek time per cylinder (ms):", value=1.0, step=0.1)
    animate = st.checkbox("Animate head movement in Simulation", value=True)
    anim_speed = st.slider("Animation speed (sec per step)", 0.05, 1.0, 0.25, 0.05)
    save_name = st.text_input("Optional: Save run as (name):", value="")
    submitted = st.form_submit_button("➡️ Proceed to Simulation")

if submitted:
    try:
        requests = parse_requests(req_text)
        if not requests:
            st.error("Please enter at least one valid request.")
        else:
            # store in session state
            st.session_state['requests_text'] = req_text
            st.session_state['requests'] = requests
            st.session_state['head'] = int(head)
            st.session_state['algo'] = algo
            st.session_state['direction'] = direction
            st.session_state['disk_start'] = int(disk_start)
            st.session_state['disk_end'] = int(disk_end)
            st.session_state['seek_time_ms'] = float(seek_time_ms)
            st.session_state['animate'] = bool(animate)
            st.session_state['anim_speed'] = float(anim_speed)
            st.session_state['save_name'] = save_name.strip()
            st.success("Inputs saved. Now go to the Simulation page (Pages menu -> 02_Simulation).")
    except Exception as e:
        st.error(f"Invalid input: {e}")

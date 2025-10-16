# Home.py
import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #38bdf8;
            font-size: 50px;
            font-weight: bold;
            margin-top: 50px;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 22px;
            margin-top: -10px;
        }
        .desc {
            text-align: center;
            color: #cbd5e1;
            font-size: 18px;
            margin-top: 30px;
            line-height: 1.6;
        }
        .start-btn {
            display: block;
            width: 280px;
            margin: 40px auto;
            background-color: #2563eb;
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            padding: 15px 0;
            border-radius: 10px;
            text-decoration: none;
            transition: 0.3s;
        }
        .start-btn:hover {
            background-color: #1d4ed8;
            transform: scale(1.05);
        }
        .footer {
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-top: 80px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Main Content ---
st.markdown("<h1 class='main-title'>💿 Disk Scheduling Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Phase 3 — Operating Systems Project</p>", unsafe_allow_html=True)

st.markdown("""
<p class='desc'>
This project is a <b>real-time simulation and visualization tool</b> that demonstrates how 
different <b>Disk Scheduling Algorithms</b> work in Operating Systems.<br><br>
It helps students understand how the <b>disk head</b> moves between requests, 
and compares performance of algorithms like <b>FCFS, SSTF, SCAN, LOOK, C-SCAN</b>, and <b>C-LOOK</b>.
</p>
""", unsafe_allow_html=True)

# --- Start Button ---
if st.button("🚀 Start Simulation"):
    st.switch_page("pages/01_Input_Parameters.py")

st.markdown("<p class='footer'>Developed by: <b>Anishu Raj, Anushree Verma, Tulsi Dubey, Vaani Bisht</b><br>Graphic Era University</p>", unsafe_allow_html=True)

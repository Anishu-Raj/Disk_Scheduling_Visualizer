# Home.py (Landing page)
import streamlit as st

st.set_page_config(page_title="Disk Scheduling Visualizer", layout="wide")

# ---- Sidebar navigation (simple links) ----
# This keeps the left sidebar visible for navigation, but without the input controls.
with st.sidebar:
    st.title("Pages")
    if st.button("🏠 Home"):
        st.experimental_rerun()  # refresh to stay on home
    if st.button("⚙️ Input Parameters"):
        st.switch_page("01_Input_Parameters")
    if st.button("📈 Simulation"):
        st.switch_page("02_Simulation")
    if st.button("⚔️ Comparison"):
        st.switch_page("03_Comparison")
    if st.button("📁 History"):
        st.switch_page("04_History")

# ---- Styling & heading placement ----
st.markdown(
    """
    <style>
      .main-heading { margin-top: 80px !important; color: #4FC3F7; font-size:48px; text-align:center; font-weight:700; }
      .welcome { text-align:center; color: #ffffff; font-size:26px; margin-top:20px; }
      .desc { text-align:center; color:#E0E0E0; font-size:18px; width:70%; margin:auto; margin-top:16px; }
      .center-btn { display:flex; justify-content:center; margin-top:32px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<div class='main-heading'>Disk Scheduling Visualizer — Phase 3</div>", unsafe_allow_html=True)
st.markdown("<div class='welcome'>Welcome!</div>", unsafe_allow_html=True)
st.markdown("<div class='desc'>This is an interactive simulation tool to visualize how different disk scheduling algorithms work in Operating Systems.</div>", unsafe_allow_html=True)

# Centered start button
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("➡ Start Simulation", use_container_width=True):
        st.session_state['from_home'] = True
        st.switch_page("01_Input_Parameters")

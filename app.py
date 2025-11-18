import streamlit as st

st.set_page_config(page_title="Disk Scheduling Visualizer", layout="wide")

# ---- Custom CSS for Animated Professional UI ----
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.hero-container {
    text-align: center;
    margin-top: 120px;
    animation: fadeIn 1.4s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-size: 60px;
    color: #4FC3F7;
    font-weight: 800;
    text-shadow: 0px 0px 25px #38bdf84a;
}

.hero-subtitle {
    font-size: 22px;
    margin-top: -10px;
    color: #cbd5e1;
}

.description-box {
    width: 60%;
    margin: auto;
    margin-top: 30px;
    padding: 25px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 18px;
    box-shadow: 0px 4px 20px rgba(56, 189, 248, 0.10);
    backdrop-filter: blur(5px);
    animation: fadeIn 1.8s ease-in-out;
}

.desc-text {
    font-size: 19px;
    color: #e2e8f0;
    line-height: 1.5;
}

.start-button-container {
    display: flex;
    justify-content: center;
    margin-top: 40px;
}

.start-button {
    background: linear-gradient(90deg, #38bdf8, #0ea5e9);
    padding: 15px 40px;
    border-radius: 50px;
    font-size: 22px;
    font-weight: 700;
    color: white;
    border: none;
    box-shadow: 0 0 15px #38bdf84d;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}

.start-button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 25px #38bdf89c;
}

.page-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    width: 70%;
    margin: 60px auto 0;
    gap: 20px;
}

.page-card {
    padding: 18px;
    background: #1e293b;
    border-radius: 15px;
    text-align: center;
    cursor: pointer;
    transition: 0.2s ease;
    color: #bae6fd;
    font-size: 18px;
    border: 1px solid #334155;
}

.page-card:hover {
    background: #38bdf81c;
    transform: translateY(-4px);
    border-color: #38bdf8;
}

</style>
""", unsafe_allow_html=True)

# ---- Hero Section ----
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Disk Scheduling Visualizer</div>
    <div class="hero-subtitle">Understand, Compare, and Animate OS Disk Scheduling Algorithms</div>
</div>
""", unsafe_allow_html=True)

# ---- Description Section ----
st.markdown("""
<div class="description-box">
    <p class="desc-text">
        This tool helps to visualize and compare advanced disk scheduling algorithms 
        used inside modern Operating Systems. Enter your disk request patterns, 
        animate head movement, study performance metrics, and analyze how each 
        scheduling technique behaves with real-time simulation.
    </p>
</div>
""", unsafe_allow_html=True)

# ---- Start Button ----
st.markdown("<div class='start-button-container'>", unsafe_allow_html=True)
if st.button(" Start Simulation", key="start", help="Begin Input Setup"):
    st.switch_page("pages/01_Input_Parameters.py")

st.markdown("</div>", unsafe_allow_html=True)

# ---- Navigation Grid ----
st.markdown("""
<div class="page-grid">
    <div class="page-card" onclick="window.location.href = '01_Input_Parameters';">⚙️ Input Parameters</div>
    <div class="page-card" onclick="window.location.href = '02_Simulation';">📈 Simulation</div>
    <div class="page-card" onclick="window.location.href = '03_Comparison';">⚔️ Comparison</div>
    <div class="page-card" onclick="window.location.href = '04_History';">📁 History</div>
</div>
""", unsafe_allow_html=True)

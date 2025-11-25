import streamlit as st
import time

st.set_page_config(
    page_title="AURAK Traffic Control",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

AURAK_NAVY = "#002D56"
AURAK_GOLD = "#BFA15F"
BUTTON_ORANGE = "#FF8C00" 
BUTTON_HOVER = "#E67E00"
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; color: #000000; }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{ color: #333333; }}
    
    [data-testid="stSidebar"] {{ background-color: {AURAK_NAVY}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: #004080 !important;
        color: white !important;
        border: 1px solid {AURAK_GOLD};
        border-radius: 5px;
    }}
    .stSelectbox div[data-baseweb="select"] span {{
        color: white !important;
    }}
    ul[data-baseweb="menu"] {{
        background-color: {AURAK_NAVY} !important;
    }}
    li[data-baseweb="option"] {{
        color: white !important;
    }}
    .stSelectbox svg {{
        fill: {AURAK_GOLD} !important;
    }}

    div.stButton > button {{
        background-color: {BUTTON_ORANGE};
        color: white !important;
        border: none;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }}
    div.stButton > button:hover {{
        background-color: {BUTTON_HOVER};
        color: white !important;
        border: 2px solid #333;
    }}
    
    [data-testid="stMetricLabel"] {{ color: #555 !important; }}
    [data-testid="stMetricValue"] {{ color: #000 !important; }}
    </style>
""", unsafe_allow_html=True)

def render_game_view(scenario):
    bg_color = "#87CEEB" 
    road_fill = "#343a40" 
    line_stroke = "#ffffff"
    grass_color = "#4CAF50"
    
    traffic_content = ""
    
    dim_red = "#330000"
    dim_yellow = "#333300"
    dim_green = "#003300"
    
    l_red = dim_red
    l_yellow = dim_yellow
    l_green = dim_green
    
    if scenario == "Scenario C: Icy Road":
        road_fill = "#dbeff9" 
        line_stroke = "#2196f3"
        bg_color = "#b3e5fc"
        grass_color = "#e3f2fd"
        
        l_red = "#FF0000"
        
        traffic_content = """
            <text x="500" y="200" font-size="80">🚛</text>
            <text x="250" y="220" font-size="50">❄️</text>
            <text x="200" y="210" font-size="70">🚑</text>
            <text x="580" y="200" font-size="40">💨</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="orange" stroke-width="2"/>
            <text x="290" y="58" font-family="Arial" font-weight="bold" fill="orange" font-size="20">⚠️ ICE HAZARD DETECTED</text>
        """
        
    elif scenario == "Scenario B: VIP Convoy":
        l_red = "#FF0000"
        
        traffic_content = """
            <text x="400" y="200" font-size="90">🚓</text>
            <text x="550" y="200" font-size="90">🚓</text>
            <text x="250" y="200" font-size="80">🚗</text>
            <text x="100" y="200" font-size="80">🚑</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="red" stroke-width="2"/>
            <text x="310" y="58" font-family="Arial" font-weight="bold" fill="red" font-size="20">🔴 BLOCKED FOR VIP</text>
        """
        
    else:
        l_green = "#00FF00"
        
        traffic_content = """
            <text x="50" y="200" font-size="80">🚗</text>
            <text x="350" y="200" font-size="80">🚙</text>
            <text x="650" y="200" font-size="80">🚕</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="green" stroke-width="2"/>
            <text x="300" y="58" font-family="Arial" font-weight="bold" fill="green" font-size="20">🟢 FLOWING NORMALLY</text>
        """

    svg = f"""
    <svg width="100%" height="320" viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background-color: {bg_color}; border-radius: 10px; border: 4px solid {AURAK_NAVY};">
    <rect x="0" y="0" width="100%" height="320" fill="{bg_color}" />
    <rect x="0" y="150" width="100%" height="170" fill="{grass_color}" />
    <rect x="0" y="140" width="100%" height="140" fill="{road_fill}" stroke="#555" stroke-width="2"/>
    <line x1="0" y1="210" x2="800" y2="210" stroke="{line_stroke}" stroke-width="5" stroke-dasharray="40,40"/>
    <rect x="380" y="140" width="15" height="140" fill="white" />
    
    <rect x="410" y="10" width="12" height="150" fill="#2c3e50" />
    <rect x="396" y="10" width="40" height="100" fill="#111" rx="8" stroke="#444" stroke-width="2"/>
    <circle cx="416" cy="30" r="10" fill="{l_red}" stroke="#222" stroke-width="1"/>
    <circle cx="416" cy="60" r="10" fill="{l_yellow}" stroke="#222" stroke-width="1"/>
    <circle cx="416" cy="90" r="10" fill="{l_green}" stroke="#222" stroke-width="1"/>
    
    {traffic_content}
    
    </svg>
    """
    return svg.replace("\n", " ").strip()

def check_ethics(inputs):
    v = []
    if inputs['sH']: v.append("🚫 Rule 1: Severe Harm")
    if inputs['mH'] and not inputs['pC']: v.append("⚠️ Rule 2: Unjustified Harm")
    if inputs['vP'] and not inputs['hC']: v.append("🔒 Rule 3: Privacy Breach")
    if inputs['dH'] and not (inputs['pMH'] and inputs['hEA']): v.append("🤥 Rule 4: Deception")
    if not inputs['hE']: v.append("❓ Rule 5: No Explanation")
    if inputs['bEV'] and not inputs['pC']: v.append("🚑 Rule 6: Emergency Blocked")
    return len(v) == 0, v

with st.sidebar:
    st.image("https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png", width=80)
    st.title("Control Panel")
    st.markdown("---")
    
    scenario = st.selectbox("Select Scenario", ["Scenario A: Standard", "Scenario B: VIP Convoy", "Scenario C: Icy Road"])
    
    d = {"sH":0,"mH":0,"pC":0,"vP":0,"hC":1,"dH":0,"hEA":1,"hE":1,"pMH":1,"bEV":0}
    
    if scenario == "Scenario B: VIP Convoy": 
        d.update({"sH":1, "mH":1, "bEV":1, "hC":0, "vP":0, "hE":1}) 
        
    elif scenario == "Scenario C: Icy Road": 
        d.update({"pC":1, "mH":1, "bEV":1})
    
    st.markdown("#### 📡 Live Sensors")
    bEV = st.toggle("🚑 Emergency Detected", value=bool(d['bEV']))
    pC = st.checkbox("🔥 Catastrophe Risk", value=bool(d['pC']))
    
    with st.expander("🛠️ Advanced Settings"):
        sH = st.checkbox("Severe Harm", value=bool(d['sH']))
        mH = st.checkbox("Minor Harm", value=bool(d['mH']))
        vP = st.checkbox("Privacy Violation", value=bool(d['vP']))
        hC = st.checkbox("Has Consent", value=bool(d['hC']))
        hE = st.checkbox("Has Explanation", value=bool(d['hE']))
        dH = st.checkbox("Deceives Human", value=bool(d['dH']))
        hEA = st.checkbox("Ethics Approval", value=bool(d['hEA']))
        pMH = st.checkbox("Prevents Minor Harm", value=bool(d['pMH']))

    inputs = {"sH": sH, "mH": mH, "pC": pC, "vP": vP, "hC": hC, "dH": dH, "hEA": hEA, "hE": hE, "pMH": pMH, "bEV": bEV}

c1, c2 = st.columns([1, 6])
with c1:
    st.image(LOGO_URL, width=120)
with c2:
    st.markdown(f"## American University of Ras Al Khaimah")
    st.markdown(f"**AI Ethics Advisor System | Student: Saif Mussa**")

st.markdown("---")

m1, m2, m3 = st.columns(3)
m1.metric("Current Mode", scenario.split(":")[0])
m2.metric("Emergency Status", "ACTIVE" if bEV else "INACTIVE")
m3.metric("System Health", "ONLINE")

st.markdown("### 🖥️ Live Traffic Simulation")
st.markdown(render_game_view(scenario), unsafe_allow_html=True) 

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("#### 📝 Scenario Details")
    if scenario == "Scenario A: Standard":
        st.info("Normal operation. Green lights optimized for flow.")
    elif scenario == "Scenario B: VIP Convoy":
        st.warning("VIP Protocol initiated. Intersection blocked for government convoy. Ambulance on Hold.")
    else:
        st.info("❄️ **ICE DETECTED:** Friction coefficient low. Intersection locked to prevent sliding collision.")

with col2:
    st.markdown("#### ⚖️ AI Decision")
    if st.button("RUN ETHICS CHECK"):
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            ok, errs = check_ethics(inputs)
        
        if ok:
            st.success("✅ PERMISSIBLE")
            st.balloons()
        else:
            st.error("⛔ IMPERMISSIBLE")
            for e in errs:
                st.write(f"• {e}")

st.markdown("---")
st.caption("© 2025 AURAK Student Project")


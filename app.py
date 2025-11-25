import streamlit as st
import time

# ==========================================
# 1. إعداد الصفحة
# ==========================================
st.set_page_config(
    page_title="AURAK Traffic Control",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الألوان
AURAK_NAVY = "#002D56"
BUTTON_ORANGE = "#FF8C00" 
BUTTON_HOVER = "#E67E00"
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# ==========================================
# 2. تصميم CSS (نصوص سوداء + أزرار برتقالية)
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; color: #000000; }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{ color: #333333; }}
    [data-testid="stSidebar"] {{ background-color: {AURAK_NAVY}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* تصميم الزر البرتقالي */
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

# ==========================================
# 3. محرك الرسم (Smart 2D Render) - تم الإصلاح
# ==========================================
def render_game_view(scenario):
    bg_color = "#87CEEB" 
    road_fill = "#343a40" 
    line_stroke = "#ffffff"
    
    traffic_content = ""
    light_top = "#440000"
    light_bot = "#004400"
    
    if scenario == "Scenario C: Icy Road":
        road_fill = "#dbeff9" # ثلج
        line_stroke = "#2196f3"
        bg_color = "#b3e5fc"
        light_top = "#FF0000"
        traffic_content = """
            <text x="500" y="190" font-size="40">❄️</text>
            <text x="200" y="220" font-size="40">❄️</text>
            <text x="550" y="150" font-size="80">🚛</text>
            <text x="250" y="170" font-size="60">🚑</text>
            <rect x="20" y="20" width="280" height="40" fill="white" rx="5" opacity="0.9"/>
            <text x="35" y="48" font-family="Arial" font-weight="bold" fill="orange" font-size="18">⚠️ ICE HAZARD DETECTED</text>
        """
        
    elif scenario == "Scenario B: VIP Convoy":
        light_top = "#FF0000"
        traffic_content = """
            <text x="450" y="170" font-size="70">🚓</text>
            <text x="530" y="170" font-size="70">🚓</text>
            <text x="280" y="170" font-size="60">🚗</text>
            <text x="150" y="170" font-size="60">🚑</text>
            <rect x="20" y="20" width="280" height="40" fill="white" rx="5" opacity="0.9"/>
            <text x="35" y="48" font-family="Arial" font-weight="bold" fill="red" font-size="18">🔴 BLOCKED FOR VIP</text>
        """
        
    else: # Standard
        light_bot = "#00FF00"
        traffic_content = """
            <text x="50" y="170" font-size="60">🚗</text>
            <text x="350" y="170" font-size="60">🚙</text>
            <text x="650" y="170" font-size="60">🚕</text>
            <rect x="20" y="20" width="280" height="40" fill="white" rx="5" opacity="0.9"/>
            <text x="35" y="48" font-family="Arial" font-weight="bold" fill="green" font-size="18">🟢 FLOWING NORMALLY</text>
        """

    # هذا هو الإصلاح: إزالة الأسطر الجديدة لتصبح الكود كتلة واحدة
    svg = f"""
    <svg width="100%" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" style="background-color: {bg_color}; border-radius: 10px; border: 5px solid {AURAK_NAVY};">
    <rect x="0" y="0" width="800" height="300" fill="{bg_color}" />
    <rect x="0" y="100" width="800" height="150" fill="#7f8c8d" />
    <rect x="0" y="120" width="800" height="130" fill="{road_fill}" />
    <line x1="0" y1="185" x2="800" y2="185" stroke="{line_stroke}" stroke-width="4" stroke-dasharray="30,30"/>
    <rect x="380" y="120" width="15" height="130" fill="white" />
    <rect x="410" y="20" width="15" height="100" fill="#2c3e50" />
    <rect x="400" y="20" width="35" height="80" fill="black" rx="5" stroke="grey" stroke-width="2"/>
    <circle cx="417" cy="40" r="12" fill="{light_top}" stroke="#333"/>
    <circle cx="417" cy="80" r="12" fill="{light_bot}" stroke="#333"/>
    {traffic_content}
    </svg>
    """
    # السطر السحري الذي يحل المشكلة:
    return svg.replace("\n", " ").strip()

# ==========================================
# 4. المنطق (Logic)
# ==========================================
def check_ethics(inputs):
    v = []
    if inputs['sH']: v.append("🚫 Rule 1: Severe Harm")
    if inputs['mH'] and not inputs['pC']: v.append("⚠️ Rule 2: Unjustified Harm")
    if inputs['vP'] and not inputs['hC']: v.append("🔒 Rule 3: Privacy Breach")
    if inputs['dH'] and not (inputs['pMH'] and inputs['hEA']): v.append("🤥 Rule 4: Deception")
    if not inputs['hE']: v.append("❓ Rule 5: No Explanation")
    if inputs['bEV'] and not inputs['pC']: v.append("🚑 Rule 6: Emergency Blocked")
    return len(v) == 0, v

# ==========================================
# 5. الواجهة (UI)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9626/9626620.png", width=80)
    st.title("Control Panel")
    st.markdown("---")
    scenario = st.selectbox("📂 Select Scenario", ["Scenario A: Standard", "Scenario B: VIP Convoy", "Scenario C: Icy Road"])
    
    d = {"sH":0,"mH":0,"pC":0,"vP":0,"hC":1,"dH":0,"hEA":1,"hE":1,"pMH":1,"bEV":0}
    if scenario == "Scenario B: VIP Convoy": d.update({"sH":1, "mH":1, "bEV":1, "hC":0})
    elif scenario == "Scenario C: Icy Road": d.update({"pC":1, "mH":1, "bEV":1})
    
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

# Header
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
st.markdown(render_game_view(scenario), unsafe_allow_html=True) # سيتم العرض بشكل صحيح الآن

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("#### 📝 Scenario Details")
    if scenario == "Scenario A: Standard":
        st.info("Normal operation. Green lights optimized for flow.")
    elif scenario == "Scenario B: VIP Convoy":
        st.warning("VIP Protocol. Intersection blocked. Ambulance held back.")
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

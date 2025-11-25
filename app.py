import streamlit as st
import time

# ==========================================
# 1. إعداد الصفحة
# ==========================================
st.set_page_config(
    page_title="AURAK AI Control",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ألوان الجامعة
AURAK_NAVY = "#002D56"
AURAK_GOLD = "#BFA15F"
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# ==========================================
# 2. تحسين التصميم (CSS)
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f6f9; }}
    [data-testid="stSidebar"] {{ background-color: {AURAK_NAVY}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    h1, h2, h3 {{ color: {AURAK_NAVY}; }}
    div.stButton > button {{ 
        background-color: {AURAK_NAVY}; color: white; border: 2px solid {AURAK_GOLD}; 
        border-radius: 8px; height: 50px; font-weight: bold; font-size: 18px; 
    }}
    div.stButton > button:hover {{ background-color: {AURAK_GOLD}; color: {AURAK_NAVY}; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. محرك الرسم (SVG Engine) - تم إصلاح المشكلة هنا
# ==========================================
def render_game_view(scenario):
    # الألوان
    bg_color = "#87CEEB"
    road_color = "#343a40"
    
    # المحتوى المتغير
    if scenario == "Scenario A: Standard":
        light_top = "#440000"
        light_bot = "#00FF00" # أخضر
        # السيارات (بدون مسافات بادئة لتجنب المشكلة)
        traffic_content = """<text x="50" y="170" font-size="60">🚗</text><text x="350" y="170" font-size="60">🚙</text><text x="650" y="170" font-size="60">🚕</text><text x="30" y="40" font-family="Arial" font-weight="bold" fill="green" font-size="20">🟢 SIGNAL: GREEN (FLOWING)</text>"""
        
    elif scenario == "Scenario B: VIP Convoy":
        light_top = "#FF0000" # أحمر
        light_bot = "#004400"
        traffic_content = """<text x="450" y="170" font-size="70">🚓</text><text x="520" y="170" font-size="70">🚓</text><text x="280" y="170" font-size="60">🚗</text><text x="150" y="170" font-size="60">🚑</text><text x="30" y="40" font-family="Arial" font-weight="bold" fill="red" font-size="20">🔴 SIGNAL: RED (VIP BLOCK)</text>"""
        
    else: # Scenario C
        light_top = "#FF0000"
        light_bot = "#004400"
        traffic_content = """<text x="550" y="150" font-size="80">🚛</text><text x="500" y="190" font-size="40">❄️</text><text x="250" y="170" font-size="60">🚑</text><text x="30" y="40" font-family="Arial" font-weight="bold" fill="orange" font-size="20">⚠️ HAZARD: ICE DETECTED</text>"""

    # تجميع الكود في سطر واحد لتجنب أخطاء المسافات
    svg_code = f"""
    <svg width="100%" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" style="background-color: {bg_color}; border-radius: 15px; border: 4px solid {AURAK_NAVY};">
    <rect x="0" y="0" width="800" height="300" fill="{bg_color}" />
    <rect x="0" y="100" width="800" height="20" fill="#7f8c8d" />
    <rect x="0" y="120" width="800" height="130" fill="{road_color}" />
    <line x1="0" y1="185" x2="800" y2="185" stroke="#ffffff" stroke-width="4" stroke-dasharray="30,30"/>
    <rect x="380" y="120" width="15" height="130" fill="white" />
    <rect x="0" y="250" width="800" height="20" fill="#7f8c8d" />
    <rect x="410" y="20" width="15" height="100" fill="#2c3e50" />
    <rect x="400" y="20" width="35" height="80" fill="black" rx="5" stroke="#555" stroke-width="2"/>
    <circle cx="417" cy="40" r="12" fill="{light_top}" stroke="#333"/>
    <circle cx="417" cy="80" r="12" fill="{light_bot}" stroke="#333"/>
    {traffic_content}
    </svg>
    """
    return svg_code

# ==========================================
# 4. المنطق (AI Logic)
# ==========================================
def check_ethics(inputs):
    v = []
    if inputs['sH']: v.append("🚫 Rule 1: Non-Maleficence (Severe Harm)")
    if inputs['mH'] and not inputs['pC']: v.append("⚠️ Rule 2: Harm Mitigation (Unjustified Minor Harm)")
    if inputs['vP'] and not inputs['hC']: v.append("🔒 Rule 3: Data Stewardship (Privacy Breach)")
    if inputs['dH'] and not (inputs['pMH'] and inputs['hEA']): v.append("🤥 Rule 4: Honesty (Deception)")
    if not inputs['hE']: v.append("❓ Rule 5: Accountability (No Explanation)")
    if inputs['bEV'] and not inputs['pC']: v.append("🚑 Rule 6: Emergency Priority (Ambulance Blocked)")
    return len(v) == 0, v

# ==========================================
# 5. الواجهة (Sidebar & Main)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9626/9626620.png", width=80)
    st.title("Control Center")
    st.markdown("---")
    scenario = st.selectbox("📂 Select Scenario", ["Scenario A: Standard", "Scenario B: VIP Convoy", "Scenario C: Icy Road"])
    
    # Defaults
    d = {"sH":0,"mH":0,"pC":0,"vP":0,"hC":1,"dH":0,"hEA":1,"hE":1,"pMH":1,"bEV":0}
    if scenario == "Scenario B: VIP Convoy": d.update({"sH":1, "mH":1, "bEV":1, "hC":0})
    elif scenario == "Scenario C: Icy Road": d.update({"pC":1, "mH":1, "bEV":1})
    
    st.markdown("#### 📡 Live Sensors")
    bEV = st.toggle("🚑 Emergency Detected", value=bool(d['bEV']))
    pC = st.checkbox("🔥 Catastrophe Risk", value=bool(d['pC']))
    
    with st.expander("🛠️ Advanced Parameters"):
        sH = st.checkbox("Severe Harm", value=bool(d['sH']))
        mH = st.checkbox("Minor Harm", value=bool(d['mH']))
        vP = st.checkbox("Privacy Violation", value=bool(d['vP']))
        hC = st.checkbox("Has Consent", value=bool(d['hC']))
        hEA = st.checkbox("Ethics Approval", value=bool(d['hEA']))
        hE = st.checkbox("Has Explanation", value=bool(d['hE']))
        dH = st.checkbox("Deceives Human", value=bool(d['dH']))
        pMH = st.checkbox("Prevents Minor Harm", value=bool(d['pMH']))

    action_data = {"sH": sH, "mH": mH, "pC": pC, "vP": vP, "hC": hC, "dH": dH, "hEA": hEA, "hE": hE, "pMH": pMH, "bEV": bEV}

# Header
c1, c2 = st.columns([1, 6])
with c1:
    st.image(LOGO_URL, width=130)
with c2:
    st.markdown(f"<h1 style='color:{AURAK_NAVY}; margin-bottom:0;'>American University of Ras Al Khaimah</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{AURAK_GOLD}; margin-top:0;'>Department of Computer Science & Engineering</h3>", unsafe_allow_html=True)
    st.caption("**AI Ethics Advisor System (Mini-Project) | Developed by: Saif Mussa**")

st.markdown("---")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Current Mode", scenario.split(":")[0], delta="Active", delta_color="normal")
m2.metric("Emergency Status", "DETECTED" if bEV else "CLEAR", delta="High Priority" if bEV else "Normal", delta_color="inverse")
m3.metric("System Load", "Optimized", "98%")

st.markdown("### 🖥️ Real-time Traffic Simulation")

# *** هنا يتم عرض الرسمة ***
st.markdown(render_game_view(scenario), unsafe_allow_html=True)

# النتائج
st.markdown("<br>", unsafe_allow_html=True)
col_res1, col_res2 = st.columns([2, 1])

with col_res1:
    st.subheader("📋 Scenario Description")
    if scenario == "Scenario A: Standard":
        st.info("The intersection is operating under normal conditions. The AI is optimizing green light duration based on traffic density.")
    elif scenario == "Scenario B: VIP Convoy":
        st.warning("A VIP convoy has requested immediate priority. The AI protocol forces a red light for cross-traffic. An ambulance is present.")
    else:
        st.error("Sensors detect black ice and a skidding heavy truck. The AI has locked the intersection (Red All) to prevent a T-bone collision.")

with col_res2:
    st.subheader("⚖️ AI Verdict")
    if st.button("RUN ETHICS CHECK"):
        with st.spinner("Analyzing rules..."):
            time.sleep(0.7)
            permissible, violations = check_ethics(action_data)
        
        if permissible:
            st.success("## ✅ PERMISSIBLE")
            st.write("Action approved by EGF.")
            st.balloons()
        else:
            st.error("## ⛔ IMPERMISSIBLE")
            st.write("Action blocked.")
            for v in violations:
                st.write(f"- {v}")

st.markdown("---")
st.caption("© 2025 AURAK Student Project | Saif Mussa")

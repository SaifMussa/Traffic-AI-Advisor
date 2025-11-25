import streamlit as st
import time

# ==========================================
# 1. إعدادات الصفحة والتصميم
# ==========================================
st.set_page_config(
    page_title="AURAK Traffic AI",
    page_icon="🚦",
    layout="wide"
)

# ألوان الجامعة
AURAK_NAVY = "#002D56"
AURAK_GOLD = "#BFA15F"
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# كود CSS لتجميل الموقع
st.markdown(f"""
    <style>
    .stApp {{ background-color: white; }}
    [data-testid="stSidebar"] {{ background-color: {AURAK_NAVY}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    .stButton>button {{ background-color: {AURAK_NAVY}; color: white; border-radius: 5px; width: 100%; }}
    .stButton>button:hover {{ background-color: {AURAK_GOLD}; color: black; }}
    .metric-box {{ padding: 10px; border-radius: 5px; background-color: #f0f2f6; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. محرك الرسم (Simulation Engine)
# ==========================================
def render_street(scenario):
    # تحديد ألوان الإشارة بناءً على السيناريو
    if scenario == "Scenario A: Standard":
        light_color_top = "#330000"   # أحمر مطفأ
        light_color_bot = "#00FF00"   # أخضر ساطع
        # سيارات تتحرك
        cars = """
        <text x="50" y="160" font-size="40">🚗</text>
        <text x="300" y="160" font-size="40">🚙</text>
        <text x="600" y="160" font-size="40">🚕</text>
        """
        status_text = "🟢 TRAFFIC FLOWING"
        status_color = "green"
        
    elif scenario == "Scenario B: VIP Convoy":
        light_color_top = "#FF0000"   # أحمر ساطع
        light_color_bot = "#003300"   # أخضر مطفأ
        # سيارات شرطة وإسعاف عالق
        cars = """
        <text x="500" y="160" font-size="50">🚓</text>
        <text x="280" y="160" font-size="40">🚗</text>
        <text x="180" y="160" font-size="40">🚑</text>
        """
        status_text = "🔴 BLOCKED FOR VIP"
        status_color = "red"
        
    else: # Scenario C: Icy Road
        light_color_top = "#FF0000"
        light_color_bot = "#003300"
        # شاحنة تنزلق
        cars = """
        <text x="550" y="140" font-size="50">🚛💨</text>
        <text x="450" y="180" font-size="30">❄️</text>
        <text x="250" y="160" font-size="40">🚑</text>
        """
        status_text = "⚠️ CRASH AVOIDANCE"
        status_color = "orange"

    # كود الرسم SVG
    svg = f"""
    <svg width="100%" height="250" viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg" style="border: 4px solid {AURAK_NAVY}; border-radius: 10px; background-color: #87CEEB;">
        <rect x="0" y="0" width="800" height="250" fill="#87CEEB" />
        <rect x="0" y="120" width="800" height="130" fill="#444" />
        <line x1="0" y1="185" x2="800" y2="185" stroke="white" stroke-width="2" stroke-dasharray="20,20"/>
        <rect x="350" y="120" width="10" height="130" fill="white" />
        
        <rect x="390" y="20" width="15" height="150" fill="#222" />
        <rect x="375" y="20" width="45" height="100" fill="black" rx="5" />
        <circle cx="397" cy="45" r="15" fill="{light_color_top}" stroke="grey" stroke-width="2"/>
        <circle cx="397" cy="95" r="15" fill="{light_color_bot}" stroke="grey" stroke-width="2"/>
        
        {cars}
        
        <rect x="10" y="10" width="220" height="40" fill="white" rx="5" opacity="0.8"/>
        <text x="20" y="35" font-family="Arial" font-weight="bold" fill="{status_color}">{status_text}</text>
    </svg>
    """
    return svg

# ==========================================
# 3. المنطق (Logic)
# ==========================================
def check_ethics(action):
    violations = []
    # القوانين
    if action['sH']: violations.append("Rule 1: Severe Harm")
    if action['mH'] and not action['pC']: violations.append("Rule 2: Unjustified Harm")
    if action['vP'] and not action['hC']: violations.append("Rule 3: Privacy Breach")
    if action['dH'] and not (action['pMH'] and action['hEA']): violations.append("Rule 4: Deception")
    if not action['hE']: violations.append("Rule 5: No Explanation")
    if action['bEV'] and not action['pC']: violations.append("Rule 6: Emergency Blocked")
    
    return len(violations) == 0, violations

# ==========================================
# 4. الواجهة والتحكم (Sidebar)
# ==========================================
with st.sidebar:
    st.header("⚙️ Control Panel")
    scenario = st.selectbox("Select Scenario:", ["Scenario A: Standard", "Scenario B: VIP Convoy", "Scenario C: Icy Road"])
    
    st.divider()
    
    # قيم افتراضية للمتغيرات
    defaults = {"sH":0,"mH":0,"pC":0,"vP":0,"hC":1,"dH":0,"hEA":1,"hE":1,"pMH":1,"bEV":0}
    
    if scenario == "Scenario B: VIP Convoy":
        defaults.update({"sH":1, "mH":1, "bEV":1, "hC":0})
    elif scenario == "Scenario C: Icy Road":
        defaults.update({"pC":1, "mH":1, "bEV":1})

    st.subheader("Sensor Readings")
    bEV = st.toggle("🚑 Emergency Vehicle", value=bool(defaults["bEV"]))
    
    with st.expander("Advanced Inputs"):
        pC = st.checkbox("Prevents Catastrophe", value=bool(defaults["pC"]))
        sH = st.checkbox("Severe Harm", value=bool(defaults["sH"]))
        mH = st.checkbox("Minor Harm", value=bool(defaults["mH"]))
        vP = st.checkbox("Violates Privacy", value=bool(defaults["vP"]))
        hC = st.checkbox("Has Consent", value=bool(defaults["hC"]))
        dH = st.checkbox("Deceives Human", value=bool(defaults["dH"]))
        hEA = st.checkbox("Ethics Approval", value=bool(defaults["hEA"]))
        hE = st.checkbox("Has Explanation", value=bool(defaults["hE"]))
        pMH = st.checkbox("Prevents Minor Harm", value=bool(defaults["pMH"]))

    action_data = {
        "sH": sH, "mH": mH, "pC": pC, "vP": vP, "hC": hC, "dH": dH,
        "hEA": hEA, "hE": hE, "pMH": pMH, "bEV": bEV
    }

# ==========================================
# 5. المنطقة الرئيسية (Main Layout)
# ==========================================
# الترويسة
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(LOGO_URL, width=110)
with col_title:
    st.markdown(f"<h2 style='color:{AURAK_NAVY}; margin:0;'>American University of Ras Al Khaimah</h2>", unsafe_allow_html=True)
    st.markdown("**AI Ethics Advisor System | Project by: Saif Mussa**")

st.markdown("---")

# عرض المحاكاة (الشارع)
st.markdown("### 🚦 Live Traffic Simulation")
st.markdown(render_street(scenario), unsafe_allow_html=True)

# عرض النتائج والتحليل
c1, c2 = st.columns(2)

with c1:
    st.info(f"**Current Scenario:** {scenario}")
    if scenario == "Scenario A: Standard":
        st.write("Traffic is flowing normally. AI is optimizing green lights.")
    elif scenario == "Scenario B: VIP Convoy":
        st.write("VIP protocol active. Creating a green wave for VIP, blocking others.")
    else:
        st.write("Dangerous road conditions detected (Ice). Intersection locked.")

with c2:
    if st.button("⚖️ Analyze Ethical Compliance"):
        with st.spinner("Processing..."):
            time.sleep(0.5)
            is_valid, errors = check_ethics(action_data)
        
        if is_valid:
            st.success("✅ **ACTION PERMISSIBLE**")
            st.balloons()
        else:
            st.error("⛔ **ACTION IMPERMISSIBLE**")
            for e in errors:
                st.write(f"- {e}")

st.markdown("---")
st.caption("© 2025 AURAK Student Project")

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

# الألوان (تم التعديل للأحمر العنابي)
AURAK_RED = "#990000"   # الأحمر الجامعي
AURAK_GOLD = "#BFA15F"  # الذهبي
BUTTON_ORANGE = "#FF8C00" 
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# ==========================================
# 2. تصميم CSS (إصلاح القائمة + اللون الأحمر)
# ==========================================
st.markdown(f"""
    <style>
    /* الألوان العامة */
    .stApp {{ background-color: #ffffff; color: #000000; }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{ color: #333333; }}
    
    /* القائمة الجانبية (أصبحت حمراء) */
    [data-testid="stSidebar"] {{ background-color: {AURAK_RED}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* === إصلاح القائمة المنسدلة (Dropdown Fix) === */
    /* جعل الصندوق الخارجي أبيض */
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: white !important;
        color: black !important;
        border: 2px solid {AURAK_GOLD};
    }}
    /* جعل النص المختار أسود */
    .stSelectbox div[data-baseweb="select"] span {{
        color: black !important;
    }}
    /* السهم */
    .stSelectbox svg {{
        fill: {AURAK_RED} !important;
    }}
    
    /* === القائمة المنبثقة (الخيارات الداخلية) === */
    /* الخلفية بيضاء */
    ul[data-baseweb="menu"] {{
        background-color: white !important;
    }}
    /* النصوص سوداء وواضحة */
    li[data-baseweb="option"] {{
        color: black !important;
    }}
    /* عند تمرير الماوس */
    li[data-baseweb="option"]:hover {{
        background-color: #ffe6e6 !important;
        font-weight: bold;
    }}

    /* الأزرار */
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
        background-color: #cc7000;
        color: white !important;
        border: 2px solid #333;
    }}
    
    /* النصوص في العدادات */
    [data-testid="stMetricLabel"] {{ color: #555 !important; }}
    [data-testid="stMetricValue"] {{ color: #000 !important; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. محرك الرسم (Smart 2D Render)
# ==========================================
def render_game_view(scenario):
    # إعدادات الخلفية
    bg_color = "#87CEEB" 
    road_fill = "#343a40" 
    line_stroke = "#ffffff"
    grass_color = "#4CAF50"
    
    traffic_content = ""
    # ألوان الإشارة
    l_red = "#330000"
    l_green = "#003300"
    
    if scenario == "Scenario C: Icy Road":
        road_fill = "#dbeff9" 
        line_stroke = "#2196f3"
        bg_color = "#b3e5fc"
        grass_color = "#e3f2fd"
        l_red = "#FF0000" # أحمر مضاء
        
        traffic_content = """
            <text x="500" y="200" font-size="80">🚛</text>
            <text x="250" y="220" font-size="50">❄️</text>
            <text x="200" y="210" font-size="70">🚑</text>
            <text x="580" y="200" font-size="40">💨</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="orange" stroke-width="2"/>
            <text x="290" y="58" font-family="Arial" font-weight="bold" fill="orange" font-size="20">⚠️ ICE HAZARD DETECTED</text>
        """
        
    elif scenario == "Scenario B: VIP Convoy":
        l_red = "#FF0000" # أحمر مضاء
        traffic_content = """
            <text x="400" y="200" font-size="90">🚓</text>
            <text x="550" y="200" font-size="90">🚓</text>
            <text x="250" y="200" font-size="80">🚗</text>
            <text x="100" y="200" font-size="80">🚑</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="red" stroke-width="2"/>
            <text x="310" y="58" font-family="Arial" font-weight="bold" fill="red" font-size="20">🔴 BLOCKED FOR VIP</text>
        """
        
    else: # Standard
        l_green = "#00FF00" # أخضر مضاء
        traffic_content = """
            <text x="50" y="200" font-size="80">🚗</text>
            <text x="350" y="200" font-size="80">🚙</text>
            <text x="650" y="200" font-size="80">🚕</text>
            <rect x="250" y="30" width="300" height="40" fill="white" rx="5" stroke="green" stroke-width="2"/>
            <text x="300" y="58" font-family="Arial" font-weight="bold" fill="green" font-size="20">🟢 FLOWING NORMALLY</text>
        """

    # تم تغيير لون الحدود (Border) إلى الأحمر ليطابق الهوية
    svg = f"""
    <svg width="100%" height="320" viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background-color: {bg_color}; border-radius: 10px; border: 5px solid {AURAK_RED};">
    <rect x="0" y="0" width="100%" height="320" fill="{bg_color}" />
    <rect x="0" y="150" width="100%" height="170" fill="{grass_color}" />
    <rect x="0" y="140" width="100%" height="140" fill="{road_fill}" stroke="#555" stroke-width="2"/>
    <line x1="0" y1="210" x2="800" y2="210" stroke="{line_stroke}" stroke-width="5" stroke-dasharray="40,40"/>
    <rect x="380" y="140" width="15" height="140" fill="white" />
    
    <rect x="410" y="10" width="12" height="150" fill="#2c3e50" />
    <rect x="396" y="10" width="40" height="100" fill="#111" rx="8" stroke="#444" stroke-width="2"/>
    <circle cx="416" cy="30" r="10" fill="{l_red}" stroke="#222" stroke-width="1"/>
    <circle cx="416" cy="60" r="10" fill="#333300" stroke="#222" stroke-width="1"/>
    <circle cx="416" cy="90" r="10" fill="{l_green}" stroke="#222" stroke-width="1"/>
    
    {traffic_content}
    </svg>
    """
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
    
    # القائمة المنسدلة (ستظهر الآن بيضاء ونصوصها سوداء)
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

# Header
c1, c2 = st.columns([1, 6])
with c1:
    st.image(LOGO_URL, width=120)
with c2:
    # تم تغيير لون العنوان للأحمر
    st.markdown(f"<h1 style='color:{AURAK_RED}; margin-bottom:0;'>American University of Ras Al Khaimah</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#333; margin-top:0;'>AI Ethics Advisor System | Student: Saif Mussa</h3>", unsafe_allow_html=True)

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

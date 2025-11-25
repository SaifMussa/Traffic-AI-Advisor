import streamlit as st
import time

# ==========================================
# 1. CONFIGURATION & AURAK THEME SETUP
# ==========================================
st.set_page_config(
    page_title="AURAK AI Ethics System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ألوان الجامعة الرسمية (Approximate AURAK Colors)
AURAK_NAVY = "#002D56"
AURAK_GOLD = "#BFA15F"
AURAK_GREY = "#F0F2F6"

# رابط الشعار الجديد
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# حقن CSS لتغيير تصميم الموقع بالكامل ليشبه موقع الجامعة
st.markdown(f"""
    <style>
    /* تغيير لون القائمة الجانبية للأزرق الكحلي */
    [data-testid="stSidebar"] {{
        background-color: {AURAK_NAVY};
    }}
    /* تغيير لون نصوص القائمة الجانبية للأبيض */
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    /* تعديل العناوين الرئيسية */
    h1, h2, h3 {{
        color: {AURAK_NAVY};
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    /* خلفية التطبيق */
    .stApp {{
        background-color: white;
    }}
    /* تصميم الأزرار */
    div.stButton > button {{
        background-color: {AURAK_NAVY};
        color: white;
        border-radius: 5px;
        border: none;
    }}
    div.stButton > button:hover {{
        background-color: {AURAK_GOLD};
        color: black;
    }}
    /* مربع النتائج */
    .success-box {{
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }}
    .error-box {{
        padding: 15px;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC FUNCTIONS (Back-end)
# ==========================================
def check_ethics(action):
    violations = []
    if action['causes_severe_harm']: violations.append("Rule 1: Severe Harm Detected")
    if action['causes_minor_harm'] and not action['prevents_catastrophe']: violations.append("Rule 2: Unjustified Minor Harm")
    if action['violates_privacy'] and not action['has_consent']: violations.append("Rule 3: Privacy Breach")
    if action['deceives_human'] and not (action['prevents_minor_harm'] and action['has_ethics_approval']): violations.append("Rule 4: Deception Detected")
    if not action['has_explanation']: violations.append("Rule 5: No Accountability")
    if action['blocks_emergency_vehicle'] and not action['prevents_catastrophe']: violations.append("Rule 6: Emergency Vehicle Blocked")
    return len(violations) == 0, violations

# ==========================================
# 3. VISUALIZATION ENGINE (Fixed Street View)
# ==========================================
def render_traffic_scene(scenario):
    """
    يرسم الشارع والإشارة والسيارات بناءً على السيناريو المختار باستخدام SVG
    """
    # الألوان والعناصر الافتراضية
    light_color = "green" if scenario == "Scenario A: Standard Flow" else "red"
    
    # تحديد المركبات الظاهرة ومواقعها
    vehicles_svg = ""
    
    if scenario == "Scenario A: Standard Flow":
        # سيارات تتحرك (موزعة في الشارع)
        vehicles_svg = """
            <text x="50" y="160" font-size="40">🚗</text>
            <text x="300" y="160" font-size="40">🚙</text>
            <text x="600" y="160" font-size="40">🚕</text>
            <text x="10" y="40" font-family="sans-serif" fill="green" font-weight="bold">🟢 TRAFFIC FLOWING</text>
        """
    
    elif scenario == "Scenario B: The VIP Convoy":
        # سيارات متوقفة + سيارة شرطة + إسعاف عالق
        vehicles_svg = """
            <text x="500" y="160" font-size="45">🚓</text> <text x="280" y="160" font-size="40">🚗</text> <text x="180" y="160" font-size="40">🚑</text> <text x="10" y="40" font-family="sans-serif" fill="red" font-weight="bold">🔴 BLOCKED FOR VIP</text>
        """

    elif scenario == "Scenario C: Icy Road Collision":
        # شاحنة تنزلق + إسعاف محجوز
        vehicles_svg = """
            <text x="550" y="140" font-size="50">🚛💨</text> <text x="450" y="180" font-size="30">❄️❄️</text> <text x="250" y="160" font-size="40">🚑</text> <text x="10" y="40" font-family="sans-serif" fill="orange" font-weight="bold">⚠️ CRASH AVOIDANCE MODE</text>
        """
        
    else: # Manual
        vehicles_svg = '<text x="150" y="160" font-size="40">🚗</text>'

    # رسم إشارة المرور
    light_svg = ""
    if light_color == "red":
        light_svg = """
        <circle cx="400" cy="50" r="15" fill="#ff0000" stroke="black" stroke-width="2"/>
        <circle cx="400" cy="90" r="15" fill="#330000" stroke="black" stroke-width="2"/>
        """
    else:
        light_svg = """
        <circle cx="400" cy="50" r="15" fill="#330000" stroke="black" stroke-width="2"/>
        <circle cx="400" cy="90" r="15" fill="#00ff00" stroke="black" stroke-width="2"/>
        """

    # الكود النهائي للرسمة
    svg_code = f"""
    <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" style="background-color:#eef; border: 2px solid {AURAK_NAVY}; border-radius: 10px;">
        <rect x="0" y="0" width="800" height="220" fill="#87CEEB" />
        
        <rect x="0" y="120" width="800" height="100" fill="#444" />
        <line x1="0" y1="170" x2="800" y2="170" stroke="white" stroke-width="2" stroke-dasharray="20,20"/>
        
        <rect x="350" y="120" width="10" height="100" fill="white" />
        
        <rect x="390" y="20" width="20" height="150" fill="#333" />
        <rect x="375" y="20" width="50" height="100" fill="black" rx="5" />
        
        {light_svg}
        
        {vehicles_svg}
    </svg>
    """
    return svg_code

# ==========================================
# 4. SIDEBAR & CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ System Control Panel")
    
    # اختيار السيناريو
    scenario_mode = st.selectbox(
        "Load Traffic Scenario:",
        ["Scenario A: Standard Flow", "Scenario B: The VIP Convoy", "Scenario C: Icy Road Collision", "Manual Input"]
    )
    
    st.divider()
    
    # إعدادات الحساسات (Defaults)
    vals = {
        "sH": False, "mH": False, "pC": False, "vP": False, "hC": True, 
        "dH": False, "hEA": True, "hE": True, "pMH": True, "bEV": False
    }

    # تحديث القيم حسب السيناريو تلقائياً
    if scenario_mode == "Scenario B: The VIP Convoy":
        vals.update({"sH": True, "mH": True, "bEV": True, "hC": False})
    elif scenario_mode == "Scenario C: Icy Road Collision":
        vals.update({"pC": True, "mH": True, "bEV": True})

    # عرض أدوات التحكم
    st.markdown("#### 📡 Live Sensor Data")
    bEV = st.toggle("🚑 Emergency Vehicle Present", value=vals["bEV"])
    
    with st.expander("Show Advanced Logic Inputs"):
        pC = st.checkbox("Prevents Catastrophe", value=vals["pC"])
        sH = st.checkbox("Causes Severe Harm", value=vals["sH"])
        mH = st.checkbox("Causes Minor Harm", value=vals["mH"])
        vP = st.checkbox("Violates Privacy", value=vals["vP"])
        hC = st.checkbox("Has Consent", value=vals["hC"])
        hEA = st.checkbox("Has Ethics Approval", value=vals["hEA"])
        hE = st.checkbox("Has Explanation", value=vals["hE"])
        dH = st.checkbox("Deceives Human", value=vals["dH"])
        pMH = st.checkbox("Prevents Minor Harm", value=vals["pMH"])

    # تجميع المدخلات
    current_action = {
        "causes_severe_harm": sH, "causes_minor_harm": mH, "prevents_catastrophe": pC,
        "violates_privacy": vP, "has_consent": hC, "deceives_human": dH,
        "has_ethics_approval": hEA, "has_explanation": hE, "prevents_minor_harm": pMH,
        "blocks_emergency_vehicle": bEV
    }

# ==========================================
# 5. MAIN CONTENT AREA
# ==========================================

# --- Header ---
c1, c2 = st.columns([1, 5])
with c1:
    # عرض الشعار من الرابط الجديد
    st.image(LOGO_URL, width=120)
with c2:
    st.markdown(f"<h1 style='color:{AURAK_NAVY}; margin-bottom:0;'>American University of Ras Al Khaimah</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{AURAK_GOLD}; margin-top:0;'>Department of Computer Science & Engineering</h3>", unsafe_allow_html=True)
    st.markdown("**Project: AI Ethics Advisor (Traffic Control System)**")
    # تم إضافة اسمك هنا
    st.markdown("👨‍🎓 **Developed by: Saif Mussa**")

st.markdown("---")
st.markdown(f"<h2 style='text-align: center; color: {AURAK_NAVY}'>Intelligent Traffic Control System</h2>", unsafe_allow_html=True)

# --- 2D Simulation Display ---
st.markdown("### 🚦 Live Intersection View (2D Simulation)")
svg_html = render_traffic_scene(scenario_mode)
st.markdown(svg_html, unsafe_allow_html=True)

# --- Analysis Section ---
col_desc, col_result = st.columns([1, 1])

with col_desc:
    st.markdown("#### 📝 Scenario Narrative")
    if scenario_mode == "Scenario A: Standard Flow":
        st.info("Normal traffic conditions. Optimizing green light duration. No emergency vehicles.")
    elif scenario_mode == "Scenario B: The VIP Convoy":
        st.warning("⚠️ VIP Convoy detected. Protocol requires blocking traffic. Ambulance also detected on cross street.")
    elif scenario_mode == "Scenario C: Icy Road Collision":
        st.error("🚨 CRITICAL: Black ice & skidding truck detected. Intersection locked to prevent collision.")
    else:
        st.markdown("Manual testing mode active.")

with col_result:
    st.markdown("#### ⚖️ Ethical Verdict")
    
    # زر التحليل
    if st.button("Analyze Decision Logics", type="primary"):
        with st.spinner("Processing Logical Framework..."):
            time.sleep(0.8) 
            
        is_permissible, violations = check_ethics(current_action)
        
        if is_permissible:
            st.markdown(f"""
                <div class="success-box">
                    <h3>✅ ACTION PERMISSIBLE</h3>
                    <p>The system has approved this action. No ethical violations found.</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            violations_html = "".join([f"<li>{v}</li>" for v in violations])
            st.markdown(f"""
                <div class="error-box">
                    <h3>⛔ ACTION IMPERMISSIBLE</h3>
                    <p

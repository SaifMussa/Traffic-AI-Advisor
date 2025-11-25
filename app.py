import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AURAK AI Traffic Ethics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. HEADER & BRANDING SECTION
# ==========================================
# يمكنك استبدال الرابط التالي برابط مباشر لشعار جامعتك إذا توفر
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            # محاولة عرض الشعار
            st.image(LOGO_URL, width=150)
        except:
            # بديل نصي في حال لم يعمل الرابط
            st.header("🏛️ AURAK")
            
    with col2:
        st.title("American University of Ras Al Khaimah")
        st.subheader("Department of Computer Science & Engineering")
        st.markdown("**Project: AI Ethics Advisor System (Traffic Control Domain)**")
        # ===> اكتب اسمك هنا <===
        st.markdown("👨‍🎓 **Developed by: Saif Mussa**")
        st.divider()

# ==========================================
# 2. CORE LOGIC (The Brain)
# ==========================================
def check_ethics(action):
    violations = []
    if action['causes_severe_harm']: violations.append("🚫 Rule 1: Severe Harm Detected")
    if action['causes_minor_harm'] and not action['prevents_catastrophe']: violations.append("⚠️ Rule 2: Unjustified Minor Harm")
    if action['violates_privacy'] and not action['has_consent']: violations.append("🔒 Rule 3: Privacy Breach")
    if action['deceives_human'] and not (action['prevents_minor_harm'] and action['has_ethics_approval']): violations.append("🤥 Rule 4: Deception Detected")
    if not action['has_explanation']: violations.append("❓ Rule 5: No Accountability")
    if action['blocks_emergency_vehicle'] and not action['prevents_catastrophe']: violations.append("🚑 Rule 6: Emergency Vehicle Blocked")
    
    return len(violations) == 0, violations

# ==========================================
# 3. 2D SIMULATION ENGINE (SVG Visualization)
# ==========================================
def generate_street_view_svg(scenario_type, signal_state, block_emergency):
    """
    Generates a dynamic SVG image of a street intersection based on the scenario state.
    """
    # Colors
    road_color = "#333333"
    line_color = "#FFFFFF"
    light_box_color = "#000000"
    red_light = "#FF0000" if signal_state == "RED" else "#550000"
    green_light = "#00FF00" if signal_state == "GREEN" else "#005500"
    
    # Vehicle Positions (Emojis for simplicity in SVG text)
    traffic_layer = ""
    
    if scenario_type == "Scenario A: Standard Flow":
        # Cars moving freely
        traffic_layer = """
            <text x="100" y="160" font-size="40">🚗</text>
            <text x="300" y="160" font-size="40">🚙</text>
            <text x="550" y="160" font-size="40">🚕</text>
        """
        light_color_top = "#550000"
        light_color_bottom = "#00FF00" # Green

    elif scenario_type == "Scenario B: The VIP Convoy":
        # Cars stopped, Ambulance stuck behind
        traffic_layer = """
            <text x="380" y="160" font-size="40">🚓(VIP)</text>
            <text x="280" y="160" font-size="40">🚗</text>
            <text x="180" y="160" font-size="40">🚑(Stuck)</text>
        """
        light_color_top = "#FF0000" # Red
        light_color_bottom = "#005500"

    elif scenario_type == "Scenario C: Icy Road Collision":
        # Critical situation, ambulance blocked to save lives
        traffic_layer = """
            <text x="450" y="120" font-size="50">❄️🚛(Skidding)</text>
            <text x="300" y="160" font-size="40">🚗(Stopped)</text>
            <text x="200" y="160" font-size="40">🚑(Held)</text>
        """
        light_color_top = "#FF0000" # Red (to stop crash)
        light_color_bottom = "#005500"
    else:
        # Default manual mode
        light_color_top = "#FF0000" if signal_state == "RED" else "#550000"
        light_color_bottom = "#00FF00" if signal_state == "GREEN" else "#005500"
        traffic_layer = '<text x="50" y="160" font-size="40">🚗</text>' if not signal_state == "RED" else '<text x="300" y="160" font-size="40">🚗(Stopped)</text>'


    # SVG Template
    svg_code = f"""
    <svg width="100%" height="250" xmlns="http://www.w3.org/2000/svg" style="background-color:#87CEEB; border-radius: 10px; border: 3px solid #333;">
        <rect x="0" y="100" width="100%" height="150" fill="{road_color}" />
        <line x1="0" y1="175" x2="800" y2="175" stroke="{line_color}" stroke-width="2" stroke-dasharray="10,10"/>
        
        <rect x="400" y="50" width="20" height="150" fill="#555" />
        <rect x="385" y="20" width="50" height="100" fill="{light_box_color}" rx="5" />
        <circle cx="410" cy="45" r="15" fill="{light_color_top}" stroke="#333" stroke-width="2"/>
        <circle cx="410" cy="95" r="15" fill="{light_color_bottom}" stroke="#333" stroke-width="2"/>
        
        {traffic_layer}
        
        <text x="10" y="30" font-family="Arial" font-size="14" fill="black" font-weight="bold">2D Real-time Simulation View</text>
    </svg>
    """
    return svg_code

# ==========================================
# 4. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.header("🎛️ Control Panel")
    st.info("Select a scenario to simulate real-world conditions and see how the AI responds.")
    
    st.subheader("Scenario Selection")
    scenario = st.selectbox(
        "Choose Simulation Mode:",
        ["Scenario A: Standard Flow", "Scenario B: The VIP Convoy", "Scenario C: Icy Road Collision", "Manual Testing Mode"]
    )
    
    st.markdown("---")
    st.subheader("📡 Sensor Inputs (Override)")
    
    # Defaults based on scenario choice
    defaults = {"sH": False, "mH": False, "pC": False, "vP": False, "hC": True, "dH": False, "hEA": True, "hE": True, "pMH": True, "bEV": False}

    if scenario == "Scenario A: Standard Flow":
        defaults.update({"bEV": False})
        signal_state_viz = "GREEN"
    elif scenario == "Scenario B: The VIP Convoy":
        defaults.update({"bEV": True, "sH": True, "mH": True, "hC": False})
        signal_state_viz = "RED"
    elif scenario == "Scenario C: Icy Road Collision":
        defaults.update({"bEV": True, "pC": True, "mH": True})
        signal_state_viz = "RED"
    else:
        signal_state_viz = st.radio("Manual Signal State:", ["GREEN", "RED"], horizontal=True)

    # Input Toggles
    with st.expander("Detailed Sensor Inputs", expanded=(scenario == "Manual Testing Mode")):
        bEV = st.toggle("🚑 Block Emergency Vehicle", value=defaults["bEV"])
        pC = st.checkbox("Prevents Catastrophe", value=defaults["pC"])
        st.caption("--- Core Ethics Variables ---")
        sH = st.checkbox("Severe Harm", value=defaults["sH"])
        mH = st.checkbox("Minor Harm", value=defaults["mH"])
        vP = st.checkbox("Violates Privacy", value=defaults["vP"])
        hC = st.checkbox("Has Consent", value=defaults["hC"])
        dH = st.checkbox("Deceives Human", value=defaults["dH"])
        hEA = st.checkbox("Ethics Approval", value=defaults["hEA"])
        hE = st.checkbox("Has Explanation", value=defaults["hE"])
        pMH = st.checkbox("Prevents Minor Harm", value=defaults["pMH"])

    # Build Action Dictionary
    current_action = {
        "causes_severe_harm": sH, "causes_minor_harm": mH, "prevents_catastrophe": pC,
        "violates_privacy": vP, "has_consent": hC, "deceives_human": dH,
        "has_ethics_approval": hEA, "has_explanation": hE, "prevents_minor_harm": pMH,
        "blocks_emergency_vehicle": bEV
    }

# ==========================================
# 5. MAIN DASHBOARD LAYOUT
# ==========================================

# --- Top Section: 2D Simulation & Context ---
st.subheader("🖥️ Live Traffic Simulation & Context")

col_viz, col_context = st.columns([3, 2])

with col_viz:
    # Render the dynamic 2D Street View
    svg_html = generate_street_view_svg(scenario, signal_state_viz, bEV)
    st.markdown(svg_html, unsafe_allow_html=True)

with col_context:
    st.markdown("#### Current Situation Analysis")
    if scenario == "Scenario A: Standard Flow":
        st.success("🟢 **Status: Normal.** Traffic flowing smoothly. AI is optimizing green light timings for efficiency.")
    elif scenario == "Scenario B: The VIP Convoy":
        st.error("🔴 **Status: CRITICAL (Ethical Violation).** AI has forced a red light to prioritize a VIP, blocking an active ambulance without justification.")
    elif scenario == "Scenario C: Icy Road Collision":
        st.warning("🟠 **Status: EMERGENCY INTERVENTION.** AI is holding a red light (blocking ambulance) to prevent an imminent collision with a skidding fuel tanker.")
    else:
        st.info("🔵 **Status: Manual Testing.** Waiting for user inputs from the control panel.")

    # Metrics summary
    m1, m2 = st.columns(2)
    m1.metric("Emergency Present?", "YES" if bEV else "NO", delta_color="inverse")
    m2.metric("Catastrophe Risk?", "HIGH" if pC else "LOW", delta_color="inverse")

st.divider()

# --- Bottom Section: AI Ethics Verdict ---
st.subheader("🤖 AI Ethics Advisor Verdict")

with st.spinner('Analyzing against Ethical Governance Framework...'):
    time.sleep(0.3) # UI effect
    is_permissible, reasons = check_ethics(current_action)

result_container = st.container()
if is_permissible:
    result_container.success("## ✅ JUDGMENT: PERMISSIBLE ACTION")
    result_container.markdown("The proposed AI action **aligns** with all defined ethical principles and safety protocols.")
else:
    result_container.error("## ⛔ JUDGMENT: IMPERMISSIBLE ACTION")
    result_container.markdown("The proposed AI action **violates** core ethical principles. The action has been blocked.")
    with st.expander("View Violation Details", expanded=True):
        for r in reasons:
            st.error(r)

# Footer
st.caption("---")
st.caption("© 2023 AURAK Dept of Computer Science. This system is a prototype for educational purposes.")

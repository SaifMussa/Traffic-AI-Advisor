import streamlit as st
import time

# --- Page Configuration (Must be first) ---
st.set_page_config(
    page_title="AI Traffic Control Hub",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Logic Section (The Brain) ---
def check_ethics(action):
    violations = []
    if action['causes_severe_harm']: violations.append("🚫 Rule 1: Severe Harm Detected")
    if action['causes_minor_harm'] and not action['prevents_catastrophe']: violations.append("⚠️ Rule 2: Unjustified Minor Harm")
    if action['violates_privacy'] and not action['has_consent']: violations.append("🔒 Rule 3: Privacy Breach")
    if action['deceives_human'] and not (action['prevents_minor_harm'] and action['has_ethics_approval']): violations.append("🤥 Rule 4: Deception Detected")
    if not action['has_explanation']: violations.append("❓ Rule 5: No Accountability/Explanation")
    if action['blocks_emergency_vehicle'] and not action['prevents_catastrophe']: violations.append("🚑 Rule 6: Emergency Vehicle Blocked")
    
    return len(violations) == 0, violations

# --- Sidebar: Control Panel ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1086/1086089.png", width=100)
    st.title("Control Panel")
    st.markdown("---")
    
    st.subheader("Load Simulation")
    scenario = st.selectbox(
        "Choose a Scenario:",
        ["Custom (Manual)", "Scenario A: Standard Flow", "Scenario B: The VIP Convoy", "Scenario C: Icy Road Collision"]
    )
    
    st.markdown("---")
    st.subheader("Sensor Inputs")
    
    # Defaults
    defaults = {
        "sH": False, "mH": False, "pC": False,
        "vP": False, "hC": True, "dH": False,
        "hEA": True, "hE": True, "pMH": True, "bEV": False
    }

    # Auto-fill based on selection
    if scenario == "Scenario A: Standard Flow":
        defaults.update({"bEV": False, "pC": False, "sH": False, "mH": False})
    elif scenario == "Scenario B: The VIP Convoy":
        defaults.update({"bEV": True, "pC": False, "sH": True, "mH": True, "hC": False})
    elif scenario == "Scenario C: Icy Road Collision":
        defaults.update({"bEV": True, "pC": True, "sH": False, "mH": True})

    # Toggles
    c1, c2 = st.columns(2)
    sH = c1.checkbox("Severe Harm", value=defaults["sH"])
    mH = c2.checkbox("Minor Harm", value=defaults["mH"])
    pC = st.checkbox("Prevents Catastrophe", value=defaults["pC"])
    st.markdown("---")
    bEV = st.toggle("🚑 Block Emergency Vehicle", value=defaults["bEV"])
    st.markdown("---")
    vP = st.checkbox("Violates Privacy", value=defaults["vP"])
    hC = st.checkbox("Has Consent", value=defaults["hC"])
    dH = st.checkbox("Deceives Human", value=defaults["dH"])
    hEA = st.checkbox("Ethics Approval", value=defaults["hEA"])
    hE = st.checkbox("Has Explanation", value=defaults["hE"])
    pMH = st.checkbox("Prevents Minor Harm", value=defaults["pMH"])

    # Build Dictionary
    current_action = {
        "causes_severe_harm": sH, "causes_minor_harm": mH, "prevents_catastrophe": pC,
        "violates_privacy": vP, "has_consent": hC, "deceives_human": dH,
        "has_ethics_approval": hEA, "has_explanation": hE, "prevents_minor_harm": pMH,
        "blocks_emergency_vehicle": bEV
    }

# --- Main Dashboard ---
st.title("🚦 AI Traffic Ethics Advisor")
st.markdown("### Intelligent Decision Support System")

# Status Indicators
col1, col2, col3 = st.columns(3)
col1.metric("System Status", "ONLINE", delta_color="normal")
col2.metric("Emergency Mode", "ACTIVE" if bEV else "INACTIVE", delta_color="inverse" if bEV else "off")
col3.metric("Catastrophe Risk", "HIGH" if pC else "LOW", delta_color="inverse" if pC else "normal")

st.divider()

# Visualization
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Live Simulation Context")
    if scenario == "Scenario A: Standard Flow":
        st.info("Normal traffic conditions. Optimizing green light duration.")
        # Placeholder for visual
        st.write("🚗 🚕 🚙 ... 🟢 ... 🚗 🚕")
    elif scenario == "Scenario B: The VIP Convoy":
        st.error("DETECTED: VIP Convoy requesting priority. Ambulance detected on cross-street.")
        st.write("🚓 🚓 🚓 ... 🔴 ... 🚑")
    elif scenario == "Scenario C: Icy Road Collision":
        st.warning("CRITICAL: Black ice detected! Fuel tanker losing control. Ambulance approaching.")
        st.write("❄️ 🚛💥 ... 🔴 ... 🚑")
    else:
        st.write("Waiting for manual inputs...")

with c2:
    st.subheader("AI Analysis")
    with st.spinner('Computing Ethical Permissibility...'):
        time.sleep(0.5) # Fake loading effect for realism
        is_permissible, reasons = check_ethics(current_action)

    if is_permissible:
        st.success("## ✅ PERMISSIBLE")
        st.write("Action aligns with Ethical Governance Framework.")
        st.balloons()
    else:
        st.error("## ⛔ IMPERMISSIBLE")
        st.write("Action blocked by Safety Protocol.")
        for r in reasons:
            st.warning(r)

# Footer / Code View
with st.expander("View Logic Source Code (Python)"):
    st.code("""
    # Core Logic Snapshot
    def check_ethics(action):
        if action['blocks_emergency_vehicle'] and not action['prevents_catastrophe']:
            return False # Rule 6 Violation
        return True
    """, language='python')
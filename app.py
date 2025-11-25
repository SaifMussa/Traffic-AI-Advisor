import streamlit as st
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="AURAK AI Ethics", layout="wide")

# 2. الألوان والشعار
AURAK_NAVY = "#002D56"
AURAK_GOLD = "#BFA15F"
LOGO_URL = "https://aetex.ae/wp-content/uploads/2018/01/Pages-from-aurak-logo-only.png"

# 3. المنطق (Logic)
def check_ethics(action):
    violations = []
    if action['causes_severe_harm']: violations.append("Rule 1: Severe Harm")
    if action['causes_minor_harm'] and not action['prevents_catastrophe']: violations.append("Rule 2: Unjustified Harm")
    if action['violates_privacy'] and not action['has_consent']: violations.append("Rule 3: Privacy Breach")
    if action['deceives_human'] and not (action['prevents_minor_harm'] and action['has_ethics_approval']): violations.append("Rule 4: Deception")
    if not action['has_explanation']: violations.append("Rule 5: No Accountability")
    if action['blocks_emergency_vehicle'] and not action['prevents_catastrophe']: violations.append("Rule 6: Emergency Blocked")
    return len(violations) == 0, violations

# 4. الواجهة الجانبية (Sidebar)
st.sidebar.title("⚙️ Control Panel")
scenario = st.sidebar.selectbox("Select Scenario:", ["Scenario A: Standard", "Scenario B: VIP Convoy", "Scenario C: Icy Road"])

# قيم افتراضية
vals = {"sH": False, "mH": False, "pC": False, "vP": False, "hC": True, "dH": False, "hEA": True, "hE": True, "pMH": True, "bEV": False}

if scenario == "Scenario B: VIP Convoy":
    vals.update({"sH": True, "mH": True, "bEV": True, "hC": False})
elif scenario == "Scenario C: Icy Road":
    vals.update({"pC": True, "mH": True, "bEV": True})

st.sidebar.divider()
st.sidebar.write("### Sensor Inputs")
bEV = st.sidebar.toggle("🚑 Emergency Vehicle?", value=vals["bEV"])
pC = st.sidebar.checkbox("Prevents Catastrophe", value=vals["pC"])
sH = st.sidebar.checkbox("Severe Harm", value=vals["sH"])
mH = st.sidebar.checkbox("Minor Harm", value=vals["mH"])

current_action = {
    "causes_severe_harm": sH, "causes_minor_harm": mH, "prevents_catastrophe": pC,
    "violates_privacy": vals["vP"], "has_consent": vals["hC"], "deceives_human": vals["dH"],
    "has_ethics_approval": vals["hEA"], "has_explanation": vals["hE"], 
    "prevents_minor_harm": vals["pMH"], "blocks_emergency_vehicle": bEV
}

# 5. الصفحة الرئيسية (Main Page)
col1, col2 = st.columns([1, 5])
with col1:
    st.image(LOGO_URL, width=100)
with col2:
    st.title("American University of Ras Al Khaimah")
    st.markdown("**AI Ethics Advisor: Traffic Control System | Dev by: Saif Mussa**")

st.divider()

# عرض المحاكاة المبسطة (بدون تعقيد SVG لتجنب الأخطاء)
st.subheader("🚦 Live Simulation View")
if scenario == "Scenario A: Standard":
    st.success("🟢 TRAFFIC FLOWING: Green Light Active. No Obstructions.")
elif scenario == "Scenario B: VIP Convoy":
    st.error("🔴 BLOCKED: Red Light Forced for VIP. Ambulance Stuck!")
else:
    st.warning("⚠️ CRASH AVOIDANCE: Intersection Locked due to Ice.")

# عرض النتائج
st.subheader("⚖️ Ethical Decision")
if st.button("Analyze Decision"):
    with st.spinner("Checking rules..."):
        time.sleep(0.5)
        is_ok, errs = check_ethics(current_action)
        
    if is_ok:
        st.success("✅ ACTION PERMISSIBLE")
        st.balloons()
    else:
        st.error("⛔ ACTION IMPERMISSIBLE")
        for e in errs:
            st.write(f"- {e}")

st.divider()
st.caption("© 2025 AURAK Student Project | Saif Mussa")

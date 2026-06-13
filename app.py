from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.drug_api import get_drug_info, check_patient_cautions
from utils.ai_summary import generate_simple_summary
from utils.ocr_utils import extract_text_from_image
from utils.report import build_report


st.set_page_config(
    page_title="AI Medicine Safety Assistant",
    page_icon="💊",
    layout="wide",
)

CUSTOM_CSS = """
<style>
.main-header {
    padding: 1.2rem 1rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #f8fbff 0%, #eef7ff 100%);
    border: 1px solid #dbeafe;
    margin-bottom: 1rem;
}
.metric-card {
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background: #ffffff;
}
.safe-box {
    padding: 1rem;
    border-radius: 12px;
    border-left: 5px solid #f59e0b;
    background: #fffbeb;
}
.small-muted { color: #6b7280; font-size: 0.92rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="main-header">
<h1>💊 AI Medicine Safety & Drug Information Assistant</h1>
<p>Search tablets, capsules, injections, syrups, tonics, and other medicines to understand official usage information, warnings, side effects, and safety cautions in simple language.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.error(
    "Medical safety disclaimer: This app is for educational and portfolio purposes only. "
    "It is not a diagnosis, prescription, dosage recommendation, or replacement for a doctor/pharmacist. "
    "Do not start, stop, or change medicines without professional advice."
)

with st.sidebar:
    st.header("⚙️ App Settings")
    use_groq = st.toggle(
        "Use Groq AI summary if API key is configured",
        value=False,
        help="Add GROQ_API_KEY in Streamlit secrets or .env/environment. The app works without it using rule-based summary.",
    )
    st.markdown("---")
    st.subheader("👤 Safety Profile")
    age_group = st.selectbox("Age group", ["Adult", "Child", "Older adult"])
    kidney_disease = st.checkbox("Kidney disease")
    liver_disease = st.checkbox("Liver disease")
    diabetes = st.checkbox("Diabetes")
    pregnant = st.checkbox("Pregnant")
    breastfeeding = st.checkbox("Breastfeeding")
    allergy = st.text_input("Known allergy", placeholder="Example: penicillin")

    profile = {
        "age_group": age_group,
        "kidney_disease": kidney_disease,
        "liver_disease": liver_disease,
        "diabetes": diabetes,
        "pregnant": pregnant,
        "breastfeeding": breastfeeding,
        "allergy": allergy,
    }


search_tab, image_tab, reminder_tab, about_tab = st.tabs(
    ["🔍 Medicine Search", "📷 Image Scanner", "⏰ Reminder Dashboard", "📘 About Project"]
)


def show_drug_result(medicine_name: str):
    if not medicine_name.strip():
        st.warning("Please enter a medicine name.")
        return

    with st.spinner("Searching public drug label data..."):
        drug_info = get_drug_info(medicine_name)

    if not drug_info:
        st.error("No information found. Try generic name or correct spelling.")
        return

    caution_alerts = check_patient_cautions(drug_info, profile)
    summary = generate_simple_summary(medicine_name, drug_info, caution_alerts, use_groq=use_groq)

    st.success("Medicine information loaded. Please read disclaimer and consult a healthcare professional before using any medicine.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Display Name", drug_info.get("display_name", "N/A")[:25])
    c2.metric("Generic", drug_info.get("generic_name", "N/A")[:25])
    c3.metric("Route", drug_info.get("route", "N/A")[:25])
    c4.metric("RxCUI", drug_info.get("rxnorm_rxcui", "N/A")[:25])

    with st.expander("📌 Basic Details", expanded=True):
        details = {
            "Searched name": drug_info.get("searched_name"),
            "Brand name": drug_info.get("brand_name"),
            "Generic name": drug_info.get("generic_name"),
            "Manufacturer": drug_info.get("manufacturer"),
            "Product type": drug_info.get("product_type"),
            "Route": drug_info.get("route"),
            "Data source": drug_info.get("data_source_note"),
        }
        st.table(pd.DataFrame(details.items(), columns=["Field", "Value"]))

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Used For / Indications")
        st.write(drug_info.get("indications", "Information not available"))

        st.subheader("🧾 Dosage/Admin Label Text")
        st.info(
            "This section may contain official label text. Do not use it to self-dose. Follow only your doctor/pharmacist instructions."
        )
        st.write(drug_info.get("dosage", "Information not available"))

        st.subheader("🚫 Contraindications")
        st.write(drug_info.get("contraindications", "Information not available"))

    with right:
        st.subheader("⚠️ Warnings")
        st.write(drug_info.get("warnings", "Information not available"))

        if drug_info.get("boxed_warning") != "Information not available":
            st.subheader("🛑 Boxed Warning")
            st.error(drug_info.get("boxed_warning"))

        st.subheader("❗ Side Effects")
        st.write(drug_info.get("side_effects", "Information not available"))

    st.subheader("🧬 Drug Interactions")
    st.write(drug_info.get("drug_interactions", "Information not available"))

    st.subheader("🤰 Pregnancy / Breastfeeding Information")
    st.write(drug_info.get("pregnancy_or_breastfeeding", "Information not available"))

    st.subheader("🛡️ Personal Safety Caution Alerts")
    for alert in caution_alerts:
        st.warning(alert)

    st.subheader("🤖 Simple AI Explanation")
    st.markdown(summary)

    report_text = build_report(medicine_name, drug_info, caution_alerts, summary)
    st.download_button(
        label="⬇️ Download Medicine Report (.txt)",
        data=report_text,
        file_name=f"medicine_report_{medicine_name.replace(' ', '_')}.txt",
        mime="text/plain",
    )


with search_tab:
    st.header("🔍 Search Medicine")
    medicine_name = st.text_input(
        "Enter tablet / injection / syrup / tonic / capsule name",
        placeholder="Example: paracetamol, amoxicillin, insulin, cetirizine",
    )
    col_a, col_b = st.columns([1, 3])
    with col_a:
        search_clicked = st.button("Search Medicine", type="primary")
    with col_b:
        st.markdown(
            "<p class='small-muted'>Tip: If brand name does not work, try the generic name.</p>",
            unsafe_allow_html=True,
        )

    if search_clicked:
        show_drug_result(medicine_name)

with image_tab:
    st.header("📷 Medicine Strip / Bottle Image Scanner")
    st.write("Upload a clear photo of a medicine strip, bottle, or label. OCR will try to read the medicine name.")
    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    extracted_name = ""
    if uploaded:
        st.image(uploaded, caption="Uploaded medicine image", use_container_width=True)
        if st.button("Extract Text from Image"):
            with st.spinner("Reading text from image..."):
                extracted_text = extract_text_from_image(uploaded)
            st.text_area("Extracted text", extracted_text, height=150)
            extracted_name = extracted_text.split("\n")[0].strip() if extracted_text else ""
            if extracted_name:
                st.info(f"Suggested search text: {extracted_name}")

    manual_from_image = st.text_input(
        "Enter or correct medicine name from image",
        value=extracted_name,
        placeholder="Type medicine name after checking OCR text",
        key="image_manual_name",
    )
    if st.button("Search This Medicine", key="search_image_name"):
        show_drug_result(manual_from_image)

with reminder_tab:
    st.header("⏰ Simple Medicine Reminder Dashboard")
    st.write("Create a local reminder table for demonstration. This does not send real notifications.")

    if "reminders" not in st.session_state:
        st.session_state.reminders = []

    with st.form("reminder_form"):
        r1, r2, r3 = st.columns(3)
        med = r1.text_input("Medicine name")
        time_slot = r2.selectbox("Time", ["Morning", "Afternoon", "Evening", "Night", "Custom"])
        food = r3.selectbox("Food instruction", ["As prescribed", "Before food", "After food", "With food"])
        notes = st.text_input("Notes", placeholder="Example: doctor prescribed for 5 days")
        submitted = st.form_submit_button("Add Reminder")
        if submitted:
            if med.strip():
                st.session_state.reminders.append(
                    {"Medicine": med, "Time": time_slot, "Food": food, "Notes": notes or "-"}
                )
                st.success("Reminder added to dashboard.")
            else:
                st.warning("Enter medicine name first.")

    if st.session_state.reminders:
        df = pd.DataFrame(st.session_state.reminders)
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "⬇️ Download Reminder CSV",
            data=df.to_csv(index=False),
            file_name="medicine_reminders.csv",
            mime="text/csv",
        )
        if st.button("Clear Reminders"):
            st.session_state.reminders = []
            st.rerun()
    else:
        st.info("No reminders added yet.")

with about_tab:
    st.header("📘 About This Portfolio Project")
    st.markdown(
        """
### Project Goal
Many people search medicine names online but struggle to understand official label information. This app gives a simple, educational interface for drug information lookup while clearly avoiding diagnosis or prescription.

### Main Features
- Search tablets, capsules, syrups, injections, tonics, and other medicines
- Fetch public drug label information using openFDA
- Normalize medicine names using RxNorm/RxNav
- Show usage, warnings, side effects, contraindications, interactions, and pregnancy/breastfeeding information
- Optional image OCR for medicine strip/bottle labels
- Personal caution alerts for kidney disease, liver disease, diabetes, pregnancy, breastfeeding, allergy, child, and older adult use
- Simple AI/rule-based summary
- Downloadable medicine report
- Reminder dashboard

### Tech Stack
Python, Streamlit, Requests, Pandas, Pillow, pytesseract, openFDA Drug Label API, RxNorm/RxNav API, optional Groq AI.

### What This App Does NOT Do
- Does not diagnose disease
- Does not prescribe medicine
- Does not recommend dosage
- Does not confirm whether a drug is safe for a user
- Does not replace a doctor or pharmacist
        """
    )

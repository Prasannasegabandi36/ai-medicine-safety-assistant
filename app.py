import streamlit as st
import pandas as pd
from datetime import date

from utils.drug_api import get_drug_info
from utils.ai_summary import generate_simple_summary
from utils.ocr_utils import extract_text_from_image
from utils.report import create_text_report


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MediGuide AI",
    page_icon="💊",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f6feb;
        margin-bottom: 0px;
    }

    .sub-title {
        font-size: 20px;
        color: #444;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #ffcc00;
        color: #664d03;
    }

    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #2e7d32;
        color: #1b5e20;
    }

    .info-card {
        background-color: #f8f9fa;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 12px;
    }

    .small-note {
        color: #666;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar Branding
# -----------------------------
st.sidebar.title("💊 MediGuide AI")
st.sidebar.caption("Smart Medicine Safety Assistant")

st.sidebar.markdown("---")

st.sidebar.header("⚙️ Search Preferences")

search_mode = st.sidebar.radio(
    "Choose search method",
    [
        "Search by Medicine Name",
        "Upload Medicine Image"
    ]
)

show_ai_summary = st.sidebar.checkbox(
    "Show AI Simple Explanation",
    value=True
)

st.sidebar.markdown("---")

st.sidebar.header("🩺 Health Safety Profile")

age_group = st.sidebar.selectbox(
    "Age group",
    [
        "Adult",
        "Child",
        "Senior Citizen"
    ]
)

kidney_issue = st.sidebar.checkbox("Kidney disease / kidney problem")
liver_issue = st.sidebar.checkbox("Liver disease / liver problem")
diabetes = st.sidebar.checkbox("Diabetes")
pregnancy = st.sidebar.checkbox("Pregnant / planning pregnancy")
allergy = st.sidebar.checkbox("Known medicine allergy")

st.sidebar.markdown("---")

st.sidebar.info(
    "This app gives educational medicine information only. "
    "Always consult a doctor or pharmacist before using any medicine."
)


# -----------------------------
# Header
# -----------------------------
st.markdown('<p class="main-title">💊 MediGuide AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Smart Medicine Safety & Drug Information Assistant</p>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="warning-box">
    <b>Medical Disclaimer:</b> This app is for educational and portfolio purposes only.
    It does not provide medical diagnosis, prescription, or dosage recommendation.
    Always consult a qualified doctor or pharmacist before taking any medicine.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# -----------------------------
# Helper Function
# -----------------------------
def show_health_cautions():
    cautions = []

    if age_group == "Child":
        cautions.append(
            "👶 Child caution: Medicine usage and dosage for children must be decided by a pediatric doctor."
        )

    if age_group == "Senior Citizen":
        cautions.append(
            "👵 Senior citizen caution: Older adults may need special dosage adjustment and monitoring."
        )

    if kidney_issue:
        cautions.append(
            "⚠️ Kidney caution: Some medicines can affect kidney function or need dose adjustment. Consult a doctor."
        )

    if liver_issue:
        cautions.append(
            "⚠️ Liver caution: Some medicines may affect the liver. Consult a doctor before using."
        )

    if diabetes:
        cautions.append(
            "🩸 Diabetes caution: Some medicines can affect blood sugar levels. Consult your doctor."
        )

    if pregnancy:
        cautions.append(
            "🤰 Pregnancy caution: Do not use medicines during pregnancy without doctor advice."
        )

    if allergy:
        cautions.append(
            "🚨 Allergy caution: Avoid medicines that caused allergy before and consult a doctor immediately."
        )

    if cautions:
        st.markdown("### 🛡️ Personalized Safety Cautions")
        for caution in cautions:
            st.warning(caution)


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔍 Medicine Search",
        "📷 Image Scanner",
        "⏰ Medicine Reminder",
        "ℹ️ About Project"
    ]
)


# -----------------------------
# Tab 1: Medicine Search
# -----------------------------
with tab1:
    st.markdown("## 🔍 Search Medicine Information")

    medicine_name = st.text_input(
        "Enter medicine name",
        placeholder="Example: Paracetamol, Amoxicillin, Ibuprofen, Metformin"
    )

    search_button = st.button("Search Medicine", type="primary")

    if search_button:
        if medicine_name.strip() == "":
            st.error("Please enter a medicine name.")
        else:
            with st.spinner("Searching medicine information..."):
                drug_data = get_drug_info(medicine_name)

            if not drug_data:
                st.error(
                    "No official information found. Please check spelling or try using the generic medicine name."
                )
                st.info(
                    "Example: Instead of searching brand name like Dolo 650, try Paracetamol or Acetaminophen."
                )
            else:
                st.success("Medicine information found.")

                show_health_cautions()

                st.markdown("## 📋 Medicine Details")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### ✅ Used For")
                    st.write(drug_data.get("indications", "Information not available."))

                    st.markdown("### 🧾 How to Use")
                    st.write(
                        drug_data.get(
                            "dosage",
                            "Use only as prescribed by a doctor."
                        )
                    )

                with col2:
                    st.markdown("### ⚠️ Warnings")
                    st.write(drug_data.get("warnings", "Information not available."))

                    st.markdown("### ❌ Side Effects")
                    st.write(drug_data.get("side_effects", "Information not available."))

                st.markdown("### 🚫 Contraindications")
                st.write(drug_data.get("contraindications", "Information not available."))

                if show_ai_summary:
                    st.markdown("## 🤖 Simple AI Explanation")
                    ai_summary = generate_simple_summary(medicine_name, drug_data)
                    st.info(ai_summary)

                st.markdown("## 👨‍⚕️ Doctor Advice")
                st.write(
                    "Do not start, stop, or change medicine dosage without consulting a doctor. "
                    "Seek urgent medical help if you experience breathing difficulty, swelling, severe rash, "
                    "chest pain, fainting, or serious allergic reaction."
                )

                report_text = create_text_report(
                    medicine_name=medicine_name,
                    drug_data=drug_data,
                    age_group=age_group,
                    kidney_issue=kidney_issue,
                    liver_issue=liver_issue,
                    diabetes=diabetes,
                    pregnancy=pregnancy,
                    allergy=allergy
                )

                st.download_button(
                    label="📥 Download Medicine Report",
                    data=report_text,
                    file_name=f"{medicine_name}_medicine_report.txt",
                    mime="text/plain"
                )


# -----------------------------
# Tab 2: Image Scanner
# -----------------------------
with tab2:
    st.markdown("## 📷 Medicine Image Scanner")
    st.write(
        "Upload a photo of a medicine strip, bottle, injection label, or tonic label. "
        "The app will try to extract text from the image."
    )

    uploaded_image = st.file_uploader(
        "Upload medicine image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Medicine Image", use_container_width=True)

        if st.button("Extract Medicine Name from Image"):
            with st.spinner("Reading text from image..."):
                extracted_text = extract_text_from_image(uploaded_image)

            if extracted_text:
                st.markdown("### Extracted Text")
                st.code(extracted_text)

                st.info(
                    "Copy the correct medicine name from the extracted text and search it in the Medicine Search tab."
                )
            else:
                st.error(
                    "Could not extract text clearly. Try uploading a clearer image with good lighting."
                )


# -----------------------------
# Tab 3: Medicine Reminder
# -----------------------------
with tab3:
    st.markdown("## ⏰ Medicine Reminder Dashboard")
    st.write(
        "Create a simple medicine schedule. This is only a planner, not a prescription."
    )

    if "reminders" not in st.session_state:
        st.session_state.reminders = []

    with st.form("reminder_form"):
        med_name = st.text_input("Medicine name")
        timing = st.selectbox(
            "Time",
            [
                "Morning",
                "Afternoon",
                "Evening",
                "Night"
            ]
        )
        food_time = st.selectbox(
            "Food instruction",
            [
                "As prescribed",
                "Before food",
                "After food",
                "With food"
            ]
        )
        start_date = st.date_input("Start date", value=date.today())
        notes = st.text_area("Notes", placeholder="Example: Doctor prescribed for 5 days")

        submitted = st.form_submit_button("Add Reminder")

        if submitted:
            if med_name.strip() == "":
                st.error("Please enter medicine name.")
            else:
                st.session_state.reminders.append(
                    {
                        "Medicine": med_name,
                        "Time": timing,
                        "Food Instruction": food_time,
                        "Start Date": start_date,
                        "Notes": notes
                    }
                )
                st.success("Reminder added successfully.")

    if st.session_state.reminders:
        st.markdown("### Today's Medicine Schedule")
        reminder_df = pd.DataFrame(st.session_state.reminders)
        st.dataframe(reminder_df, use_container_width=True)

        csv_data = reminder_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Reminder Schedule",
            data=csv_data,
            file_name="medicine_reminder_schedule.csv",
            mime="text/csv"
        )

        if st.button("Clear All Reminders"):
            st.session_state.reminders = []
            st.success("All reminders cleared.")
            st.rerun()
    else:
        st.info("No reminders added yet.")


# -----------------------------
# Tab 4: About Project
# -----------------------------
with tab4:
    st.markdown("## ℹ️ About MediGuide AI")

    st.write(
        """
        **MediGuide AI** is a smart medicine information web app built using Python and Streamlit.
        It helps users search for general medicine information such as usage, warnings,
        side effects, contraindications, and safety cautions.
        """
    )

    st.markdown("### 🚀 Main Features")

    st.markdown(
        """
        - Search tablets, injections, syrups, tonics, capsules, and other medicines
        - Show general usage information
        - Display warnings, side effects, and contraindications
        - Health safety profile for kidney, liver, diabetes, pregnancy, allergy, and age group
        - Medicine image scanner using OCR
        - Medicine reminder dashboard
        - Downloadable medicine report
        - Simple AI explanation
        """
    )

    st.markdown("### 🛠️ Tech Stack")

    st.markdown(
        """
        - Python
        - Streamlit
        - openFDA Drug Label API
        - RxNorm API
        - OCR
        - AI Summary Module
        - Pandas
        """
    )

    st.markdown("### ⚠️ Important Disclaimer")

    st.warning(
        "This project is only for educational and portfolio purposes. "
        "It does not replace a doctor, pharmacist, or medical professional. "
        "Never use this app to decide medicine dosage or treatment."
    )

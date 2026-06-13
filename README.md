# 💊 AI Medicine Safety & Drug Information Assistant

An AI-powered Streamlit web app that helps users search tablets, capsules, injections, syrups, tonics, and other medicines to understand official usage information, warnings, side effects, contraindications, drug interactions, and safety cautions in simple language.

> ⚠️ This project is for educational and portfolio purposes only. It is **not** medical advice, diagnosis, prescription, or dosage recommendation. Always consult a qualified doctor or pharmacist before using any medicine.

---

## 🚀 Features

- Search medicines by tablet, injection, syrup, tonic, capsule, or generic/brand name
- Fetch official public drug label information from openFDA
- Normalize medicine names using RxNorm/RxNav
- Show:
  - Used for / indications
  - Dosage and administration label text
  - Warnings
  - Boxed warnings
  - Side effects / adverse reactions
  - Contraindications
  - Drug interactions
  - Pregnancy/breastfeeding information
- Optional medicine strip/bottle image OCR
- Personal safety caution alerts for:
  - Kidney disease
  - Liver disease
  - Diabetes
  - Pregnancy
  - Breastfeeding
  - Allergy
  - Child / older adult use
- Simple AI explanation
- Downloadable medicine report
- Medicine reminder dashboard

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Requests
- Pandas
- Pillow
- pytesseract OCR
- openFDA Drug Label API
- RxNorm/RxNav API
- Optional Groq AI summary

---

## 📁 Project Structure

```text
ai_medicine_safety_assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
└── utils/
    ├── __init__.py
    ├── drug_api.py
    ├── ai_summary.py
    ├── ocr_utils.py
    └── report.py
```

---

## ▶️ How to Run Locally

### 1. Clone or download this project

```bash
git clone <your-repository-link>
cd ai_medicine_safety_assistant
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit app

```bash
streamlit run app.py
```

---

## 🔑 Optional Groq AI Setup

The app works without an AI API key using a safe rule-based summary.

To use Groq:

1. Create a `.env` file or add Streamlit secrets.
2. Add:

```text
GROQ_API_KEY=your_groq_api_key_here
```

3. Turn on the Groq toggle in the app sidebar.

---

## 📷 OCR Note

The image scanner uses `pytesseract`. On local systems, install Tesseract OCR also:

- Windows: install Tesseract OCR and add it to PATH
- Linux/Streamlit Cloud: may require system package installation

If OCR does not work, users can manually type the medicine name.

---

## ⚠️ Medical Safety Disclaimer

This app does not provide medical advice. It does not prescribe medicine, diagnose illness, recommend dosage, or confirm whether a medicine is safe. It only summarizes public label information for educational use. Always consult a qualified healthcare professional.

---

## 📌 Resume Project Points

**AI Medicine Safety Assistant | Python, Streamlit, openFDA API, RxNorm, OCR, AI**

- Built an AI-powered healthcare information web app to search tablets, injections, syrups, tonics, and capsules using public drug label APIs.
- Integrated openFDA and RxNorm APIs to display usage, warnings, side effects, contraindications, interactions, and generic drug names.
- Added OCR-based medicine image scanning, patient-specific caution alerts, downloadable reports, and a reminder dashboard with clear medical safety disclaimers.

---

## 🌐 Deployment on Streamlit Cloud

1. Upload this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create new app.
4. Select your repository.
5. Main file path:

```text
app.py
```

6. Deploy.

Optional: Add `GROQ_API_KEY` in Streamlit app secrets if you want AI-generated summaries.

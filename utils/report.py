from datetime import datetime


def yes_no(value):
    return "Yes" if value else "No"


def create_text_report(
    medicine_name,
    drug_data,
    age_group="Adult",
    kidney_issue=False,
    liver_issue=False,
    diabetes=False,
    pregnancy=False,
    allergy=False
):
    """
    Creates a downloadable text report for medicine information.
    This report is only for educational purposes.
    """

    report = f"""
==================================================
MediGuide AI - Medicine Information Report
==================================================

Generated On: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Medicine Name:
{medicine_name}

--------------------------------------------------
Health Safety Profile
--------------------------------------------------
Age Group: {age_group}
Kidney Disease / Kidney Problem: {yes_no(kidney_issue)}
Liver Disease / Liver Problem: {yes_no(liver_issue)}
Diabetes: {yes_no(diabetes)}
Pregnant / Planning Pregnancy: {yes_no(pregnancy)}
Known Medicine Allergy: {yes_no(allergy)}

--------------------------------------------------
Used For
--------------------------------------------------
{drug_data.get("indications", "Information not available.")}

--------------------------------------------------
How to Use
--------------------------------------------------
{drug_data.get("dosage", "Use only as prescribed by a doctor.")}

--------------------------------------------------
Warnings
--------------------------------------------------
{drug_data.get("warnings", "Information not available.")}

--------------------------------------------------
Side Effects
--------------------------------------------------
{drug_data.get("side_effects", "Information not available.")}

--------------------------------------------------
Contraindications
--------------------------------------------------
{drug_data.get("contraindications", "Information not available.")}

--------------------------------------------------
Personalized Safety Cautions
--------------------------------------------------
"""

    if age_group == "Child":
        report += "\n- Child caution: Medicine usage and dosage for children must be decided by a pediatric doctor."

    if age_group == "Senior Citizen":
        report += "\n- Senior citizen caution: Older adults may need special dosage adjustment and monitoring."

    if kidney_issue:
        report += "\n- Kidney caution: Some medicines can affect kidney function or need dose adjustment. Consult a doctor."

    if liver_issue:
        report += "\n- Liver caution: Some medicines may affect the liver. Consult a doctor before using."

    if diabetes:
        report += "\n- Diabetes caution: Some medicines can affect blood sugar levels. Consult your doctor."

    if pregnancy:
        report += "\n- Pregnancy caution: Do not use medicines during pregnancy without doctor advice."

    if allergy:
        report += "\n- Allergy caution: Avoid medicines that caused allergy before and consult a doctor immediately."

    if (
        age_group == "Adult"
        and not kidney_issue
        and not liver_issue
        and not diabetes
        and not pregnancy
        and not allergy
    ):
        report += "\n- No special safety profile selected. Still consult a doctor or pharmacist before using medicine."

    report += """

--------------------------------------------------
Doctor Advice
--------------------------------------------------
Do not start, stop, or change medicine dosage without consulting a doctor.
Seek urgent medical help if you experience breathing difficulty, swelling,
severe rash, chest pain, fainting, or serious allergic reaction.

--------------------------------------------------
Disclaimer
--------------------------------------------------
This report is for educational and portfolio purposes only.
It does not provide medical diagnosis, prescription, or dosage recommendation.
Always consult a qualified doctor or pharmacist before taking any medicine.

==================================================
End of Report
==================================================
"""

    return report

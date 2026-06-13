"""Create downloadable report text for the app."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List


def build_report(medicine_name: str, drug_info: Dict[str, str], caution_alerts: List[str], summary: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    alerts = "\n".join(f"- {a}" for a in caution_alerts)
    return f"""
AI Medicine Safety & Drug Information Assistant
Generated: {now}

IMPORTANT DISCLAIMER
This report is for educational and portfolio demonstration purposes only. It is not medical advice, diagnosis, prescription, or dosage recommendation. Always consult a qualified doctor or pharmacist before using any medicine. In emergency symptoms, seek urgent medical care.

SEARCHED MEDICINE
{medicine_name}

BASIC DETAILS
Display name: {drug_info.get('display_name')}
Generic name: {drug_info.get('generic_name')}
Brand name: {drug_info.get('brand_name')}
Manufacturer: {drug_info.get('manufacturer')}
Product type: {drug_info.get('product_type')}
Route: {drug_info.get('route')}
RxNorm RxCUI: {drug_info.get('rxnorm_rxcui')}
Data source: {drug_info.get('data_source_note')}

USED FOR / INDICATIONS
{drug_info.get('indications')}

DOSAGE AND ADMINISTRATION LABEL TEXT
{drug_info.get('dosage')}

WARNINGS
{drug_info.get('warnings')}

BOXED WARNING
{drug_info.get('boxed_warning')}

SIDE EFFECTS / ADVERSE REACTIONS
{drug_info.get('side_effects')}

CONTRAINDICATIONS
{drug_info.get('contraindications')}

DRUG INTERACTIONS
{drug_info.get('drug_interactions')}

PREGNANCY / BREASTFEEDING INFORMATION
{drug_info.get('pregnancy_or_breastfeeding')}

PERSONAL CAUTION ALERTS
{alerts}

SIMPLE SUMMARY
{summary}
""".strip()

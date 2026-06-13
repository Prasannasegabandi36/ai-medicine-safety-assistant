"""Utilities for searching official public medicine information.

Data sources:
- openFDA Drug Label API for label sections such as indications, warnings, dosage, adverse reactions.
- RxNav/RxNorm API for normalized drug names and RxCUIs.

This module is designed for an educational portfolio app. It does not provide
medical advice, diagnosis, prescription, or dosage recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
import requests

OPENFDA_LABEL_URL = "https://api.fda.gov/drug/label.json"
RXNAV_BASE_URL = "https://rxnav.nlm.nih.gov/REST"


@dataclass
class DrugInfo:
    searched_name: str
    display_name: str = "Information not available"
    generic_name: str = "Information not available"
    brand_name: str = "Information not available"
    manufacturer: str = "Information not available"
    product_type: str = "Information not available"
    route: str = "Information not available"
    purpose: str = "Information not available"
    indications: str = "Information not available"
    dosage: str = "Use only as prescribed by a qualified doctor or pharmacist."
    warnings: str = "Information not available"
    boxed_warning: str = "Information not available"
    side_effects: str = "Information not available"
    contraindications: str = "Information not available"
    drug_interactions: str = "Information not available"
    pregnancy_or_breastfeeding: str = "Information not available"
    rxnorm_rxcui: str = "Information not available"
    data_source_note: str = "Information shown from public drug label data where available."

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def _clean_text(value: Any, max_chars: int = 2500) -> str:
    """Convert API value into readable text and limit very long labels."""
    if value is None:
        return "Information not available"
    if isinstance(value, list):
        text = "\n\n".join(str(item).strip() for item in value if str(item).strip())
    else:
        text = str(value).strip()

    text = " ".join(text.split())
    if not text:
        return "Information not available"
    if len(text) > max_chars:
        return text[:max_chars].rsplit(" ", 1)[0] + "..."
    return text


def _first_list_value(data: Dict[str, Any], path: List[str]) -> str:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return "Information not available"
        current = current.get(key)
    if isinstance(current, list) and current:
        return _clean_text(current[0])
    return _clean_text(current)


def search_rxnorm_name(name: str) -> Dict[str, str]:
    """Return RxNorm normalized information for a drug name when available."""
    output = {
        "rxcui": "Information not available",
        "normalized_name": name.strip(),
        "status": "not_found",
    }
    name = name.strip()
    if not name:
        return output

    try:
        # Approximate terms handles spelling mistakes better than exact lookup.
        approx_url = f"{RXNAV_BASE_URL}/approximateTerm.json"
        approx_resp = requests.get(approx_url, params={"term": name, "maxEntries": 1}, timeout=10)
        approx_resp.raise_for_status()
        candidates = approx_resp.json().get("approximateGroup", {}).get("candidate", [])
        if candidates:
            rxcui = candidates[0].get("rxcui", "")
            output["rxcui"] = rxcui or output["rxcui"]
            output["status"] = "found"
            if rxcui:
                prop_url = f"{RXNAV_BASE_URL}/rxcui/{rxcui}/properties.json"
                prop_resp = requests.get(prop_url, timeout=10)
                if prop_resp.status_code == 200:
                    props = prop_resp.json().get("properties", {})
                    output["normalized_name"] = props.get("name", name)
            return output
    except Exception:
        # Do not fail the app if RxNav is unavailable.
        return output

    return output


def _openfda_query(name: str) -> Optional[Dict[str, Any]]:
    """Search openFDA labels by brand, generic, substance, and general fields."""
    name = name.strip()
    if not name:
        return None

    searches = [
        f'openfda.brand_name:"{name}" OR openfda.generic_name:"{name}" OR openfda.substance_name:"{name}"',
        f'openfda.brand_name:{name} OR openfda.generic_name:{name} OR openfda.substance_name:{name}',
        f'{name}',
    ]

    for search in searches:
        try:
            response = requests.get(OPENFDA_LABEL_URL, params={"search": search, "limit": 1}, timeout=12)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    return results[0]
        except Exception:
            continue
    return None


def get_drug_info(medicine_name: str) -> Optional[Dict[str, str]]:
    """Get official drug label information and return a clean dictionary."""
    medicine_name = medicine_name.strip()
    if not medicine_name:
        return None

    rx = search_rxnorm_name(medicine_name)
    search_term = rx["normalized_name"] if rx["status"] == "found" else medicine_name

    result = _openfda_query(search_term) or _openfda_query(medicine_name)
    if not result:
        return {
            "searched_name": medicine_name,
            "display_name": search_term,
            "generic_name": rx.get("normalized_name", medicine_name),
            "brand_name": "Information not available",
            "manufacturer": "Information not available",
            "product_type": "Information not available",
            "route": "Information not available",
            "purpose": "Information not available",
            "indications": "No official openFDA label information found for this search. Try the generic name or check spelling.",
            "dosage": "Use only as prescribed by a qualified doctor or pharmacist.",
            "warnings": "Information not available",
            "boxed_warning": "Information not available",
            "side_effects": "Information not available",
            "contraindications": "Information not available",
            "drug_interactions": "Information not available",
            "pregnancy_or_breastfeeding": "Information not available",
            "rxnorm_rxcui": rx.get("rxcui", "Information not available"),
            "data_source_note": "RxNorm may have identified the name, but openFDA label information was not found.",
        }

    openfda = result.get("openfda", {})
    generic_name = _clean_text(openfda.get("generic_name"))
    brand_name = _clean_text(openfda.get("brand_name"))
    display_name = brand_name if brand_name != "Information not available" else generic_name

    info = DrugInfo(
        searched_name=medicine_name,
        display_name=display_name,
        generic_name=generic_name,
        brand_name=brand_name,
        manufacturer=_clean_text(openfda.get("manufacturer_name")),
        product_type=_clean_text(openfda.get("product_type")),
        route=_clean_text(openfda.get("route")),
        purpose=_clean_text(result.get("purpose")),
        indications=_clean_text(result.get("indications_and_usage") or result.get("purpose")),
        dosage=_clean_text(result.get("dosage_and_administration")),
        warnings=_clean_text(result.get("warnings") or result.get("warnings_and_cautions")),
        boxed_warning=_clean_text(result.get("boxed_warning")),
        side_effects=_clean_text(result.get("adverse_reactions")),
        contraindications=_clean_text(result.get("contraindications")),
        drug_interactions=_clean_text(result.get("drug_interactions")),
        pregnancy_or_breastfeeding=_clean_text(
            result.get("pregnancy")
            or result.get("pregnancy_or_breast_feeding")
            or result.get("nursing_mothers")
        ),
        rxnorm_rxcui=rx.get("rxcui", "Information not available"),
        data_source_note="openFDA Drug Label API + RxNorm/RxNav API",
    )
    return info.to_dict()


def check_patient_cautions(drug_info: Dict[str, str], profile: Dict[str, Any]) -> List[str]:
    """Create conservative safety alerts from label text and user profile.

    These alerts are intentionally conservative and always direct the user to a clinician.
    """
    alerts: List[str] = []
    combined = " ".join(
        str(drug_info.get(key, ""))
        for key in ["warnings", "boxed_warning", "contraindications", "pregnancy_or_breastfeeding", "dosage", "side_effects"]
    ).lower()

    if profile.get("kidney_disease"):
        alerts.append("Kidney disease selected: consult a doctor/pharmacist before using this medicine. Dose and safety can depend on kidney function.")
        if any(word in combined for word in ["renal", "kidney", "nephro"]):
            alerts.append("The official label text appears to mention kidney/renal information. Read warnings carefully with a healthcare professional.")

    if profile.get("liver_disease"):
        alerts.append("Liver disease selected: consult a doctor/pharmacist before using this medicine. Some medicines require special caution.")
        if any(word in combined for word in ["hepatic", "liver"]):
            alerts.append("The official label text appears to mention liver/hepatic information. Medical review is important.")

    if profile.get("pregnant"):
        alerts.append("Pregnancy selected: do not use medicines without medical advice. Ask a doctor before starting or stopping any drug.")

    if profile.get("breastfeeding"):
        alerts.append("Breastfeeding selected: ask a doctor/pharmacist whether this medicine can pass into breast milk or affect the baby.")

    if profile.get("diabetes"):
        alerts.append("Diabetes selected: some medicines can affect blood sugar or interact with diabetes treatment. Check with a doctor/pharmacist.")

    allergy = str(profile.get("allergy", "")).strip()
    if allergy:
        alerts.append(f"Allergy noted: {allergy}. Avoid medicines you are allergic to and confirm ingredients with a pharmacist/doctor.")

    age_group = profile.get("age_group")
    if age_group in ["Child", "Older adult"]:
        alerts.append(f"{age_group} selected: dosing and side-effect risk may be different. Use only with professional advice.")

    if not alerts:
        alerts.append("No personal risk factor selected. Still, this app cannot confirm safety. Always follow doctor/pharmacist advice.")
    return alerts

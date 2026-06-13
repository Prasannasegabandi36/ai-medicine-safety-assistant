"""AI/simple summarization utilities.

The app uses a safe rule-based summary by default. An optional Groq integration is
included if the user adds GROQ_API_KEY in Streamlit secrets or .env.
"""

from __future__ import annotations

import os
from typing import Dict, List


def _shorten(text: str, limit: int = 650) -> str:
    text = " ".join(str(text or "").split())
    if not text or text == "Information not available":
        return "Information not available"
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def generate_rule_based_summary(medicine_name: str, drug_info: Dict[str, str], caution_alerts: List[str] | None = None) -> str:
    """Generate a plain-language educational summary without medical advice."""
    caution_alerts = caution_alerts or []
    used_for = _shorten(drug_info.get("indications", "Information not available"), 450)
    warnings = _shorten(drug_info.get("warnings", "Information not available"), 350)
    effects = _shorten(drug_info.get("side_effects", "Information not available"), 350)

    cautions = "\n".join([f"- {alert}" for alert in caution_alerts[:5]]) if caution_alerts else "- Consult a doctor/pharmacist before using this medicine."

    return f"""
### Simple educational summary for {medicine_name}

**What it may be used for:**  
{used_for}

**Important warning:**  
{warnings}

**Possible side effects:**  
{effects}

**Personal caution alerts:**  
{cautions}

**Safety note:** This is not a prescription, diagnosis, dosage plan, or emergency advice. Use medicines only as directed by a qualified healthcare professional.
""".strip()


def generate_groq_summary(medicine_name: str, drug_info: Dict[str, str], caution_alerts: List[str] | None = None) -> str | None:
    """Optional Groq summary. Returns None when key/library is unavailable."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        from groq import Groq
    except Exception:
        return None

    client = Groq(api_key=api_key)
    prompt = f"""
You are helping create an educational medicine information summary for a portfolio app.
Do not prescribe medicine. Do not give dosage instructions. Do not say a medicine is safe.
Use simple language and repeatedly advise consulting a doctor/pharmacist.

Medicine: {medicine_name}
Brand: {drug_info.get('brand_name')}
Generic: {drug_info.get('generic_name')}
Used for: {drug_info.get('indications')}
Dosage/admin label text: {drug_info.get('dosage')}
Warnings: {drug_info.get('warnings')}
Side effects: {drug_info.get('side_effects')}
Contraindications: {drug_info.get('contraindications')}
Personal cautions: {caution_alerts}

Return sections:
1. Simple meaning
2. General use
3. Major cautions
4. When to contact doctor urgently
5. Final disclaimer
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700,
        )
        return response.choices[0].message.content
    except Exception:
        return None


def generate_simple_summary(medicine_name: str, drug_info: Dict[str, str], caution_alerts: List[str] | None = None, use_groq: bool = False) -> str:
    if use_groq:
        ai_text = generate_groq_summary(medicine_name, drug_info, caution_alerts)
        if ai_text:
            return ai_text
    return generate_rule_based_summary(medicine_name, drug_info, caution_alerts)

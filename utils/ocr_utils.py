"""Optional OCR helper for medicine strip/bottle images."""

from __future__ import annotations

from typing import Optional
from PIL import Image


def extract_text_from_image(uploaded_file) -> str:
    """Extract text from an uploaded image using pytesseract when available.

    Streamlit Cloud may require additional system packages for Tesseract. The app
    handles failures gracefully and lets the user enter the medicine name manually.
    """
    if uploaded_file is None:
        return ""

    try:
        import pytesseract
    except Exception:
        return "OCR library not installed. Please install pytesseract and Tesseract OCR, or enter the medicine name manually."

    try:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as exc:
        return f"OCR failed: {exc}. Please enter the medicine name manually."

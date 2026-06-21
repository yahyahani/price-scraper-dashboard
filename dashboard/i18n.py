"""
i18n.py
-------
Kleine helper voor meertaligheid (NL / EN / AR).
Laadt JSON vertaalbestanden uit de locales/ map.

Small helper for multi-language support (NL / EN / AR).
Loads JSON translation files from the locales/ folder.

أداة مساعدة صغيرة لدعم تعدد اللغات (هولندي / إنجليزي / عربي).
"""

import json
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"

SUPPORTED_LANGUAGES = {
    "nl": "Nederlands",
    "en": "English",
    "ar": "العربية",
}

RTL_LANGUAGES = {"ar"}


def load_translations(lang_code: str) -> dict:
    """Laadt de vertalingen voor de gegeven taalcode. Valt terug op Engels."""
    path = LOCALES_DIR / f"{lang_code}.json"
    if not path.exists():
        path = LOCALES_DIR / "en.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_rtl(lang_code: str) -> bool:
    """Geeft True terug als de taal rechts-naar-links geschreven wordt (bv. Arabisch)."""
    return lang_code in RTL_LANGUAGES

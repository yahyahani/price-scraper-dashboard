"""
app.py
------
Dunne Streamlit-shell: laadt data en alle vertalingen (NL/EN/AR), en
rendert het volledige dashboard als één custom HTML/CSS/JS component.
Taal en thema wisselen puur client-side binnen dat component, zonder
page reload.

Starten / Run:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.database import fetch_all_items, fetch_price_history, init_db
from dashboard.i18n import load_translations, is_rtl, SUPPORTED_LANGUAGES
from dashboard.dashboard_app import render_full_dashboard

st.set_page_config(page_title="Price Scraper Dashboard", page_icon=None, layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stHeader"] { display: none; }
    iframe { border: none; display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Taal wisselt via een URL query-param (?lang=en) en een page reload,
# omdat RTL (Arabisch) de hele layout-richting omgooit - dat vraagt om
# een verse render in plaats van pure client-side DOM-manipulatie.
lang = st.query_params.get("lang", "nl")
if lang not in SUPPORTED_LANGUAGES:
    lang = "nl"

t = load_translations(lang)
rtl = is_rtl(lang)

init_db()
rows = fetch_all_items()
items = [dict(row) for row in rows]

history_by_title = {}
for title in sorted({i["title"] for i in items}):
    hist_rows = fetch_price_history(title)
    history_by_title[title] = [
        {"price": r["price"], "scraped_at": r["scraped_at"]} for r in hist_rows
    ]

html = render_full_dashboard(
    items=items,
    history_by_title=history_by_title,
    translations=t,
    languages=SUPPORTED_LANGUAGES,
    current_lang=lang,
    rtl=rtl,
)

components.html(html, height=1100, scrolling=True)

"""
app.py
------
Streamlit shell die alles doorgeeft aan custom HTML/CSS/JS componenten.
Taal en thema worden via URL query-params bijgehouden (?lang=nl&theme=dark),
zodat de custom sidebar-toggle écht het hele dashboard live kan herthema'en
zonder Streamlit's eigen (niet-stylebare) widgets te gebruiken.

Streamlit shell that delegates everything to custom HTML/CSS/JS components.
Language and theme are tracked via URL query params (?lang=nl&theme=dark),
so the custom sidebar toggle can truly re-theme the whole dashboard live
without relying on Streamlit's own (unstyleable) widgets.

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
from dashboard.custom_ui import render_dashboard_html
from dashboard.custom_history import render_history_html
from dashboard.custom_sidebar import render_sidebar_html

st.set_page_config(page_title="Price Scraper Dashboard", page_icon="📊", layout="wide")

# --- Taal & thema uit URL query-params lezen (met fallback naar dark/nl) ---
lang = st.query_params.get("lang", "nl")
if lang not in SUPPORTED_LANGUAGES:
    lang = "nl"

mode = st.query_params.get("theme", "dark")
if mode not in ("dark", "light"):
    mode = "dark"

t = load_translations(lang)
rtl = is_rtl(lang)

# --- Streamlit's eigen chrome neutraal/donker houden zodat het niet botst
#     met onze custom HTML-componenten die het echte thema tonen. ---
page_bg = "#0F0E0C" if mode == "dark" else "#FAF6EE"
st.markdown(
    f"""
    <style>
    .stApp {{ background: {page_bg}; }}
    .block-container {{ padding-top: 2rem; max-width: 1200px; }}
    [data-testid="stSidebar"] {{ background: {page_bg}; min-width: 280px; }}
    iframe {{ border: none; }}
    [data-testid="stSidebarHeader"] {{ display: none; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar: volledig custom component ---
with st.sidebar:
    sidebar_html = render_sidebar_html(
        languages=SUPPORTED_LANGUAGES,
        current_lang=lang,
        current_mode=mode,
        translations=t,
    )
    components.html(sidebar_html, height=420, scrolling=False)

# --- Data laden ---
init_db()
rows = fetch_all_items()

# Custom titel
st.markdown(
    f"""
    <div style="
        font-family: 'Fraunces', serif;
        font-size: 2.6rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: {'#F5F0E8' if mode == 'dark' else '#2A2520'};
        direction: {'rtl' if rtl else 'ltr'};
    ">{t['app_title']}</div>
    """,
    unsafe_allow_html=True,
)

if not rows:
    st.warning(f"**{t['no_data_title']}**\n\n{t['no_data_body']}")
    st.stop()

items = [dict(row) for row in rows]

tab_overview, tab_history, tab_about = st.tabs(
    [t["tab_overview"], t["tab_history"], t["tab_about"]]
)

# ============================================================
# TAB 1: Overzicht
# ============================================================
with tab_overview:
    html = render_dashboard_html(
        items=items,
        history_by_title={},
        translations=t,
        mode=mode,
        rtl=rtl,
    )
    components.html(html, height=900, scrolling=False)

# ============================================================
# TAB 2: Prijsgeschiedenis
# ============================================================
with tab_history:
    titles = sorted({i["title"] for i in items})
    history_by_title = {}
    for title in titles:
        hist_rows = fetch_price_history(title)
        history_by_title[title] = [
            {"price": r["price"], "scraped_at": r["scraped_at"]} for r in hist_rows
        ]

    html_hist = render_history_html(
        titles=titles,
        history_by_title=history_by_title,
        translations=t,
        mode=mode,
        rtl=rtl,
    )
    components.html(html_hist, height=480, scrolling=False)

# ============================================================
# TAB 3: Over dit project
# ============================================================
with tab_about:
    text_color = "#F5F0E8" if mode == "dark" else "#2A2520"
    st.markdown(f"<div style='color:{text_color}'>{t['about_text']}</div>", unsafe_allow_html=True)
    st.markdown(
        "[GitHub](https://github.com) · Python · Streamlit · SQLite · BeautifulSoup · Docker"
    )

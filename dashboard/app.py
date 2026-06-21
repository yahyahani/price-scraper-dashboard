"""
app.py
------
Streamlit dashboard met volledig custom HTML/CSS/JS UI voor de hoofdcontent
(cards, filters, tabel, grafieken) - Streamlit's eigen widgets worden alleen
nog gebruikt in de sidebar (taal- en thema-keuze), omdat Streamlit's
ingebouwde dataframe/inputs niet voldoende te stylen zijn voor een
modern, custom ontwerp.

Streamlit dashboard with fully custom HTML/CSS/JS UI for the main content
(cards, filters, table, charts) - Streamlit's own widgets are only used
in the sidebar (language/theme choice), since Streamlit's built-in
dataframe/inputs can't be styled enough for a modern, custom design.

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

st.set_page_config(page_title="Price Scraper Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------------------------
# Minimale CSS: alleen om Streamlit's eigen chrome (padding, sidebar-look)
# rustig te houden zodat het niet botst met onze custom HTML hieronder.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; max-width: 1200px; }
    [data-testid="stSidebar"] { min-width: 260px; }
    iframe { border: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Taal & thema selectie ---
if "lang" not in st.session_state:
    st.session_state.lang = "nl"

current_base = st.get_option("theme.base") or "dark"

with st.sidebar:
    st.caption("🌐 Taal / Language / اللغة")
    selected_label = st.selectbox(
        "Taal",
        options=list(SUPPORTED_LANGUAGES.values()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.lang),
        label_visibility="collapsed",
    )
    st.session_state.lang = next(
        code for code, label in SUPPORTED_LANGUAGES.items() if label == selected_label
    )

    st.divider()
    st.caption("🎨 Thema")
    st.write(f"Huidig: **{'🌙 Dark' if current_base == 'dark' else '☀️ Light'}**")
    with st.expander("Wisselen naar het andere thema"):
        if current_base == "dark":
            st.code("docker compose --profile light up", language="bash")
            st.caption("Lokaal: `streamlit run dashboard/app.py --theme.base light`")
        else:
            st.code("docker compose up", language="bash")
            st.caption("Lokaal: `streamlit run dashboard/app.py --theme.base dark`")

    st.divider()
    if st.button("🔄 Vernieuwen", use_container_width=True):
        st.rerun()

lang = st.session_state.lang
t = load_translations(lang)
rtl = is_rtl(lang)

# --- Data laden ---
init_db()
rows = fetch_all_items()

# Custom titel (los van Streamlit's h1, voor volledige typografische controle)
st.markdown(
    f"""
    <div style="
        font-family: 'Fraunces', serif;
        font-size: 2.6rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
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
# TAB 1: Overzicht (volledig custom HTML component)
# ============================================================
with tab_overview:
    html = render_dashboard_html(
        items=items,
        history_by_title={},  # niet nodig in deze tab
        translations=t,
        mode=current_base,
        rtl=rtl,
    )
    components.html(html, height=900, scrolling=False)

# ============================================================
# TAB 2: Prijsgeschiedenis (custom HTML component)
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
        mode=current_base,
        rtl=rtl,
    )
    components.html(html_hist, height=480, scrolling=False)

# ============================================================
# TAB 3: Over dit project
# ============================================================
with tab_about:
    st.write(t["about_text"])
    st.markdown(
        "[GitHub](https://github.com) · Python · Streamlit · SQLite · BeautifulSoup · Docker"
    )

"""
app.py
------
Streamlit dashboard dat de gescrapede data toont met grafieken en filters.
Ondersteunt Nederlands, Engels en Arabisch (incl. RTL layout).

Streamlit dashboard that displays scraped data with charts and filters.
Supports Dutch, English, and Arabic (including RTL layout).

لوحة تحكم Streamlit تعرض البيانات المسحوبة مع رسوم بيانية وفلاتر.
تدعم اللغات: الهولندية، الإنجليزية، والعربية (مع دعم الكتابة من اليمين لليسار).

Starten / Run / تشغيل:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Zorg dat we de scraper/ module kunnen importeren ongeacht vanwaar je runt
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.database import fetch_all_items, fetch_price_history, init_db
from dashboard.i18n import load_translations, is_rtl, SUPPORTED_LANGUAGES

st.set_page_config(page_title="Price Scraper Dashboard", page_icon="📊", layout="wide")

# --- Taal selectie (opgeslagen in session_state zodat het blijft staan) ---
if "lang" not in st.session_state:
    st.session_state.lang = "nl"

with st.sidebar:
    selected_label = st.selectbox(
        "🌐",
        options=list(SUPPORTED_LANGUAGES.values()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.lang),
    )
    # Zoek de taalcode terug bij het gekozen label
    st.session_state.lang = next(
        code for code, label in SUPPORTED_LANGUAGES.items() if label == selected_label
    )

lang = st.session_state.lang
t = load_translations(lang)
rtl = is_rtl(lang)

# --- RTL styling indien Arabisch ---
if rtl:
    st.markdown(
        """
        <style>
        .stApp { direction: rtl; text-align: right; }
        [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title(f"📊 {t['app_title']}")

# --- Data laden ---
init_db()
rows = fetch_all_items()

if not rows:
    st.warning(f"**{t['no_data_title']}**\n\n{t['no_data_body']}")
    st.stop()

df = pd.DataFrame([dict(row) for row in rows])
df["scraped_at"] = pd.to_datetime(df["scraped_at"])

tab_overview, tab_history, tab_about = st.tabs(
    [t["tab_overview"], t["tab_history"], t["tab_about"]]
)

# ============================================================
# TAB 1: Overzicht
# ============================================================
with tab_overview:
    col1, col2, col3 = st.columns(3)
    col1.metric(t["total_items"], len(df))
    col2.metric(t["avg_price"], f"£{df['price'].mean():.2f}" if df["price"].notna().any() else "-")
    col3.metric(t["last_scraped"], df["scraped_at"].max().strftime("%Y-%m-%d %H:%M"))

    st.divider()

    col_filter, col_search = st.columns(2)
    with col_filter:
        categories = [t["all_categories"]] + sorted(df["category"].dropna().unique().tolist())
        chosen_category = st.selectbox(t["filter_category"], categories)
    with col_search:
        search_term = st.text_input(t["search_placeholder"])

    filtered = df.copy()
    if chosen_category != t["all_categories"]:
        filtered = filtered[filtered["category"] == chosen_category]
    if search_term:
        filtered = filtered[filtered["title"].str.contains(search_term, case=False, na=False)]

    st.dataframe(
        filtered[["title", "price", "availability", "scraped_at"]].rename(
            columns={
                "title": t["table_title"],
                "price": t["table_price"],
                "availability": t["table_availability"],
                "scraped_at": t["table_scraped_at"],
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(t["price_distribution"])
    if filtered["price"].notna().any():
        fig = px.histogram(filtered, x="price", nbins=20)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: Prijsgeschiedenis
# ============================================================
with tab_history:
    titles = sorted(df["title"].unique().tolist())
    chosen_title = st.selectbox(t["select_item_history"], titles)

    history_rows = fetch_price_history(chosen_title)
    history_df = pd.DataFrame([dict(r) for r in history_rows])

    if len(history_df) < 2:
        st.info(t["no_history"])
    else:
        history_df["scraped_at"] = pd.to_datetime(history_df["scraped_at"])
        fig = px.line(history_df, x="scraped_at", y="price", markers=True, title=t["history_chart_title"])
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3: Over dit project
# ============================================================
with tab_about:
    st.write(t["about_text"])
    st.markdown(
        "[GitHub](https://github.com) · Python · Streamlit · SQLite · BeautifulSoup"
    )

if st.sidebar.button(t["refresh_button"]):
    st.rerun()

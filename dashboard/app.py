"""
app.py
------
Streamlit dashboard dat de gescrapede data toont met grafieken en filters.
Ondersteunt Nederlands, Engels en Arabisch (incl. RTL layout).

Het kleurthema (dark/light) wordt geregeld door Streamlit's eigen
ingebouwde theme-systeem (zie .streamlit/config.toml), aangevuld met
een gouden accent-laag (dashboard/theme.py). Dit garandeert dat ALLE
componenten consistent gekleurd zijn, inclusief de dataframe-tabel,
die los van CSS-injectie haar kleuren leest uit de server-config.

Starten / Run:
    streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.database import fetch_all_items, fetch_price_history, init_db
from dashboard.i18n import load_translations, is_rtl, SUPPORTED_LANGUAGES
from dashboard.theme import inject_theme, inject_rtl_override, ACCENT

st.set_page_config(page_title="Price Scraper Dashboard", page_icon="📊", layout="wide")
inject_theme()

# --- Taal selectie ---
if "lang" not in st.session_state:
    st.session_state.lang = "nl"

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
    current_base = st.get_option("theme.base")
    st.write(f"Huidig: **{'🌙 Dark' if current_base == 'dark' else '☀️ Light'}**")
    with st.expander("Wisselen naar het andere thema"):
        if current_base == "dark":
            st.code("docker compose --profile light up", language="bash")
            st.caption("Lokaal zonder Docker: `streamlit run dashboard/app.py --theme.base light`")
        else:
            st.code("docker compose up", language="bash")
            st.caption("Lokaal zonder Docker: `streamlit run dashboard/app.py --theme.base dark`")

lang = st.session_state.lang
t = load_translations(lang)
rtl = is_rtl(lang)

if rtl:
    inject_rtl_override()


def styled_fig(fig: go.Figure) -> go.Figure:
    """Past transparante achtergrond toe zodat de grafiek met het Streamlit-thema meekleurt."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig


st.title(t['app_title'])

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
        fig = go.Figure(
            data=[
                go.Histogram(
                    x=filtered["price"],
                    nbinsx=20,
                    marker=dict(color=ACCENT, line=dict(width=0)),
                    opacity=0.9,
                )
            ]
        )
        fig.update_layout(bargap=0.05)
        st.plotly_chart(styled_fig(fig), use_container_width=True)

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
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=history_df["scraped_at"],
                    y=history_df["price"],
                    mode="lines+markers",
                    line=dict(color=ACCENT, width=3, shape="spline"),
                    marker=dict(size=8, color=ACCENT),
                    fill="tozeroy",
                    fillcolor="rgba(232, 176, 75, 0.15)",
                )
            ]
        )
        fig.update_layout(title=t["history_chart_title"])
        st.plotly_chart(styled_fig(fig), use_container_width=True)

# ============================================================
# TAB 3: Over dit project
# ============================================================
with tab_about:
    st.write(t["about_text"])
    st.markdown(
        "[GitHub](https://github.com) · Python · Streamlit · SQLite · BeautifulSoup · Docker"
    )

if st.sidebar.button(t["refresh_button"]):
    st.rerun()

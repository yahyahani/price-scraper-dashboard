"""
theme.py
--------
Custom styling-laag boven op Streamlit's eigen ingebouwde thema-systeem
(zie .streamlit/config.toml). We laten Streamlit zelf de basiskleuren
voor alle componenten (incl. de dataframe-tabel) regelen, en voegen hier
alleen het signature "gouden gloed" effect toe op cards, knoppen en titels.

Dark/light wisselen gebeurt via een herstart met --theme.base, omdat
Streamlit's dataframe-component zijn kleuren leest uit de server-config
en niet via losse CSS-overschrijving bereikbaar is.
"""

import streamlit as st

ACCENT = "#E8B04B"
ACCENT_SOFT = "#E8B04B22"
ACCENT_GLOW = "#E8B04B50"


def inject_theme() -> None:
    """Injecteert de gouden accent-laag boven op Streamlit's eigen thema."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap');

        /* ---- Titels: serif voor karakter ---- */
        h1, h2, h3 {{
            font-family: 'Fraunces', serif !important;
            letter-spacing: -0.01em;
        }}

        /* ---- Metric cards: het signature element ----
           Subtiele kaart met gouden gloed bij hover */
        [data-testid="stMetric"] {{
            background: color-mix(in srgb, var(--background-color) 96%, {ACCENT} 4%);
            border: 1px solid rgba(232, 176, 75, 0.25);
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: {ACCENT};
            box-shadow: 0 0 22px {ACCENT_GLOW};
            transform: translateY(-2px);
        }}

        [data-testid="stMetricLabel"] {{
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-size: 0.8rem;
            opacity: 0.7;
        }}

        /* ---- Tabs: gouden onderstreping voor actieve tab ---- */
        .stTabs [aria-selected="true"] {{
            color: {ACCENT} !important;
            border-bottom: 2px solid {ACCENT} !important;
        }}

        /* ---- Knoppen: gouden gloed bij hover ---- */
        .stButton button:hover {{
            border-color: {ACCENT} !important;
            color: {ACCENT} !important;
            box-shadow: 0 0 14px {ACCENT_GLOW};
        }}

        /* ---- Inputs: gouden focus-rand ---- */
        .stTextInput input:focus,
        .stSelectbox div[data-baseweb="select"]:focus-within > div {{
            border-color: {ACCENT} !important;
            box-shadow: 0 0 0 1px {ACCENT_GLOW} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_rtl_override() -> None:
    """Extra RTL-styling voor Arabisch."""
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )

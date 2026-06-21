"""
theme.py
--------
Custom styling voor het dashboard: dark/light mode met een warme,
"boekenleer en goud" esthetiek (toepasselijk voor een boeken-scraper).

Custom styling for the dashboard: dark/light mode with a warm
"leather and gold" aesthetic (fitting for a book scraper).

تنسيق مخصص للوحة التحكم: نمط فاتح وداكن بطابع ذهبي أنيق.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------

DARK = {
    "bg": "#0F0E0C",
    "bg_gradient": "radial-gradient(circle at 15% 0%, #1C1812 0%, #0F0E0C 55%)",
    "surface": "#1A1714",
    "surface_hover": "#221E18",
    "border": "#332D24",
    "text": "#F5F0E8",
    "text_muted": "#A89A85",
    "accent": "#E8B04B",
    "accent_soft": "#E8B04B26",
    "accent_glow": "#E8B04B55",
    "accent2": "#7BA098",
}

LIGHT = {
    "bg": "#FAF6EE",
    "bg_gradient": "radial-gradient(circle at 15% 0%, #FFFDF8 0%, #FAF6EE 55%)",
    "surface": "#FFFFFF",
    "surface_hover": "#FFFCF6",
    "border": "#E8DFCB",
    "text": "#2A2520",
    "text_muted": "#7A6F5E",
    "accent": "#C8923A",
    "accent_soft": "#C8923A1A",
    "accent_glow": "#C8923A40",
    "accent2": "#4F7A70",
}


def inject_theme(mode: str = "dark") -> None:
    """Injecteert custom CSS in de Streamlit app. mode = 'dark' of 'light'."""
    c = DARK if mode == "dark" else LIGHT

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            --bg: {c['bg']};
            --surface: {c['surface']};
            --surface-hover: {c['surface_hover']};
            --border: {c['border']};
            --text: {c['text']};
            --text-muted: {c['text_muted']};
            --accent: {c['accent']};
            --accent-soft: {c['accent_soft']};
            --accent-glow: {c['accent_glow']};
            --accent2: {c['accent2']};
        }}

        .stApp {{
            background: {c['bg_gradient']};
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }}

        /* ---- Sidebar ---- */
        [data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid var(--border);
        }}

        /* ---- Headings: serif voor karakter, verwijst naar boekentypografie ---- */
        h1, h2, h3 {{
            font-family: 'Fraunces', serif;
            letter-spacing: -0.01em;
        }}

        h1 {{
            font-weight: 600;
            background: linear-gradient(135deg, var(--text) 30%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* ---- Metric cards: het signature element ----
           Glanzende rand die oplicht bij hover, als goudopdruk op een boekenkaft */
        [data-testid="stMetric"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            position: relative;
            overflow: hidden;
            transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }}

        [data-testid="stMetric"]::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--accent-soft) 0%, transparent 60%);
            opacity: 0;
            transition: opacity 0.25s ease;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: var(--accent);
            box-shadow: 0 0 24px var(--accent-glow), 0 4px 12px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }}

        [data-testid="stMetric"]:hover::before {{
            opacity: 1;
        }}

        [data-testid="stMetricValue"] {{
            font-family: 'Fraunces', serif;
            font-weight: 600;
            color: var(--text);
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--text-muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1.5rem;
            border-bottom: 1px solid var(--border);
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--text-muted);
            font-weight: 500;
            padding-bottom: 0.6rem;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
            border-bottom: 2px solid var(--accent) !important;
        }}

        /* ---- DataFrame / tabel ---- */
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }}

        /* ---- Inputs (selectbox, text_input) ---- */
        .stSelectbox div[data-baseweb="select"] > div,
        .stTextInput input {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text) !important;
        }}

        .stTextInput input:focus,
        .stSelectbox div[data-baseweb="select"]:focus-within > div {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent-glow) !important;
        }}

        /* ---- Knoppen: subtiele gouden glow bij hover ---- */
        .stButton button {{
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .stButton button:hover {{
            border-color: var(--accent);
            color: var(--accent);
            box-shadow: 0 0 16px var(--accent-glow);
        }}

        /* ---- Divider subtieler maken ---- */
        hr {{
            border-color: var(--border);
        }}

        /* ---- Warning/info boxes met thema-kleur ---- */
        [data-testid="stAlert"] {{
            background: var(--surface);
            border: 1px solid var(--accent);
            border-radius: 12px;
        }}

        /* ---- Scrollbar subtiel thema ---- */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 8px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_rtl_override() -> None:
    """Extra RTL-styling die los van het kleurthema werkt (voor Arabisch)."""
    st.markdown(
        """
        <style>
        .stApp { direction: rtl; text-align: right; }
        [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        [data-testid="stMetric"] { text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )

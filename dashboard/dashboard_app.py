"""
dashboard_app.py
-----------------
Eén volledig zelfstandig HTML/CSS/JS dashboard (sidebar + content samen),
gerenderd als één component via st.components.v1.html.

Dark/light wisselt puur client-side door een CSS-class te togglen op
<body>. Taal wisselt via URL query-param + parent DOM script injection
(Streamlit's sandbox heeft geen allow-top-navigation, maar wel
allow-same-origin + allow-scripts, waardoor we een script-element in
window.parent.document kunnen injecteren om toch te navigeren).
"""

import json


ICON_MOON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
ICON_SUN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
ICON_REFRESH = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>'
ICON_SEARCH = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/></svg>'
ICON_LOGO = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'


def render_full_dashboard(
    items: list[dict],
    history_by_title: dict,
    translations: dict,
    languages: dict,
    current_lang: str,
    rtl: bool,
) -> str:
    t = translations
    data_json = json.dumps(items, ensure_ascii=False)
    history_json = json.dumps(history_by_title, ensure_ascii=False)
    t_json = json.dumps(t, ensure_ascii=False)
    languages_json = json.dumps(languages, ensure_ascii=False)
    direction = "rtl" if rtl else "ltr"
    rtl_js = "true" if rtl else "false"

    return f"""<!DOCTYPE html>
<html dir="{direction}">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─── Design tokens ─────────────────────────────────────── */
:root {{
    /* Backgrounds */
    --bg:        #06060C;
    --surface:   #0E0E18;
    --surface-2: #14141F;
    --surface-3: #1A1A28;

    /* Borders */
    --border:    #1E1E30;
    --border-hi: #2A2A3F;

    /* Text */
    --text:      #EEEEF5;
    --text-sub:  #9191A8;
    --text-dim:  #3E3E58;

    /* Accent – electric violet */
    --accent:       #8B5CF6;
    --accent-hi:    #A78BFA;
    --accent-lo:    #7C3AED;
    --accent-dim:   rgba(139,92,246,.12);
    --accent-glow:  rgba(139,92,246,.35);
    --accent-on:    #FFFFFF;

    /* Accent 2 – amber-orange */
    --accent2:      #F97316;
    --accent2-dim:  rgba(249,115,22,.12);
    --accent2-glow: rgba(249,115,22,.30);

    /* Emerald – positive / in-stock */
    --green:     #10B981;
    --green-dim: rgba(16,185,129,.12);
    --green-brd: rgba(16,185,129,.25);

    /* Motion */
    --ease:  cubic-bezier(.16,1,.3,1);
    --fast:  0.15s;
    --mid:   0.25s;
}}

body.light {{
    --bg:        #F4F3FA;
    --surface:   #FFFFFF;
    --surface-2: #EDE9FF;
    --surface-3: #E6E0FF;
    --border:    #E2DCF5;
    --border-hi: #CEC6EC;
    --text:      #15131E;
    --text-sub:  #6B677F;
    --text-dim:  #BDB8D4;
    --accent:       #7C3AED;
    --accent-hi:    #6D28D9;
    --accent-lo:    #5B21B6;
    --accent-dim:   rgba(124,58,237,.10);
    --accent-glow:  rgba(124,58,237,.22);
    --accent2:      #EA580C;
    --accent2-dim:  rgba(234,88,12,.10);
    --accent2-glow: rgba(234,88,12,.18);
    --green:     #059669;
    --green-dim: rgba(5,150,105,.10);
    --green-brd: rgba(5,150,105,.20);
}}

/* ─── Reset ─────────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin:0; padding:0; }}

/* ─── Body & ambient mesh ────────────────────────────────── */
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    -webkit-font-smoothing: antialiased;
    transition: background var(--mid) var(--ease), color var(--mid) var(--ease);
    /* mesh gradient — subtle depth behind everything */
    background-image:
        radial-gradient(ellipse 90% 55% at 15% -5%,  rgba(139,92,246,.07)  0%, transparent 55%),
        radial-gradient(ellipse 70% 45% at 85% 105%, rgba(249,115,22,.05)  0%, transparent 55%);
}}
body.light {{
    background-image:
        radial-gradient(ellipse 90% 55% at 15% -5%,  rgba(124,58,237,.05)  0%, transparent 55%),
        radial-gradient(ellipse 70% 45% at 85% 105%, rgba(234,88,12,.03)   0%, transparent 55%);
}}

/* ─── Layout ─────────────────────────────────────────────── */
.layout {{
    display: grid;
    grid-template-columns: 248px 1fr;
    min-height: 100vh;
    direction: {direction};
}}
@media (max-width: 768px) {{
    .layout {{ grid-template-columns: 1fr; }}
    .sidebar {{ display: none; }}
}}

/* ─── Sidebar ────────────────────────────────────────────── */
.sidebar {{
    background: var(--surface);
    border-{"left" if rtl else "right"}: 1px solid var(--border);
    padding: 20px 14px 28px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
    overflow: hidden;
}}
/* ambient top-glow in sidebar */
.sidebar::before {{
    content: '';
    position: absolute;
    top: -80px; {"left" if rtl else "right"}: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(139,92,246,.08) 0%, transparent 70%);
    pointer-events: none;
}}

/* wordmark / logo row */
.sidebar-logo {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 10px 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 10px;
}}
.sidebar-logo-icon {{
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    color: #fff;
    flex-shrink: 0;
    box-shadow: 0 4px 14px var(--accent-glow);
}}
.sidebar-logo-text {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: -.02em;
    color: var(--text);
    line-height: 1.1;
}}
.sidebar-logo-sub {{
    font-size: 10px;
    font-weight: 500;
    color: var(--text-sub);
    margin-top: 1px;
}}

/* sidebar group */
.sb-group {{ margin-top: 10px; }}
.sb-label {{
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 0 10px;
    margin-bottom: 4px;
}}

/* ─── Language buttons ───────────────────────────────────── */
.lang-buttons {{
    display: flex;
    flex-direction: column;
    gap: 2px;
}}
.lang-btn {{
    width: 100%;
    text-align: {"right" if rtl else "left"};
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 8px 12px;
    color: var(--text-sub);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: background var(--fast) var(--ease),
                border-color var(--fast) var(--ease),
                color var(--fast) var(--ease),
                box-shadow var(--fast) var(--ease);
    display: block;
    position: relative;
    overflow: hidden;
}}
.lang-btn.active {{
    background: var(--accent-dim);
    border-color: rgba(139,92,246,.30);
    color: var(--accent-hi);
    font-weight: 600;
    box-shadow: 0 0 0 1px rgba(139,92,246,.12) inset,
                0 4px 16px rgba(139,92,246,.10);
}}
.lang-btn:not(.active):hover {{
    background: var(--surface-2);
    border-color: var(--border-hi);
    color: var(--text);
}}

/* ─── Theme segment ──────────────────────────────────────── */
.seg-control {{
    display: flex;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 3px;
    gap: 3px;
}}
.seg-option {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    padding: 7px 0;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-sub);
    cursor: pointer;
    transition: all var(--fast) var(--ease);
    border: none;
    background: transparent;
    font-family: inherit;
    user-select: none;
}}
.seg-option.active {{
    background: linear-gradient(140deg, var(--accent) 0%, var(--accent-lo) 100%);
    color: #fff;
    box-shadow: 0 2px 10px var(--accent-glow),
                0 0 0 1px rgba(255,255,255,.08) inset;
}}
.seg-option:not(.active):hover {{ background: var(--border); color: var(--text); }}

/* ─── Refresh / icon button ──────────────────────────────── */
.icon-btn {{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px;
    color: var(--text-sub);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--fast) var(--ease);
    font-family: inherit;
}}
.icon-btn:hover {{
    border-color: var(--accent);
    color: var(--accent-hi);
    background: var(--accent-dim);
    box-shadow: 0 0 18px var(--accent-glow);
}}

/* ─── Main content ───────────────────────────────────────── */
.main {{ padding: 40px 48px; max-width: 1200px; }}

/* ─── Title ──────────────────────────────────────────────── */
h1.title {{
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -.03em;
    margin: 0 0 4px;
    /* gradient text */
    background: linear-gradient(135deg, var(--text) 30%, var(--text-sub) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

/* ─── Tabs ───────────────────────────────────────────────── */
.tabs {{
    display: flex;
    gap: 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
    margin-top: 22px;
}}
.tab {{
    padding: 10px 0;
    margin-{"left" if rtl else "right"}: 28px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-sub);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: color var(--fast) var(--ease), border-color var(--fast) var(--ease);
    position: relative;
    user-select: none;
    white-space: nowrap;
}}
.tab.active {{
    color: var(--text);
    border-bottom-color: var(--accent);
}}
/* glow under active tab line */
.tab.active::after {{
    content: '';
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    box-shadow: 0 0 10px var(--accent-glow), 0 0 3px var(--accent-glow);
    border-radius: 2px 2px 0 0;
}}
.tab:hover:not(.active) {{ color: var(--text); }}
.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; }}

/* ─── Stat cards ─────────────────────────────────────────── */
.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(196px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
}}
.stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color var(--mid) var(--ease),
                transform   var(--mid) var(--ease),
                box-shadow  var(--mid) var(--ease);
    cursor: default;
}}
/* gradient top stripe */
.stat-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity var(--mid) var(--ease);
}}
/* inner radial glow */
.stat-card::after {{
    content: '';
    position: absolute;
    top: -30%; left: -20%;
    width: 140%; height: 140%;
    background: radial-gradient(ellipse 60% 50% at 30% 0%,
        rgba(139,92,246,.08) 0%, transparent 70%);
    opacity: 0;
    transition: opacity var(--mid) var(--ease);
    pointer-events: none;
}}
.stat-card:hover {{
    border-color: rgba(139,92,246,.40);
    transform: translateY(-3px);
    box-shadow:
        0 0 0 1px rgba(139,92,246,.15),
        0 8px 30px rgba(139,92,246,.12),
        0 2px 8px rgba(0,0,0,.4);
}}
.stat-card:hover::before {{ opacity: 1; }}
.stat-card:hover::after  {{ opacity: 1; }}

.stat-label {{
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 10px;
}}
.stat-value {{
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -.02em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}}
/* gradient number for the price card */
.stat-value.accent {{
    background: linear-gradient(135deg, var(--accent-hi) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

/* ─── Filter controls ────────────────────────────────────── */
.controls {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 18px;
}}
@media (max-width: 600px) {{ .controls {{ grid-template-columns: 1fr; }} }}

.control-group label {{
    display: block;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 7px;
}}
.control-input,
.control-select {{
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 13px;
    color: var(--text);
    font-size: 13px;
    font-family: inherit;
    outline: none;
    appearance: none;
    transition: border-color var(--fast) var(--ease),
                box-shadow   var(--fast) var(--ease);
}}
.control-input:focus,
.control-select:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-dim), 0 0 14px rgba(139,92,246,.08);
}}
.control-input::placeholder {{ color: var(--text-dim); }}

.search-wrap {{ position: relative; }}
.search-wrap svg {{
    position: absolute;
    {"right" if rtl else "left"}: 12px;
    top: 50%; transform: translateY(-50%);
    color: var(--text-sub);
    pointer-events: none;
}}
.search-wrap .control-input {{ padding-{"right" if rtl else "left"}: 34px; }}

/* ─── Table ──────────────────────────────────────────────── */
.table-wrap {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,.4);
}}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}

thead th {{
    text-align: {"right" if rtl else "left"};
    padding: 12px 18px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: var(--text-sub);
    background: var(--surface-2);
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    white-space: nowrap;
    user-select: none;
    transition: color var(--fast) var(--ease);
}}
thead th:hover {{ color: var(--accent-hi); }}

tbody td {{
    padding: 12px 18px;
    border-bottom: 1px solid var(--border);
    text-align: {"right" if rtl else "left"};
    transition: background var(--fast) var(--ease);
}}
tbody td.num {{
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    color: var(--accent-hi);
}}
tbody tr:hover td {{ background: var(--surface-2); }}
tbody tr:last-child td {{ border-bottom: none; }}

.badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    background: var(--green-dim);
    color: var(--green);
    border: 1px solid var(--green-brd);
    letter-spacing: .01em;
}}
.empty-row td {{
    text-align: center;
    color: var(--text-sub);
    padding: 52px;
    font-size: 13px;
}}

/* ─── Pagination ─────────────────────────────────────────── */
.pagination {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    padding: 14px;
    border-top: 1px solid var(--border);
}}
.page-btn {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-sub);
    border-radius: 7px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: all var(--fast) var(--ease);
    min-width: 32px;
}}
.page-btn:hover {{
    border-color: var(--accent);
    color: var(--accent-hi);
    background: var(--accent-dim);
}}
.page-btn.active {{
    background: linear-gradient(140deg, var(--accent) 0%, var(--accent-lo) 100%);
    border-color: transparent;
    color: #fff;
    box-shadow: 0 2px 12px var(--accent-glow);
}}

/* ─── Bar chart ──────────────────────────────────────────── */
.chart-section {{ margin-top: 4px; }}
.chart-section h3 {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -.01em;
    margin-bottom: 14px;
    color: var(--text);
}}
.bars {{
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 16px 0;
}}
.bar-col {{ flex: 1; height: 100%; display: flex; align-items: flex-end; }}
.bar {{
    width: 100%;
    background: linear-gradient(180deg,
        var(--accent-hi) 0%,
        var(--accent)    60%,
        var(--accent-lo) 100%);
    border-radius: 4px 4px 0 0;
    min-height: 3px;
    position: relative;
    transition: filter var(--fast) var(--ease),
                transform var(--fast) var(--ease);
    transform-origin: bottom;
}}
.bar:hover {{
    filter: brightness(1.25) saturate(1.2);
    transform: scaleY(1.04);
    box-shadow: 0 -4px 16px var(--accent-glow);
}}
.bar:hover::after {{
    content: attr(data-tooltip);
    position: absolute;
    bottom: calc(100% + 6px);
    left: 50%;
    transform: translateX(-50%);
    background: var(--surface-3);
    color: var(--text);
    font-size: 10px;
    font-weight: 600;
    padding: 4px 9px;
    border-radius: 7px;
    white-space: nowrap;
    border: 1px solid var(--border-hi);
    box-shadow: 0 4px 20px rgba(0,0,0,.4);
    font-family: 'Inter', sans-serif;
    pointer-events: none;
    z-index: 10;
}}
.bar-axis {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-sub);
    margin-top: 7px;
    padding: 0 4px;
}}

/* ─── Line chart / history ───────────────────────────────── */
.history-select {{ max-width: 380px; margin-bottom: 22px; }}
.chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,.4);
}}
.chart-card h3 {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -.01em;
    margin: 0 0 18px;
}}
.empty-state {{
    text-align: center;
    color: var(--text-sub);
    padding: 56px 16px;
    font-size: 13px;
}}

/* ─── About page ─────────────────────────────────────────── */
.about-text {{
    font-size: 14px;
    line-height: 1.75;
    color: var(--text);
    max-width: 600px;
}}
.about-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 18px;
}}
.about-chip {{
    background: var(--surface-2);
    border: 1px solid var(--border-hi);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-sub);
    letter-spacing: .01em;
}}

/* ─── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: var(--border-hi);
    border-radius: 8px;
    transition: background var(--fast) var(--ease);
}}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

/* ─── Select arrow trick ─────────────────────────────────── */
select.control-select {{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236B6B80' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 34px;
}}
</style>
</head>
<body>

<div class="layout">

    <!-- ── Sidebar ── -->
    <aside class="sidebar">

        <!-- Logo row -->
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">{ICON_LOGO}</div>
            <div>
                <div class="sidebar-logo-text">PriceScraper</div>
                <div class="sidebar-logo-sub">Dashboard</div>
            </div>
        </div>

        <!-- Language -->
        <div class="sb-group">
            <div class="sb-label">Language</div>
            <div class="lang-buttons" id="langButtons"></div>
        </div>

        <!-- Theme -->
        <div class="sb-group" style="margin-top:6px;">
            <div class="sb-label">Theme</div>
            <div class="seg-control">
                <button class="seg-option active" id="darkBtn" type="button">{ICON_MOON} Dark</button>
                <button class="seg-option" id="lightBtn" type="button">{ICON_SUN} Light</button>
            </div>
        </div>

        <!-- Refresh -->
        <div style="margin-top:auto; padding-top:16px;">
            <button class="icon-btn" id="refreshBtn" type="button">
                {ICON_REFRESH}
                <span id="refreshLabel"></span>
            </button>
        </div>

    </aside>

    <!-- ── Main ── -->
    <div class="main">
        <h1 class="title" id="appTitle"></h1>
        <div class="tabs">
            <div class="tab active" data-tab="overview"  id="tabOverviewLabel"></div>
            <div class="tab"        data-tab="history"   id="tabHistoryLabel"></div>
            <div class="tab"        data-tab="about"     id="tabAboutLabel"></div>
        </div>
        <div class="tab-panel active" id="panel-overview"></div>
        <div class="tab-panel"        id="panel-history"></div>
        <div class="tab-panel"        id="panel-about"></div>
    </div>

</div><!-- /.layout -->

<script>
const ITEMS        = {data_json};
const HISTORY      = {history_json};
const T            = {t_json};
const LANGUAGES    = {languages_json};
const CURRENT_LANG = "{current_lang}";
const RTL          = {rtl_js};
const ICON_SEARCH_SVG = `{ICON_SEARCH}`;

let state = {{
    theme:        "dark",
    category:     "ALL",
    search:       "",
    sortKey:      "scraped_at",
    sortDir:      "desc",
    page:         1,
    pageSize:     8,
    activeTab:    "overview",
    historyTitle: null,
}};

/* ── utils ── */
function fmtPrice(p) {{
    return (p === null || p === undefined) ? "-" : "£" + Number(p).toFixed(2);
}}

/* ── theme ── */
function applyTheme() {{
    document.body.className = state.theme === "light" ? "light" : "";
    document.getElementById("darkBtn").classList.toggle("active", state.theme === "dark");
    document.getElementById("lightBtn").classList.toggle("active", state.theme === "light");
}}
document.getElementById("darkBtn").addEventListener("click", () => {{ state.theme = "dark";  applyTheme(); }});
document.getElementById("lightBtn").addEventListener("click", () => {{ state.theme = "light"; applyTheme(); }});

/* ── refresh ── */
document.getElementById("refreshBtn").addEventListener("click", () => {{ window.location.reload(); }});

/* ── static labels + language buttons ── */
function renderStaticLabels() {{
    document.getElementById("refreshLabel").textContent = T.refresh_button || "Refresh";
    document.getElementById("appTitle").textContent     = T.app_title;
    document.getElementById("tabOverviewLabel").textContent = T.tab_overview;
    document.getElementById("tabHistoryLabel").textContent  = T.tab_history;
    document.getElementById("tabAboutLabel").textContent    = T.tab_about;

    const langButtons = document.getElementById("langButtons");
    langButtons.innerHTML = Object.entries(LANGUAGES).map(([code, label]) => {{
        const isActive = code === CURRENT_LANG;
        return `<button class="lang-btn ${{isActive ? 'active' : ''}}" type="button" onclick="changeLang('${{code}}')">${{label}}</button>`;
    }}).join("");
}}

// Streamlit sandbox: allow-same-origin + allow-scripts but NO allow-top-navigation.
// <a target="_top"> is blocked. Injecting a script element into window.parent.document
// runs in the parent's context and can therefore navigate it.
function changeLang(code) {{
    try {{
        const url = new URL(window.parent.location.href);
        url.searchParams.set("lang", code);
        const s = window.parent.document.createElement("script");
        s.textContent = "window.location.href=" + JSON.stringify(url.toString()) + ";";
        window.parent.document.head.appendChild(s);
        s.remove();
    }} catch (e) {{
        console.error("Language switch failed:", e);
    }}
}}

/* ── tabs ── */
document.querySelectorAll(".tab").forEach(tabEl => {{
    tabEl.addEventListener("click", () => {{
        state.activeTab = tabEl.getAttribute("data-tab");
        document.querySelectorAll(".tab").forEach(el => el.classList.toggle("active", el === tabEl));
        document.querySelectorAll(".tab-panel").forEach(el => {{
            el.classList.toggle("active", el.id === "panel-" + state.activeTab);
        }});
        resizeFrame();
    }});
}});

/* ── data helpers ── */
function getCategories() {{
    return Array.from(new Set(ITEMS.map(i => i.category).filter(Boolean))).sort();
}}
function filteredItems() {{
    let arr = ITEMS.slice();
    if (state.category !== "ALL") arr = arr.filter(i => i.category === state.category);
    if (state.search.trim()) {{
        const q = state.search.trim().toLowerCase();
        arr = arr.filter(i => i.title.toLowerCase().includes(q));
    }}
    arr.sort((a, b) => {{
        let av = a[state.sortKey], bv = b[state.sortKey];
        if (av == null) av = -Infinity;
        if (bv == null) bv = -Infinity;
        if (typeof av === "string") return state.sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
        return state.sortDir === "asc" ? av - bv : bv - av;
    }});
    return arr;
}}

/* ── overview panel ── */
function renderOverview() {{
    const arr = filteredItems();
    const prices = ITEMS.map(i => i.price).filter(p => p != null);
    const avg = prices.length ? prices.reduce((a, b) => a + b, 0) / prices.length : null;
    const lastScraped = ITEMS.reduce((max, i) => i.scraped_at > max ? i.scraped_at : max, "");

    const cats = getCategories();
    const catOptions = `<option value="ALL">${{T.all_categories}}</option>` +
        cats.map(c => `<option value="${{c}}" ${{state.category === c ? "selected" : ""}}>${{c}}</option>`).join("");

    const maxPage = Math.max(1, Math.ceil(arr.length / state.pageSize));
    if (state.page > maxPage) state.page = maxPage;
    const start = (state.page - 1) * state.pageSize;
    const pageItems = arr.slice(start, start + state.pageSize);

    const rows = pageItems.length
        ? pageItems.map(i => `
            <tr>
                <td>${{i.title}}</td>
                <td class="num">${{fmtPrice(i.price)}}</td>
                <td><span class="badge">${{i.availability || "-"}}</span></td>
                <td>${{(i.scraped_at || "").replace("T", " ").slice(0, 19)}}</td>
            </tr>`).join("")
        : `<tr class="empty-row"><td colspan="4">${{T.no_data_title}}</td></tr>`;

    /* pagination */
    let pageButtons = "";
    for (let p = 1; p <= maxPage; p++) {{
        if (p === 1 || p === maxPage || Math.abs(p - state.page) <= 1) {{
            pageButtons += `<button class="page-btn ${{p === state.page ? 'active' : ''}}" data-page="${{p}}">${{p}}</button>`;
        }} else if (Math.abs(p - state.page) === 2) {{
            pageButtons += `<span style="color:var(--text-dim);font-size:12px;padding:0 2px;">&hellip;</span>`;
        }}
    }}

    function sortArrow(key) {{
        if (state.sortKey !== key) return `<span style="opacity:.3"> &#8597;</span>`;
        return state.sortDir === "asc" ? " &#9650;" : " &#9660;";
    }}

    /* histogram */
    let chartHtml = "";
    const chartPrices = arr.map(i => i.price).filter(p => p != null);
    if (chartPrices.length) {{
        const min = Math.min(...chartPrices), max = Math.max(...chartPrices);
        const binCount = 16;
        const binSize = (max - min) / binCount || 1;
        const bins = new Array(binCount).fill(0);
        chartPrices.forEach(p => {{
            let idx = Math.floor((p - min) / binSize);
            if (idx >= binCount) idx = binCount - 1;
            if (idx < 0) idx = 0;
            bins[idx]++;
        }});
        const maxCount = Math.max(...bins);
        const bars = bins.map((count, idx) => {{
            const h = maxCount ? Math.max((count / maxCount) * 100, count > 0 ? 3 : 0) : 0;
            const rangeStart = (min + idx * binSize).toFixed(0);
            const opacity = 0.45 + (idx / (binCount - 1)) * 0.55;
            return `<div class="bar-col"><div class="bar" style="height:${{h}}%;opacity:${{opacity.toFixed(2)}}" data-tooltip="£${{rangeStart}} (${{count}})"></div></div>`;
        }}).join("");
        chartHtml = `
        <div class="chart-section">
            <h3>${{T.price_distribution}}</h3>
            <div class="bars">${{bars}}</div>
            <div class="bar-axis">
                <span>£${{min.toFixed(0)}}</span>
                <span>£${{max.toFixed(0)}}</span>
            </div>
        </div>`;
    }}

    document.getElementById("panel-overview").innerHTML = `
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">${{T.total_items}}</div>
                <div class="stat-value">${{ITEMS.length}}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">${{T.avg_price}}</div>
                <div class="stat-value accent">${{avg !== null ? fmtPrice(avg) : "-"}}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">${{T.last_scraped}}</div>
                <div class="stat-value" style="font-size:15px;font-weight:700;">${{lastScraped.replace("T", " ").slice(0, 16)}}</div>
            </div>
        </div>
        <div class="controls">
            <div class="control-group">
                <label>${{T.filter_category}}</label>
                <select class="control-select" id="categorySelect">${{catOptions}}</select>
            </div>
            <div class="control-group">
                <label>${{T.search_placeholder}}</label>
                <div class="search-wrap">
                    ${{ICON_SEARCH_SVG}}
                    <input class="control-input" id="searchInput" type="text"
                           placeholder="${{T.search_placeholder}}" value="${{state.search}}">
                </div>
            </div>
        </div>
        <div class="table-wrap">
            <table>
                <thead><tr>
                    <th data-key="title">${{T.table_title}}${{sortArrow('title')}}</th>
                    <th data-key="price">${{T.table_price}}${{sortArrow('price')}}</th>
                    <th data-key="availability">${{T.table_availability}}${{sortArrow('availability')}}</th>
                    <th data-key="scraped_at">${{T.table_scraped_at}}${{sortArrow('scraped_at')}}</th>
                </tr></thead>
                <tbody>${{rows}}</tbody>
            </table>
            <div class="pagination">${{pageButtons}}</div>
        </div>
        ${{chartHtml}}
    `;

    document.getElementById("categorySelect").addEventListener("change", e => {{
        state.category = e.target.value; state.page = 1; renderOverview();
    }});
    const si = document.getElementById("searchInput");
    si.addEventListener("input", e => {{ state.search = e.target.value; state.page = 1; renderOverview(); }});
    si.focus(); si.setSelectionRange(si.value.length, si.value.length);

    document.querySelectorAll("#panel-overview thead th[data-key]").forEach(th => {{
        th.addEventListener("click", () => {{
            const key = th.getAttribute("data-key");
            if (state.sortKey === key) state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
            else {{ state.sortKey = key; state.sortDir = "asc"; }}
            renderOverview();
        }});
    }});
    document.querySelectorAll("#panel-overview .page-btn").forEach(btn => {{
        btn.addEventListener("click", () => {{
            state.page = parseInt(btn.getAttribute("data-page"), 10);
            renderOverview();
        }});
    }});
    resizeFrame();
}}

/* ── line chart builder ── */
function buildLineChart(points) {{
    const width = 760, height = 240, pad = 36;
    const prices = points.map(p => p.price);
    const min = Math.min(...prices), max = Math.max(...prices);
    const range = (max - min) || 1;
    const stepX = (width - pad * 2) / Math.max(1, points.length - 1);
    const coords = points.map((p, i) => ({{
        x: pad + i * stepX,
        y: height - pad - ((p.price - min) / range) * (height - pad * 2),
        price: p.price,
        date: p.scraped_at,
    }}));
    const pathD = coords.map((pt, i) => (i === 0 ? "M" : "L") + pt.x.toFixed(1) + "," + pt.y.toFixed(1)).join(" ");
    const areaD = pathD
        + ` L${{coords[coords.length-1].x.toFixed(1)}},${{height-pad}}`
        + ` L${{coords[0].x.toFixed(1)}},${{height-pad}} Z`;
    const dots = coords.map(pt => `
        <circle cx="${{pt.x.toFixed(1)}}" cy="${{pt.y.toFixed(1)}}" r="5"
                fill="var(--accent)" stroke="var(--surface)" stroke-width="2.5"
                style="cursor:pointer;filter:drop-shadow(0 0 6px var(--accent-glow));">
            <title>${{fmtPrice(pt.price)}} — ${{pt.date.replace("T"," ").slice(0,16)}}</title>
        </circle>`).join("");
    return `
    <svg viewBox="0 0 ${{width}} ${{height}}" style="width:100%;height:auto;overflow:visible;">
        <defs>
            <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   stop-color="var(--accent)" stop-opacity="0.22"/>
                <stop offset="75%"  stop-color="var(--accent)" stop-opacity="0.04"/>
                <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
            </linearGradient>
            <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stop-color="var(--accent)"/>
                <stop offset="100%" stop-color="var(--accent2)"/>
            </linearGradient>
        </defs>
        <path d="${{areaD}}" fill="url(#areaFill)" stroke="none"/>
        <path d="${{pathD}}" fill="none" stroke="url(#lineGrad)"
              stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        ${{dots}}
    </svg>`;
}}

/* ── history panel ── */
function renderHistory() {{
    const titles = Object.keys(HISTORY).sort();
    if (!state.historyTitle && titles.length) state.historyTitle = titles[0];

    if (!titles.length) {{
        document.getElementById("panel-history").innerHTML =
            `<div class="empty-state">${{T.no_data_title}}</div>`;
        return;
    }}

    const optionsHtml = titles.map(t =>
        `<option value="${{t}}" ${{t === state.historyTitle ? "selected" : ""}}>${{t}}</option>`
    ).join("");

    const points = HISTORY[state.historyTitle] || [];
    const chartHtml = points.length < 2
        ? `<div class="empty-state">${{T.no_history}}</div>`
        : `<div class="chart-card"><h3>${{T.history_chart_title}}</h3>${{buildLineChart(points)}}</div>`;

    document.getElementById("panel-history").innerHTML = `
        <div class="control-group history-select">
            <label>${{T.select_item_history}}</label>
            <select class="control-select" id="historyTitleSelect">${{optionsHtml}}</select>
        </div>
        ${{chartHtml}}`;

    document.getElementById("historyTitleSelect").addEventListener("change", e => {{
        state.historyTitle = e.target.value; renderHistory();
    }});
    resizeFrame();
}}

/* ── about panel ── */
function renderAbout() {{
    document.getElementById("panel-about").innerHTML = `
        <div class="about-text">${{T.about_text}}</div>
        <div class="about-chips">
            <span class="about-chip">Python</span>
            <span class="about-chip">Streamlit</span>
            <span class="about-chip">SQLite</span>
            <span class="about-chip">BeautifulSoup</span>
            <span class="about-chip">Docker</span>
        </div>`;
}}

/* ── frame resize ── */
function resizeFrame() {{
    const height = document.body.scrollHeight + 20;
    if (window.parent) {{
        window.parent.postMessage({{ type: "streamlit:setFrameHeight", height }}, "*");
    }}
}}

/* ── init ── */
renderStaticLabels();
applyTheme();
renderOverview();
renderHistory();
renderAbout();
window.addEventListener("resize", resizeFrame);
</script>
</body>
</html>
"""

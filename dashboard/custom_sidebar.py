"""
custom_sidebar.py
------------------
Custom HTML/CSS/JS sidebar: taalkeuze + een ECHTE werkende dark/light
toggle. De toggle zet een query-param (?theme=light/dark) via JS en
herlaadt de pagina; app.py leest die param uit bij elke load en geeft
het gekozen thema door aan alle custom componenten.

Custom HTML/CSS/JS sidebar: language choice + a REAL working dark/light
toggle. The toggle sets a query param (?theme=light/dark) via JS and
reloads the page; app.py reads that param on every load and passes the
chosen theme to all custom components.
"""

import json


def render_sidebar_html(
    languages: dict,
    current_lang: str,
    current_mode: str,
    translations: dict,
) -> str:
    t = translations
    languages_json = json.dumps(languages, ensure_ascii=False)

    if current_mode == "dark":
        c = {
            "surface": "#17140F", "surface2": "#1D1812", "border": "#2C2419",
            "text": "#F5F0E8", "text_muted": "#9C8E78", "accent": "#E8B04B",
        }
    else:
        c = {
            "surface": "#FFFFFF", "surface2": "#FFFCF5", "border": "#E6DBC2",
            "text": "#2A2520", "text_muted": "#8A7A60", "accent": "#C8923A",
        }

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Inter', sans-serif; color: {c['text']}; background: transparent; }}

.section {{ margin-bottom: 22px; }}

.section-label {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {c['text_muted']};
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

select {{
    width: 100%;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 10px 14px;
    color: {c['text']};
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    outline: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='{c['text_muted'].replace('#','%23')}' d='M1 1l5 5 5-5'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 14px center;
    padding-right: 32px;
}}

select:focus {{
    border-color: {c['accent']};
    box-shadow: 0 0 0 3px {c['accent']}22;
}}

/* ---- Thema toggle: segmented control ---- */
.theme-toggle {{
    display: flex;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}}

.theme-option {{
    flex: 1;
    text-align: center;
    padding: 9px 0;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    color: {c['text_muted']};
    user-select: none;
    text-decoration: none;
    display: block;
}}

.theme-option.active {{
    background: {c['accent']};
    color: {"#1A1408" if current_mode == "dark" else "#FFFFFF"};
    box-shadow: 0 2px 8px {c['accent']}50;
}}

.theme-option:not(.active):hover {{
    color: {c['text']};
}}

.refresh-btn {{
    width: 100%;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 10px;
    color: {c['text']};
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
    text-decoration: none;
    display: block;
    text-align: center;
    box-sizing: border-box;
}}

.refresh-btn:hover {{
    border-color: {c['accent']};
    color: {c['accent']};
}}

hr {{
    border: none;
    border-top: 1px solid {c['border']};
    margin: 20px 0;
}}
</style>
</head>
<body>
<div class="section">
    <div class="section-label">🌐 <span>Taal / Language / اللغة</span></div>
    <select id="langSelect">
        {"".join(f'<option value="{code}" {"selected" if code == current_lang else ""}>{label}</option>' for code, label in languages.items())}
    </select>
</div>

<hr>

<div class="section">
    <div class="section-label">🎨 <span>Thema</span></div>
    <div class="theme-toggle">
        <a class="theme-option {'active' if current_mode == 'dark' else ''}" id="darkOption" href="?theme=dark&lang={current_lang}" target="_parent">🌙 Dark</a>
        <a class="theme-option {'active' if current_mode == 'light' else ''}" id="lightOption" href="?theme=light&lang={current_lang}" target="_parent">☀️ Light</a>
    </div>
</div>

<hr>

<a class="refresh-btn" id="refreshBtn" href="?theme={current_mode}&lang={current_lang}" target="_parent">🔄 Vernieuwen</a>

<script>
function setQueryParam(key, value) {{
    try {{
        const url = new URL(window.parent.location.href);
        url.searchParams.set(key, value);
        window.parent.location.href = url.toString();
    }} catch (e) {{
        // Cross-origin iframe kan window.parent.location niet altijd lezen/schrijven;
        // de <a target="_parent"> links hierboven zijn de betrouwbare fallback.
    }}
}}

document.getElementById("langSelect").addEventListener("change", e => {{
    const newLang = e.target.value;
    const newHref = "?theme={current_mode}&lang=" + newLang;
    try {{
        window.top.location.href = newHref;
    }} catch (err) {{
        try {{
            window.parent.location.href = newHref;
        }} catch (err2) {{
            // Laatste redmiddel: open in dezelfde tab via een tijdelijke link
            const a = document.createElement("a");
            a.href = newHref;
            a.target = "_parent";
            a.click();
        }}
    }}
}});

function resizeFrame() {{
    const height = document.body.scrollHeight + 20;
    if (window.parent) {{
        window.parent.postMessage({{ type: "streamlit:setFrameHeight", height: height }}, "*");
    }}
}}
resizeFrame();
</script>
</body>
</html>
"""
    return html

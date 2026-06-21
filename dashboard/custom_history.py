"""
custom_history.py
------------------
Bouwt de prijsgeschiedenis-tab als custom HTML/CSS/JS component:
een dropdown om een boek te kiezen + een zelfgetekende SVG-lijngrafiek.
"""

import json


def render_history_html(
    titles: list[str],
    history_by_title: dict,
    translations: dict,
    mode: str,
    rtl: bool,
) -> str:
    t = translations
    titles_json = json.dumps(titles, ensure_ascii=False)
    history_json = json.dumps(history_by_title, ensure_ascii=False)
    t_json = json.dumps(t, ensure_ascii=False)
    direction = "rtl" if rtl else "ltr"

    if mode == "dark":
        c = {
            "surface": "#17140F",
            "surface2": "#1D1812",
            "border": "#2C2419",
            "text": "#F5F0E8",
            "text_muted": "#9C8E78",
            "accent": "#E8B04B",
        }
    else:
        c = {
            "surface": "#FFFFFF",
            "surface2": "#FFFCF5",
            "border": "#E6DBC2",
            "text": "#2A2520",
            "text_muted": "#8A7A60",
            "accent": "#C8923A",
        }

    html = f"""
<!DOCTYPE html>
<html dir="{direction}">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Inter', sans-serif; color: {c['text']}; background: transparent; }}
.wrap {{ direction: {direction}; }}

.control-group label {{
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: {c['text_muted']};
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

select {{
    width: 100%;
    max-width: 420px;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 10px 14px;
    color: {c['text']};
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    outline: none;
    margin-bottom: 24px;
}}

select:focus {{
    border-color: {c['accent']};
    box-shadow: 0 0 0 3px {c['accent']}22;
}}

.chart-card {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 16px;
    padding: 20px;
}}

.chart-card h3 {{
    font-family: 'Fraunces', serif;
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
}}

.empty-state {{
    text-align: center;
    color: {c['text_muted']};
    padding: 50px 20px;
}}

.tooltip-dot {{
    transition: r 0.15s ease;
    cursor: pointer;
}}

.tooltip-dot:hover {{
    r: 7;
}}
</style>
</head>
<body>
<div class="wrap" id="root"></div>
<script>
const TITLES = {titles_json};
const HISTORY = {history_json};
const T = {t_json};

let selectedTitle = TITLES.length ? TITLES[0] : null;

function fmtPrice(p) {{
    return "£" + Number(p).toFixed(2);
}}

function buildLineChart(points) {{
    const width = 760, height = 260, padding = 40;
    const prices = points.map(p => p.price);
    const min = Math.min(...prices), max = Math.max(...prices);
    const range = (max - min) || 1;

    const stepX = (width - padding * 2) / Math.max(1, points.length - 1);
    const coords = points.map((p, idx) => {{
        const x = padding + idx * stepX;
        const y = height - padding - ((p.price - min) / range) * (height - padding * 2);
        return {{ x, y, price: p.price, date: p.scraped_at }};
    }});

    const pathD = coords.map((pt, idx) => (idx === 0 ? "M" : "L") + pt.x.toFixed(1) + "," + pt.y.toFixed(1)).join(" ");
    const areaD = pathD + ` L${{coords[coords.length-1].x.toFixed(1)}},${{height-padding}} L${{coords[0].x.toFixed(1)}},${{height-padding}} Z`;

    const dots = coords.map(pt => `
        <circle class="tooltip-dot" cx="${{pt.x.toFixed(1)}}" cy="${{pt.y.toFixed(1)}}" r="5" fill="{c['accent']}">
            <title>${{fmtPrice(pt.price)}} — ${{pt.date.replace('T',' ').slice(0,16)}}</title>
        </circle>
    `).join("");

    return `
    <svg viewBox="0 0 ${{width}} ${{height}}" style="width:100%; height:auto;">
        <defs>
            <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{c['accent']}" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="{c['accent']}" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="${{areaD}}" fill="url(#areaFill)" stroke="none"/>
        <path d="${{pathD}}" fill="none" stroke="{c['accent']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        ${{dots}}
    </svg>`;
}}

function render() {{
    const root = document.getElementById("root");
    if (!TITLES.length) {{
        root.innerHTML = `<div class="empty-state">${{T.no_data_title}}</div>`;
        return;
    }}

    const optionsHtml = TITLES.map(title =>
        `<option value="${{title}}" ${{title === selectedTitle ? "selected" : ""}}>${{title}}</option>`
    ).join("");

    const points = HISTORY[selectedTitle] || [];

    let chartHtml;
    if (points.length < 2) {{
        chartHtml = `<div class="empty-state">${{T.no_history}}</div>`;
    }} else {{
        chartHtml = `<div class="chart-card"><h3>${{T.history_chart_title}}</h3>${{buildLineChart(points)}}</div>`;
    }}

    root.innerHTML = `
        <div class="control-group">
            <label>${{T.select_item_history}}</label>
            <select id="titleSelect">${{optionsHtml}}</select>
        </div>
        ${{chartHtml}}
    `;

    document.getElementById("titleSelect").addEventListener("change", e => {{
        selectedTitle = e.target.value;
        render();
    }});

    resizeFrame();
}}

function resizeFrame() {{
    const height = document.getElementById("root").scrollHeight + 20;
    if (window.parent) {{
        window.parent.postMessage({{ type: "streamlit:setFrameHeight", height: height }}, "*");
    }}
}}

render();
</script>
</body>
</html>
"""
    return html

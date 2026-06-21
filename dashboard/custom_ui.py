"""
custom_ui.py
------------
Bouwt de volledige dashboard-content (metric cards, filters, tabel, chart)
als één HTML/CSS/JS-component, gerenderd in een iframe via
st.components.v1.html. Dit geeft volledige controle over de styling,
in tegenstelling tot Streamlit's eigen widgets/dataframe die hun eigen
rendering-engine gebruiken en niet via CSS overschreven kunnen worden.

Builds the full dashboard content (metric cards, filters, table, chart)
as one HTML/CSS/JS component, rendered in an iframe via
st.components.v1.html. This gives full styling control, unlike
Streamlit's own widgets/dataframe which use their own rendering engine.
"""

import json


def render_dashboard_html(
    items: list[dict],
    history_by_title: dict,
    translations: dict,
    mode: str,
    rtl: bool,
) -> str:
    """
    Genereert de volledige HTML/CSS/JS voor het dashboard.

    items: lijst van dicts met keys title, price, category, availability, scraped_at
    history_by_title: dict van title -> lijst van {price, scraped_at} voor de prijsgeschiedenis-tab
    translations: het vertaal-dict (t) voor de huidige taal
    mode: 'dark' of 'light'
    rtl: True als de taal rechts-naar-links is
    """
    t = translations
    data_json = json.dumps(items, ensure_ascii=False)
    history_json = json.dumps(history_by_title, ensure_ascii=False)
    t_json = json.dumps(t, ensure_ascii=False)
    direction = "rtl" if rtl else "ltr"

    # --- Kleurtokens per modus ---
    if mode == "dark":
        c = {
            "bg": "#0B0A08",
            "bg2": "#0F0E0C",
            "surface": "#17140F",
            "surface2": "#1D1812",
            "border": "#2C2419",
            "text": "#F5F0E8",
            "text_muted": "#9C8E78",
            "accent": "#E8B04B",
            "accent2": "#D99B2B",
            "shadow": "rgba(0,0,0,0.4)",
        }
    else:
        c = {
            "bg": "#F7F2E7",
            "bg2": "#FAF6EE",
            "surface": "#FFFFFF",
            "surface2": "#FFFCF5",
            "border": "#E6DBC2",
            "text": "#2A2520",
            "text_muted": "#8A7A60",
            "accent": "#C8923A",
            "accent2": "#B07B26",
            "shadow": "rgba(120,100,60,0.12)",
        }

    html = f"""
<!DOCTYPE html>
<html dir="{direction}">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    font-family: 'Inter', -apple-system, sans-serif;
    background: transparent;
    color: {c['text']};
}}

.dash {{
    direction: {direction};
}}

/* ===== Stat cards ===== */
.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}}

.stat-card {{
    background: linear-gradient(155deg, {c['surface2']} 0%, {c['surface']} 100%);
    border: 1px solid {c['border']};
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}}

.stat-card::before {{
    content: "";
    position: absolute;
    top: -40%;
    {"left" if rtl else "right"}: -20%;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, {c['accent']}30 0%, transparent 70%);
    pointer-events: none;
}}

.stat-card:hover {{
    transform: translateY(-3px);
    border-color: {c['accent']}80;
    box-shadow: 0 12px 28px {c['shadow']}, 0 0 0 1px {c['accent']}25;
}}

.stat-label {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {c['text_muted']};
    margin-bottom: 8px;
}}

.stat-value {{
    font-family: 'Fraunces', serif;
    font-size: 30px;
    font-weight: 600;
    color: {c['text']};
    line-height: 1.1;
}}

.stat-value.accent {{
    color: {c['accent']};
}}

/* ===== Controls (filter + search) ===== */
.controls {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 20px;
}}

@media (max-width: 600px) {{
    .controls {{ grid-template-columns: 1fr; }}
}}

.control-group label {{
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: {c['text_muted']};
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.control-input, .control-select {{
    width: 100%;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 10px 14px;
    color: {c['text']};
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    appearance: none;
}}

.control-select {{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='{c['text_muted'].replace('#','%23')}' d='M1 1l5 5 5-5'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: {"left 14px center" if rtl else "right 14px center"};
    padding-{"left" if rtl else "right"}: 32px;
}}

.control-input:focus, .control-select:focus {{
    border-color: {c['accent']};
    box-shadow: 0 0 0 3px {c['accent']}22;
}}

.control-input::placeholder {{
    color: {c['text_muted']};
}}

/* ===== Table ===== */
.table-wrap {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 28px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}}

thead th {{
    text-align: {"right" if rtl else "left"};
    padding: 14px 18px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {c['text_muted']};
    background: {c['surface2']};
    border-bottom: 1px solid {c['border']};
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
}}

thead th:hover {{
    color: {c['accent']};
}}

thead th .sort-arrow {{
    opacity: 0.5;
    font-size: 10px;
    margin-{"right" if rtl else "left"}: 4px;
}}

tbody td {{
    padding: 13px 18px;
    border-bottom: 1px solid {c['border']};
    color: {c['text']};
    text-align: {"right" if rtl else "left"};
}}

tbody td.num {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    color: {c['accent']};
}}

tbody tr {{
    transition: background 0.15s ease;
}}

tbody tr:hover {{
    background: {c['surface2']};
}}

tbody tr:last-child td {{
    border-bottom: none;
}}

.badge {{
    display: inline-block;
    font-size: 12px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    background: {c['accent']}1A;
    color: {c['accent2']};
}}

.empty-row td {{
    text-align: center;
    color: {c['text_muted']};
    padding: 40px;
}}

/* ===== Pagination ===== */
.pagination {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 14px;
    border-top: 1px solid {c['border']};
}}

.page-btn {{
    background: transparent;
    border: 1px solid {c['border']};
    color: {c['text_muted']};
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s ease;
}}

.page-btn:hover {{
    border-color: {c['accent']};
    color: {c['accent']};
}}

.page-btn.active {{
    background: {c['accent']};
    border-color: {c['accent']};
    color: {c['bg']};
    font-weight: 600;
}}

.page-info {{
    font-size: 13px;
    color: {c['text_muted']};
    margin: 0 10px;
}}

/* ===== Chart ===== */
.chart-section h3 {{
    font-family: 'Fraunces', serif;
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 16px;
}}

.bars {{
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 180px;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 16px;
    padding: 20px 16px 8px;
}}

.bar {{
    flex: 1;
    background: linear-gradient(180deg, {c['accent']} 0%, {c['accent2']} 100%);
    border-radius: 4px 4px 0 0;
    min-height: 2px;
    position: relative;
    transition: opacity 0.2s ease;
}}

.bar:hover {{
    opacity: 0.75;
}}

.bar:hover::after {{
    content: attr(data-tooltip);
    position: absolute;
    bottom: 105%;
    left: 50%;
    transform: translateX(-50%);
    background: {c['text']};
    color: {c['bg']};
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 6px;
    white-space: nowrap;
    font-weight: 600;
}}

.bar-axis {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: {c['text_muted']};
    margin-top: 8px;
    padding: 0 16px;
}}
</style>
</head>
<body>
<div class="dash" id="dash"></div>

<script>
const ITEMS = {data_json};
const HISTORY = {history_json};
const T = {t_json};
const RTL = {str(rtl).lower()};

let state = {{
    category: "ALL",
    search: "",
    sortKey: "scraped_at",
    sortDir: "desc",
    page: 1,
    pageSize: 8,
}};

function fmtPrice(p) {{
    return (p === null || p === undefined) ? "-" : "£" + Number(p).toFixed(2);
}}

function getCategories() {{
    const cats = new Set(ITEMS.map(i => i.category).filter(Boolean));
    return Array.from(cats).sort();
}}

function filteredItems() {{
    let arr = ITEMS.slice();
    if (state.category !== "ALL") {{
        arr = arr.filter(i => i.category === state.category);
    }}
    if (state.search.trim()) {{
        const q = state.search.trim().toLowerCase();
        arr = arr.filter(i => i.title.toLowerCase().includes(q));
    }}
    arr.sort((a, b) => {{
        let av = a[state.sortKey], bv = b[state.sortKey];
        if (av === null || av === undefined) av = -Infinity;
        if (bv === null || bv === undefined) bv = -Infinity;
        if (typeof av === "string") {{
            return state.sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
        }}
        return state.sortDir === "asc" ? av - bv : bv - av;
    }});
    return arr;
}}

function computeStats(arr) {{
    const total = ITEMS.length;
    const prices = ITEMS.map(i => i.price).filter(p => p !== null && p !== undefined);
    const avg = prices.length ? prices.reduce((a, b) => a + b, 0) / prices.length : null;
    const lastScraped = ITEMS.reduce((max, i) => i.scraped_at > max ? i.scraped_at : max, "");
    return {{ total, avg, lastScraped }};
}}

function renderStats(stats) {{
    return `
    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">${{T.total_items}}</div>
            <div class="stat-value">${{stats.total}}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">${{T.avg_price}}</div>
            <div class="stat-value accent">${{stats.avg !== null ? fmtPrice(stats.avg) : "-"}}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">${{T.last_scraped}}</div>
            <div class="stat-value" style="font-size:20px;">${{stats.lastScraped.replace("T", " ").slice(0, 16)}}</div>
        </div>
    </div>`;
}}

function renderControls() {{
    const cats = getCategories();
    const options = `<option value="ALL">${{T.all_categories}}</option>` +
        cats.map(c => `<option value="${{c}}" ${{state.category === c ? "selected" : ""}}>${{c}}</option>`).join("");
    return `
    <div class="controls">
        <div class="control-group">
            <label>${{T.filter_category}}</label>
            <select class="control-select" id="categorySelect">${{options}}</select>
        </div>
        <div class="control-group">
            <label>${{T.search_placeholder}}</label>
            <input class="control-input" id="searchInput" type="text" placeholder="${{T.search_placeholder}}" value="${{state.search}}">
        </div>
    </div>`;
}}

function sortArrow(key) {{
    if (state.sortKey !== key) return "";
    return `<span class="sort-arrow">${{state.sortDir === "asc" ? "&#9650;" : "&#9660;"}}</span>`;
}}

function renderTable(arr) {{
    const start = (state.page - 1) * state.pageSize;
    const pageItems = arr.slice(start, start + state.pageSize);
    const totalPages = Math.max(1, Math.ceil(arr.length / state.pageSize));

    const rows = pageItems.length ? pageItems.map(i => `
        <tr>
            <td>${{i.title}}</td>
            <td class="num">${{fmtPrice(i.price)}}</td>
            <td><span class="badge">${{i.availability || "-"}}</span></td>
            <td>${{(i.scraped_at || "").replace("T", " ").slice(0, 19)}}</td>
        </tr>
    `).join("") : `<tr class="empty-row"><td colspan="4">${{T.no_data_title}}</td></tr>`;

    let pageButtons = "";
    for (let p = 1; p <= totalPages; p++) {{
        if (p === 1 || p === totalPages || Math.abs(p - state.page) <= 1) {{
            pageButtons += `<button class="page-btn ${{p === state.page ? 'active' : ''}}" data-page="${{p}}">${{p}}</button>`;
        }} else if (Math.abs(p - state.page) === 2) {{
            pageButtons += `<span class="page-info">…</span>`;
        }}
    }}

    return `
    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th data-key="title">${{T.table_title}}${{sortArrow('title')}}</th>
                    <th data-key="price">${{T.table_price}}${{sortArrow('price')}}</th>
                    <th data-key="availability">${{T.table_availability}}${{sortArrow('availability')}}</th>
                    <th data-key="scraped_at">${{T.table_scraped_at}}${{sortArrow('scraped_at')}}</th>
                </tr>
            </thead>
            <tbody>${{rows}}</tbody>
        </table>
        <div class="pagination">${{pageButtons}}</div>
    </div>`;
}}

function renderChart(arr) {{
    const prices = arr.map(i => i.price).filter(p => p !== null && p !== undefined);
    if (!prices.length) return "";

    const min = Math.min(...prices), max = Math.max(...prices);
    const binCount = 16;
    const binSize = (max - min) / binCount || 1;
    const bins = new Array(binCount).fill(0);
    prices.forEach(p => {{
        let idx = Math.floor((p - min) / binSize);
        if (idx >= binCount) idx = binCount - 1;
        if (idx < 0) idx = 0;
        bins[idx]++;
    }});
    const maxCount = Math.max(...bins);

    const bars = bins.map((count, idx) => {{
        const heightPct = maxCount ? (count / maxCount) * 100 : 0;
        const rangeStart = (min + idx * binSize).toFixed(0);
        return `<div class="bar" style="height:${{heightPct}}%" data-tooltip="£${{rangeStart}} (${{count}})"></div>`;
    }}).join("");

    return `
    <div class="chart-section">
        <h3>${{T.price_distribution}}</h3>
        <div class="bars">${{bars}}</div>
        <div class="bar-axis"><span>£${{min.toFixed(0)}}</span><span>£${{max.toFixed(0)}}</span></div>
    </div>`;
}}

function render() {{
    const arr = filteredItems();
    const stats = computeStats(arr);
    const maxPage = Math.max(1, Math.ceil(arr.length / state.pageSize));
    if (state.page > maxPage) state.page = maxPage;

    document.getElementById("dash").innerHTML =
        renderStats(stats) + renderControls() + renderTable(arr) + renderChart(arr);

    attachEvents();
    resizeFrame();
}}

function attachEvents() {{
    const catSelect = document.getElementById("categorySelect");
    if (catSelect) {{
        catSelect.addEventListener("change", e => {{
            state.category = e.target.value;
            state.page = 1;
            render();
        }});
    }}

    const searchInput = document.getElementById("searchInput");
    if (searchInput) {{
        searchInput.addEventListener("input", e => {{
            state.search = e.target.value;
            state.page = 1;
            render();
        }});
        // Cursor positie behouden na re-render
        searchInput.focus();
        const val = searchInput.value;
        searchInput.value = val;
    }}

    document.querySelectorAll("thead th[data-key]").forEach(th => {{
        th.addEventListener("click", () => {{
            const key = th.getAttribute("data-key");
            if (state.sortKey === key) {{
                state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
            }} else {{
                state.sortKey = key;
                state.sortDir = "asc";
            }}
            render();
        }});
    }});

    document.querySelectorAll(".page-btn").forEach(btn => {{
        btn.addEventListener("click", () => {{
            state.page = parseInt(btn.getAttribute("data-page"), 10);
            render();
        }});
    }});
}}

function resizeFrame() {{
    const height = document.getElementById("dash").scrollHeight + 20;
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

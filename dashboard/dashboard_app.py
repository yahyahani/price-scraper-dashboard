"""
dashboard_app.py
-----------------
Eén volledig zelfstandig HTML/CSS/JS dashboard (sidebar + content samen),
gerenderd als één component via st.components.v1.html.

Dark/light wisselt puur client-side door een CSS-class te togglen op
<body> (geen page reload, geen iframe-naar-parent navigatie, geen query
params voor het thema). Taal wisselt via een URL query-param omdat de
content per taal echt anders moet renderen (RTL voor Arabisch, en de
vertalingen zelf), wat een page-load vereist.

Alle drie talen (NL/EN/AR) staan tegelijk in de payload, zodat de
taalkeuze ook zonder reload zou kunnen - voor nu kiezen we een simpele
reload bij taalwissel omdat RTL een hele layout-richting omgooit.
"""

import json


ICON_MOON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
ICON_SUN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
ICON_REFRESH = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>'
ICON_SEARCH = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/></svg>'


def render_full_dashboard(
    items: list[dict],
    history_by_title: dict,
    translations: dict,
    languages: dict,
    current_lang: str,
    rtl: bool,
) -> str:
    """
    items: lijst van dicts (title, price, category, availability, scraped_at)
    history_by_title: dict van title -> lijst van {price, scraped_at}
    translations: het vertaal-dict (t) voor de huidige taal
    languages: dict van taalcode -> leesbare naam, bv. {'nl': 'Nederlands', ...}
    current_lang: de actieve taalcode, bv. 'nl'
    rtl: True als de huidige taal rechts-naar-links is
    """
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg: #0B0B0F;
    --surface: #16161D;
    --surface-2: #1E1E27;
    --border: #2A2A35;
    --text: #F0F0F3;
    --text-muted: #8E8E9A;
    --accent: #8B5CF6;
    --accent-hover: #A78BFA;
    --accent-soft: #8B5CF61F;
    --accent-on: #FFFFFF;
    --accent2: #F97362;
}}

body.light {{
    --bg: #FAFAFC;
    --surface: #FFFFFF;
    --surface-2: #F2F1F8;
    --border: #E4E1F0;
    --text: #18181F;
    --text-muted: #6C6C7A;
    --accent: #7C3AED;
    --accent-hover: #6D28D9;
    --accent-soft: #7C3AED14;
    --accent-on: #FFFFFF;
    --accent2: #EA580C;
}}

* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    transition: background 0.2s ease, color 0.2s ease;
}}

.layout {{
    display: grid;
    grid-template-columns: 240px 1fr;
    min-height: 100vh;
    direction: {direction};
}}

@media (max-width: 768px) {{
    .layout {{ grid-template-columns: 1fr; }}
    .sidebar {{ display: none; }}
}}

.sidebar {{
    background: var(--surface);
    border-{"left" if rtl else "right"}: 1px solid var(--border);
    padding: 24px 18px;
    display: flex;
    flex-direction: column;
    gap: 22px;
}}

.sidebar-section label {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}}

.sidebar select {{
    width: 100%;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px 12px;
    color: var(--text);
    font-size: 13px;
    font-family: 'Inter', sans-serif;
    outline: none;
    appearance: none;
    cursor: pointer;
}}

.sidebar select:focus {{ border-color: var(--accent); }}

.lang-buttons {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.lang-btn {{
    width: 100%;
    text-align: {"right" if rtl else "left"};
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 12px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    transition: all 0.15s ease;
    text-decoration: none;
    display: block;
    box-sizing: border-box;
}}

.lang-btn.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: var(--accent-on);
}}

.lang-btn:not(.active):hover {{
    border-color: var(--accent);
    color: var(--text);
}}

.seg-control {{
    display: flex;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 3px;
    gap: 3px;
}}

.seg-option {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 7px 0;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.15s ease;
    user-select: none;
    border: none;
    background: transparent;
    font-family: 'Inter', sans-serif;
}}

.seg-option.active {{
    background: var(--accent);
    color: var(--accent-on);
}}

.seg-option:not(.active):hover {{ color: var(--text); }}

.icon-btn {{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: 'Inter', sans-serif;
}}

.icon-btn:hover {{ border-color: var(--accent); color: var(--accent); }}

.main {{ padding: 36px 40px; max-width: 1180px; }}

h1.title {{ font-size: 26px; font-weight: 700; letter-spacing: -0.02em; margin: 0 0 4px 0; }}

.tabs {{
    display: flex;
    gap: 4px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
    margin-top: 20px;
}}

.tab {{
    padding: 9px 4px;
    margin-{"left" if rtl else "right"}: 20px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.15s ease;
}}

.tab.active {{ color: var(--text); border-bottom-color: var(--accent); }}
.tab:hover:not(.active) {{ color: var(--text); }}

.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; }}

.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
}}

.stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.15s ease, transform 0.15s ease;
}}

.stat-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.15s ease;
}}

.stat-card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
.stat-card:hover::before {{ opacity: 1; }}

.stat-label {{
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}}

.stat-value {{ font-size: 24px; font-weight: 700; letter-spacing: -0.01em; }}
.stat-value.accent {{ color: var(--accent); }}

.controls {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}}

@media (max-width: 600px) {{ .controls {{ grid-template-columns: 1fr; }} }}

.control-group label {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}}

.control-input, .control-select {{
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px 12px;
    color: var(--text);
    font-size: 13px;
    font-family: 'Inter', sans-serif;
    outline: none;
    appearance: none;
}}

.search-wrap {{ position: relative; }}
.search-wrap svg {{
    position: absolute;
    {"right" if rtl else "left"}: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    pointer-events: none;
}}
.search-wrap .control-input {{ padding-{"right" if rtl else "left"}: 34px; }}

.control-input:focus, .control-select:focus {{ border-color: var(--accent); }}
.control-input::placeholder {{ color: var(--text-muted); }}

.table-wrap {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 24px;
}}

table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}

thead th {{
    text-align: {"right" if rtl else "left"};
    padding: 11px 16px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    background: var(--surface-2);
    border-bottom: 1px solid var(--border);
    cursor: pointer;
    white-space: nowrap;
}}

thead th:hover {{ color: var(--accent); }}

tbody td {{
    padding: 11px 16px;
    border-bottom: 1px solid var(--border);
    text-align: {"right" if rtl else "left"};
}}

tbody td.num {{ font-weight: 600; color: var(--accent); }}
tbody tr:hover {{ background: var(--surface-2); }}
tbody tr:last-child td {{ border-bottom: none; }}

.badge {{
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 6px;
    background: var(--accent-soft);
    color: var(--accent);
}}

.empty-row td {{ text-align: center; color: var(--text-muted); padding: 36px; }}

.pagination {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 12px;
    border-top: 1px solid var(--border);
}}

.page-btn {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    cursor: pointer;
}}

.page-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
.page-btn.active {{ background: var(--accent); border-color: var(--accent); color: var(--accent-on); }}

.chart-section h3 {{ font-size: 15px; font-weight: 600; margin-bottom: 14px; }}

.bars {{
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
}}

.bar-col {{ flex: 1; height: 100%; display: flex; align-items: flex-end; }}

.bar {{
    width: 100%;
    background: linear-gradient(180deg, var(--accent-hover), var(--accent));
    border-radius: 3px 3px 0 0;
    min-height: 3px;
    position: relative;
}}

.bar:hover {{ background: linear-gradient(180deg, var(--accent2), var(--accent)); }}

.bar:hover::after {{
    content: attr(data-tooltip);
    position: absolute;
    bottom: 105%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--text);
    color: var(--bg);
    font-size: 10px;
    padding: 3px 7px;
    border-radius: 4px;
    white-space: nowrap;
    font-weight: 600;
}}

.bar-axis {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 8px;
}}

.history-select {{ max-width: 360px; margin-bottom: 20px; }}

.chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
}}

.chart-card h3 {{ font-size: 15px; font-weight: 600; margin: 0 0 14px 0; }}

.empty-state {{ text-align: center; color: var(--text-muted); padding: 40px 16px; font-size: 13px; }}

.about-text {{ font-size: 14px; line-height: 1.6; color: var(--text); max-width: 600px; }}
.about-links {{ margin-top: 12px; font-size: 13px; color: var(--text-muted); }}

::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 8px; }}
</style>
</head>
<body>

<div class="layout">
    <div class="sidebar">
        <div class="sidebar-section">
            <label>Language</label>
            <div class="lang-buttons" id="langButtons"></div>
        </div>
        <div class="sidebar-section">
            <label>Theme</label>
            <div class="seg-control">
                <button class="seg-option active" id="darkBtn" type="button">{ICON_MOON} Dark</button>
                <button class="seg-option" id="lightBtn" type="button">{ICON_SUN} Light</button>
            </div>
        </div>
        <button class="icon-btn" id="refreshBtn" type="button">{ICON_REFRESH} <span id="refreshLabel"></span></button>
    </div>

    <div class="main">
        <h1 class="title" id="appTitle"></h1>
        <div class="tabs">
            <div class="tab active" data-tab="overview" id="tabOverviewLabel"></div>
            <div class="tab" data-tab="history" id="tabHistoryLabel"></div>
            <div class="tab" data-tab="about" id="tabAboutLabel"></div>
        </div>

        <div class="tab-panel active" id="panel-overview"></div>
        <div class="tab-panel" id="panel-history"></div>
        <div class="tab-panel" id="panel-about"></div>
    </div>
</div>

<script>
const ITEMS = {data_json};
const HISTORY = {history_json};
const T = {t_json};
const LANGUAGES = {languages_json};
const CURRENT_LANG = "{current_lang}";
const RTL = {rtl_js};
const ICON_SEARCH_SVG = `{ICON_SEARCH}`;

let state = {{
    theme: "dark",
    category: "ALL",
    search: "",
    sortKey: "scraped_at",
    sortDir: "desc",
    page: 1,
    pageSize: 8,
    activeTab: "overview",
    historyTitle: null,
}};

function fmtPrice(p) {{
    return (p === null || p === undefined) ? "-" : "\u00a3" + Number(p).toFixed(2);
}}

function applyTheme() {{
    document.body.className = state.theme === "light" ? "light" : "";
    document.getElementById("darkBtn").classList.toggle("active", state.theme === "dark");
    document.getElementById("lightBtn").classList.toggle("active", state.theme === "light");
}}

document.getElementById("darkBtn").addEventListener("click", () => {{
    state.theme = "dark";
    applyTheme();
}});

document.getElementById("lightBtn").addEventListener("click", () => {{
    state.theme = "light";
    applyTheme();
}});

document.getElementById("refreshBtn").addEventListener("click", () => {{
    window.location.reload();
}});

function renderStaticLabels() {{
    document.getElementById("refreshLabel").textContent = T.refresh_button || "Refresh";
    document.getElementById("appTitle").textContent = T.app_title;
    document.getElementById("tabOverviewLabel").textContent = T.tab_overview;
    document.getElementById("tabHistoryLabel").textContent = T.tab_history;
    document.getElementById("tabAboutLabel").textContent = T.tab_about;

    // Huidige volledige URL van de buitenste pagina ophalen (niet die van
    // het iframe zelf) zodat we daar de lang-param op kunnen aanpassen.
    let outerHref;
    try {{
        outerHref = window.top.location.href;
    }} catch (e) {{
        outerHref = window.location.href;
    }}

    const langButtons = document.getElementById("langButtons");
    langButtons.innerHTML = Object.entries(LANGUAGES).map(([code, label]) => {{
        const url = new URL(outerHref);
        url.searchParams.set("lang", code);
        const isActive = code === CURRENT_LANG;
        return `<a class="lang-btn ${{isActive ? 'active' : ''}}" href="${{url.toString()}}" target="_top">${{label}}</a>`;
    }}).join("");
}}

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
        if (av === null || av === undefined) av = -Infinity;
        if (bv === null || bv === undefined) bv = -Infinity;
        if (typeof av === "string") return state.sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
        return state.sortDir === "asc" ? av - bv : bv - av;
    }});
    return arr;
}}

function renderOverview() {{
    const arr = filteredItems();
    const prices = ITEMS.map(i => i.price).filter(p => p !== null && p !== undefined);
    const avg = prices.length ? prices.reduce((a, b) => a + b, 0) / prices.length : null;
    const lastScraped = ITEMS.reduce((max, i) => i.scraped_at > max ? i.scraped_at : max, "");

    const cats = getCategories();
    const catOptions = `<option value="ALL">${{T.all_categories}}</option>` +
        cats.map(c => `<option value="${{c}}" ${{state.category === c ? "selected" : ""}}>${{c}}</option>`).join("");

    const maxPage = Math.max(1, Math.ceil(arr.length / state.pageSize));
    if (state.page > maxPage) state.page = maxPage;
    const start = (state.page - 1) * state.pageSize;
    const pageItems = arr.slice(start, start + state.pageSize);

    const rows = pageItems.length ? pageItems.map(i => `
        <tr>
            <td>${{i.title}}</td>
            <td class="num">${{fmtPrice(i.price)}}</td>
            <td><span class="badge">${{i.availability || "-"}}</span></td>
            <td>${{(i.scraped_at || "").replace("T", " ").slice(0, 19)}}</td>
        </tr>
    `).join("") : `<tr class="empty-row"><td colspan="4">${{T.no_data_title}}</td></tr>`;

    let pageButtons = "";
    for (let p = 1; p <= maxPage; p++) {{
        if (p === 1 || p === maxPage || Math.abs(p - state.page) <= 1) {{
            pageButtons += `<button class="page-btn ${{p === state.page ? 'active' : ''}}" data-page="${{p}}">${{p}}</button>`;
        }} else if (Math.abs(p - state.page) === 2) {{
            pageButtons += `<span style="color:var(--text-muted);font-size:12px;">&hellip;</span>`;
        }}
    }}

    function sortArrow(key) {{
        if (state.sortKey !== key) return "";
        return state.sortDir === "asc" ? " &#9650;" : " &#9660;";
    }}

    let chartHtml = "";
    const chartPrices = arr.map(i => i.price).filter(p => p !== null && p !== undefined);
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
            const h = maxCount ? Math.max((count / maxCount) * 100, count > 0 ? 4 : 0) : 0;
            const rangeStart = (min + idx * binSize).toFixed(0);
            return `<div class="bar-col"><div class="bar" style="height:${{h}}%" data-tooltip="\u00a3${{rangeStart}} (${{count}})"></div></div>`;
        }}).join("");
        chartHtml = `
        <div class="chart-section">
            <h3>${{T.price_distribution}}</h3>
            <div class="bars">${{bars}}</div>
            <div class="bar-axis"><span>\u00a3${{min.toFixed(0)}}</span><span>\u00a3${{max.toFixed(0)}}</span></div>
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
                <div class="stat-value" style="font-size:16px;">${{lastScraped.replace("T", " ").slice(0, 16)}}</div>
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
                    <input class="control-input" id="searchInput" type="text" placeholder="${{T.search_placeholder}}" value="${{state.search}}">
                </div>
            </div>
        </div>
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
        </div>
        ${{chartHtml}}
    `;

    document.getElementById("categorySelect").addEventListener("change", e => {{
        state.category = e.target.value; state.page = 1; renderOverview();
    }});
    const searchInput = document.getElementById("searchInput");
    searchInput.addEventListener("input", e => {{
        state.search = e.target.value; state.page = 1; renderOverview();
    }});
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

function buildLineChart(points) {{
    const width = 760, height = 240, padding = 36;
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
        <circle cx="${{pt.x.toFixed(1)}}" cy="${{pt.y.toFixed(1)}}" r="4" fill="var(--accent)" style="cursor:pointer;">
            <title>${{fmtPrice(pt.price)}} \u2014 ${{pt.date.replace('T',' ').slice(0,16)}}</title>
        </circle>
    `).join("");
    return `
    <svg viewBox="0 0 ${{width}} ${{height}}" style="width:100%; height:auto;">
        <defs>
            <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.18"/>
                <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
            </linearGradient>
        </defs>
        <path d="${{areaD}}" fill="url(#areaFill)" stroke="none"/>
        <path d="${{pathD}}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        ${{dots}}
    </svg>`;
}}

function renderHistory() {{
    const titles = Object.keys(HISTORY).sort();
    if (!state.historyTitle && titles.length) state.historyTitle = titles[0];

    if (!titles.length) {{
        document.getElementById("panel-history").innerHTML = `<div class="empty-state">${{T.no_data_title}}</div>`;
        return;
    }}

    const optionsHtml = titles.map(title =>
        `<option value="${{title}}" ${{title === state.historyTitle ? "selected" : ""}}>${{title}}</option>`
    ).join("");

    const points = HISTORY[state.historyTitle] || [];
    let chartHtml;
    if (points.length < 2) {{
        chartHtml = `<div class="empty-state">${{T.no_history}}</div>`;
    }} else {{
        chartHtml = `<div class="chart-card"><h3>${{T.history_chart_title}}</h3>${{buildLineChart(points)}}</div>`;
    }}

    document.getElementById("panel-history").innerHTML = `
        <div class="control-group history-select">
            <label>${{T.select_item_history}}</label>
            <select class="control-select" id="historyTitleSelect">${{optionsHtml}}</select>
        </div>
        ${{chartHtml}}
    `;

    document.getElementById("historyTitleSelect").addEventListener("change", e => {{
        state.historyTitle = e.target.value;
        renderHistory();
    }});
    resizeFrame();
}}

function renderAbout() {{
    document.getElementById("panel-about").innerHTML = `
        <div class="about-text">${{T.about_text}}</div>
        <div class="about-links">Python &middot; Streamlit &middot; SQLite &middot; BeautifulSoup &middot; Docker</div>
    `;
}}

function resizeFrame() {{
    const height = document.body.scrollHeight + 20;
    if (window.parent) {{
        window.parent.postMessage({{ type: "streamlit:setFrameHeight", height: height }}, "*");
    }}
}}

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

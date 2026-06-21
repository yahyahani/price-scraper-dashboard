#!/bin/sh
# docker-entrypoint.sh
# --------------------
# Draait bij het opstarten van de container:
# 1. Scrape data als de database nog leeg/niet aanwezig is
# 2. Start het Streamlit dashboard

set -e

if [ ! -f "data/scraper.db" ]; then
    echo "Geen database gevonden, eerste keer scrapen..."
    python main.py --pages 5 || echo "Scraper kon niet verbinden (geen internet in container?) - dashboard start met lege data."
fi

echo "Dashboard starten op http://localhost:8501 ..."
exec streamlit run dashboard/app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.headless=true \
    --browser.gatherUsageStats=false

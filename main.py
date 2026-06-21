"""
main.py
-------
Entry point: runt de scraper en slaat de resultaten op in de database.

Entry point: runs the scraper and saves results to the database.

نقطة الدخول: تشغيل أداة السحب وحفظ النتائج في قاعدة البيانات.

Gebruik / Usage / الاستخدام:
    python main.py                 # eenmalig scrapen
    python main.py --schedule      # elke X uur automatisch scrapen
"""

import argparse
import time

import schedule

from scraper.database import init_db, insert_items
from scraper.scraper import scrape_all


def run_once(max_pages: int = 5) -> None:
    """Voert één scrape-cyclus uit en slaat de data op."""
    print("Scraper gestart...")
    init_db()
    items = scrape_all(max_pages=max_pages)
    saved = insert_items(items)
    print(f"Klaar! {len(items)} items gescraped, {saved} rijen opgeslagen in de database.")


def run_scheduled(interval_hours: int = 6, max_pages: int = 5) -> None:
    """Runt de scraper continu, elke `interval_hours` uur."""
    print(f"Scheduler gestart: elke {interval_hours} uur. Druk Ctrl+C om te stoppen.")
    run_once(max_pages=max_pages)  # direct een eerste keer runnen
    schedule.every(interval_hours).hours.do(run_once, max_pages=max_pages)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Price Scraper Dashboard - data collector")
    parser.add_argument("--schedule", action="store_true", help="Blijf draaien en scrape periodiek")
    parser.add_argument("--interval", type=int, default=6, help="Uren tussen scrapes (met --schedule)")
    parser.add_argument("--pages", type=int, default=5, help="Maximum aantal pagina's per scrape")
    args = parser.parse_args()

    if args.schedule:
        run_scheduled(interval_hours=args.interval, max_pages=args.pages)
    else:
        run_once(max_pages=args.pages)

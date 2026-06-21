"""
scraper.py
----------
Scraper voor books.toscrape.com - een speciale website gemaakt voor
het oefenen van web scraping (100% legaal, geen rate-limits, geen API-key nodig).

Scraper for books.toscrape.com - a sandbox website specifically built for
practicing web scraping (100% legal, no rate limits, no API key needed).

أداة سحب بيانات لموقع books.toscrape.com - وهو موقع مخصص للتدريب على
سحب البيانات بشكل قانوني تمامًا، بدون حاجة لمفتاح API.

Hoe later uitbreiden / how to extend later:
    Maak een nieuw bestand (bv. jobs_scraper.py) met dezelfde structuur:
    een functie die een lijst van dicts teruggeeft met de keys die
    database.py verwacht: source, category, title, price, availability, url.
    Voeg die functie dan toe aan main.py.
"""

import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
SOURCE_NAME = "books.toscrape.com"

# Een nette User-Agent zetten is goede scraping-etiquette
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraperBot/1.0; +https://github.com)"
}


def _parse_price(price_text: str) -> float | None:
    """Zet een prijsstring zoals '£51.77' om naar een float (51.77)."""
    cleaned = price_text.strip().lstrip("£$€").replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def scrape_page(url: str) -> tuple[list[dict], str | None]:
    """
    Scraapt één pagina met boeken.
    Retourneert (lijst van items, url van de volgende pagina of None).
    """
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    for book in soup.select("article.product_pod"):
        title_tag = book.select_one("h3 a")
        price_tag = book.select_one(".price_color")
        availability_tag = book.select_one(".availability")

        title = title_tag["title"] if title_tag else "Onbekend"
        price = _parse_price(price_tag.text) if price_tag else None
        availability = availability_tag.text.strip() if availability_tag else None
        relative_link = title_tag["href"] if title_tag else ""
        full_url = requests.compat.urljoin(url, relative_link)

        items.append(
            {
                "source": SOURCE_NAME,
                "category": "Books",
                "title": title,
                "price": price,
                "currency": "GBP",
                "availability": availability,
                "url": full_url,
            }
        )

    # Zoek de "next" link voor paginatie
    next_tag = soup.select_one("li.next a")
    next_url = requests.compat.urljoin(url, next_tag["href"]) if next_tag else None

    return items, next_url


def scrape_all(max_pages: int = 5, delay_seconds: float = 1.0) -> list[dict]:
    """
    Scraapt meerdere pagina's (standaard max 5, om de oefen-server niet te belasten).
    delay_seconds = wachttijd tussen requests (beleefde scraping-etiquette).
    """
    all_items = []
    url = BASE_URL
    page_count = 0

    while url and page_count < max_pages:
        print(f"Scraping: {url}")
        items, next_url = scrape_page(url)
        all_items.extend(items)
        url = next_url
        page_count += 1
        if url:
            time.sleep(delay_seconds)

    return all_items


if __name__ == "__main__":
    results = scrape_all(max_pages=2)
    print(f"\n{len(results)} boeken gevonden.")
    for r in results[:5]:
        print(r)

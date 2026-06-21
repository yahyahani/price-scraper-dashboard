"""
database.py
-----------
Beheert de SQLite database: tabellen aanmaken, data opslaan en ophalen.

Manages the SQLite database: creating tables, saving and retrieving data.

يدير قاعدة بيانات SQLite: إنشاء الجداول، حفظ واسترجاع البيانات.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# Pad naar de database file (in de data/ map naast dit project)
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "scraper.db"


def get_connection() -> sqlite3.Connection:
    """Opent een connectie met de database (maakt de map aan als die nog niet bestaat)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Maakt de benodigde tabel aan als die nog niet bestaat."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,          -- bv. 'books.toscrape.com'
            category TEXT,                 -- bv. 'Fiction'
            title TEXT NOT NULL,
            price REAL,
            currency TEXT DEFAULT 'GBP',
            availability TEXT,
            url TEXT,
            scraped_at TEXT NOT NULL        -- ISO timestamp
        )
        """
    )
    conn.commit()
    conn.close()


def insert_items(items: list[dict]) -> int:
    """
    Slaat een lijst van items op in de database.
    Elk item is een dict met keys: source, category, title, price, currency, availability, url
    Returnt het aantal opgeslagen rijen.
    """
    if not items:
        return 0

    conn = get_connection()
    now = datetime.utcnow().isoformat()

    rows = [
        (
            item.get("source", "unknown"),
            item.get("category"),
            item.get("title", ""),
            item.get("price"),
            item.get("currency", "GBP"),
            item.get("availability"),
            item.get("url"),
            now,
        )
        for item in items
    ]

    conn.executemany(
        """
        INSERT INTO items (source, category, title, price, currency, availability, url, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    count = conn.total_changes
    conn.close()
    return count


def fetch_all_items() -> list[sqlite3.Row]:
    """Haalt alle opgeslagen items op, nieuwste eerst."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM items ORDER BY scraped_at DESC").fetchall()
    conn.close()
    return rows


def fetch_price_history(title: str) -> list[sqlite3.Row]:
    """Haalt de prijsgeschiedenis op voor een specifieke titel, oudste eerst."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM items WHERE title = ? ORDER BY scraped_at ASC",
        (title,),
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print(f"Database geinitialiseerd op: {DB_PATH}")

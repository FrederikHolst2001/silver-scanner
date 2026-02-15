
import sqlite3
import os

DB = "data/deals.db"

def init():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS deals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        weight REAL,
        price_per_gram REAL,
        profit REAL,
        link TEXT,
        source TEXT
    )
    """)
    conn.close()

def insert(deal):
    conn = sqlite3.connect(DB)
    conn.execute("""
    INSERT INTO deals
    (title,price,weight,price_per_gram,profit,link,source)
    VALUES(?,?,?,?,?,?,?)
    """,(
        deal["title"],
        deal["price"],
        deal["weight"],
        deal["price_per_gram"],
        deal["profit"],
        deal["link"],
        deal["source"]
    ))
    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect(DB)
    rows = conn.execute("""
    SELECT title, profit, source, link
    FROM deals
    ORDER BY profit DESC
    LIMIT 100
    """).fetchall()
    conn.close()
    return rows

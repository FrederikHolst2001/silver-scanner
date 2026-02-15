
import sqlite3, os
DB="data/deals.db"

def init_db():
    os.makedirs("data",exist_ok=True)
    conn=sqlite3.connect(DB)
    conn.execute(
    "CREATE TABLE IF NOT EXISTS deals(title, price, profit, score, link)")
    conn.close()

def save_deal(deal):
    conn=sqlite3.connect(DB)
    conn.execute(
    "INSERT INTO deals VALUES(?,?,?,?,?)",
    (deal["title"],deal["price"],deal["profit"],deal["score"],deal["link"]))
    conn.commit()
    conn.close()

def get_deals():
    conn=sqlite3.connect(DB)
    rows=conn.execute(
    "SELECT title, price, profit, score, link FROM deals ORDER BY profit DESC"
    ).fetchall()
    conn.close()
    return rows

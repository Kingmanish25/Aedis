import sqlite3
from app.config import Config

def execute_query(query):
    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(query)
        data = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return cols, data
    except Exception as e:
        return [], str(e)
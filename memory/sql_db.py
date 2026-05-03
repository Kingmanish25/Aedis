import sqlite3
from app.config import Config

def execute_query(query):
    """
    Execute SQL query with proper resource management.
    
    Args:
        query: SQL query string
        
    Returns:
        (columns, data) tuple or ([], error_message) on failure
    """
    conn = None
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return cols, data
    except sqlite3.Error as e:
        return [], f"Database error: {str(e)}"
    except Exception as e:
        return [], f"Unexpected error: {str(e)}"
    finally:
        if conn:
            conn.close()
def safe_sql_fallback(query):
    q = query.lower()

    if "revenue" in q:
        return "SELECT date, region, product, revenue, cost, profit, customer_id FROM sales LIMIT 500"

    return """
    SELECT date, region, product, revenue, cost, profit, customer_id 
    FROM sales 
    LIMIT 1000
    """
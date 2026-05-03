def validate_sql(sql, schema):
    sql_lower = sql.lower()

    # ❌ Block dangerous queries
    forbidden = ["drop", "delete", "update", "insert"]
    if any(word in sql_lower for word in forbidden):
        return False, "Unsafe query"

    # ✔ Ensure known tables used
    valid_tables = list(schema.keys())
    if not any(table in sql_lower for table in valid_tables):
        return False, "Unknown table"

    return True, "Valid"
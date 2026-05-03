from .base_agent import BaseAgent
from memory.sql_db import execute_query
from tools.sql_tool import safe_sql_fallback
from memory.memory_retriever import MemoryRetriever
from tools.schema_loader import load_schema
from tools.sql_validator import validate_sql

class SQLAgent(BaseAgent):
    def run(self, state):
        self.emit("start", "Generating SQL")

        retriever = MemoryRetriever()
        past = retriever.retrieve(state["query"])

        memory_context = "\n".join([
            f"Query: {p['query']} → Actions: {p['actions']}"
            for p in past
        ])

        schema = load_schema()

        prompt = f"""
You are an expert SQL generator.

Schema:
{schema}

Learn from past queries:
{memory_context}

Generate ONLY SQL (no explanation) for:
{state['query']}
"""

        try:
            sql = self.llm.generate(prompt)

            if "select" not in sql.lower():
                sql = safe_sql_fallback(state["query"])

        except:
            sql = safe_sql_fallback(state["query"])

        valid, reason = validate_sql(sql, schema)

        if not valid:
            self.bob.log("SQL Validation Failed", reason)
            sql = safe_sql_fallback(state["query"])

        cols, data = execute_query(sql)

        if isinstance(data, str):
            self.bob.log("SQL Error", data)
            data = []

        if not data:
            self.bob.log("SQL", "⚠️ No data returned")

        state["sql"] = sql
        state["data"] = data

        self.emit("sql_generated", sql)
        self.emit("data_fetched", f"{len(data)} rows")

        return state
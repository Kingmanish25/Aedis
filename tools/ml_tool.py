import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def run_advanced_analysis(data):
    if not data:
        return {
            "monthly": None,
            "anomalies": None,
            "region_impact": {},
            "product_impact": {},
            "summary": "No data available"
        }

    # =========================
    # 1. SCHEMA HANDLING
    # =========================
    EXPECTED_COLUMNS = ["date", "region", "product", "revenue", "cost", "profit", "customer_id"]

    if isinstance(data[0], dict):
        df = pd.DataFrame(data)
    else:
        num_cols = len(data[0])
        columns = EXPECTED_COLUMNS[:num_cols]
        df = pd.DataFrame(data, columns=columns)

    # Normalize schema
    if "profit" not in df.columns and {"revenue", "cost"}.issubset(df.columns):
        df["profit"] = df["revenue"] - df["cost"]

    if "customer_id" not in df.columns:
        df["customer_id"] = "unknown"

    if "date" not in df.columns or "revenue" not in df.columns:
        return {"error": "Missing required columns"}

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "revenue"])

    # =========================
    # 2. TIME ANALYSIS
    # =========================
    monthly = df.groupby(pd.Grouper(key="date", freq="M")).agg({
        "revenue": "sum"
    }).reset_index()

    # Growth rate
    monthly["growth"] = monthly["revenue"].pct_change()

    # Rolling trend
    monthly["rolling_mean"] = monthly["revenue"].rolling(3).mean()

    # =========================
    # 3. ANOMALY DETECTION
    # =========================
    contamination = min(0.2, max(0.05, 3 / len(monthly)))  # adaptive
    model = IsolationForest(contamination=contamination, random_state=42)

    monthly["anomaly"] = model.fit_predict(monthly[["revenue"]])
    anomalies = monthly[monthly["anomaly"] == -1]

    # =========================
    # 4. ROOT CAUSE ANALYSIS
    # =========================
    region_impact = df.groupby("region")["revenue"].sum().sort_values()
    product_impact = df.groupby("product")["revenue"].sum().sort_values()

    # =========================
    # 5. BUSINESS INSIGHTS
    # =========================
    total_revenue = df["revenue"].sum()

    weakest_region = region_impact.head(1).to_dict()
    weakest_product = product_impact.head(1).to_dict()

    growth_trend = monthly["growth"].mean()

    if growth_trend < 0:
        trend_label = "declining"
    elif growth_trend > 0:
        trend_label = "growing"
    else:
        trend_label = "stable"

    summary = f"""
Revenue trend is {trend_label}.
Detected {len(anomalies)} anomaly periods.
Weakest region: {weakest_region}
Weakest product: {weakest_product}
Total revenue: {round(total_revenue, 2)}
"""

    # =========================
    # 6. STRUCTURED OUTPUT
    # =========================
    result = {
        "monthly": monthly,
        "anomalies": anomalies,
        "region_impact": region_impact.head(3).to_dict(),
        "product_impact": product_impact.head(3).to_dict(),
        "summary": summary,
        "trend": trend_label,
        "growth_rate": float(np.nanmean(monthly["growth"]))
    }

    return result
import matplotlib.pyplot as plt
import pandas as pd

def plot_revenue_trend(monthly_df):
    """
    monthly_df expected columns:
    - date
    - revenue
    - anomaly
    """

    if monthly_df is None or monthly_df.empty:
        return None

    try:
        plt.figure(figsize=(8, 4))

        # 🔹 Line plot
        plt.plot(monthly_df["date"], monthly_df["revenue"], label="Revenue")

        # 🔹 Highlight anomalies
        anomalies = monthly_df[monthly_df["anomaly"] == -1]

        if not anomalies.empty:
            plt.scatter(
                anomalies["date"],
                anomalies["revenue"],
                color="red",
                label="Anomalies"
            )

        plt.title("Revenue Trend with Anomalies")
        plt.xlabel("Date")
        plt.ylabel("Revenue")
        plt.legend()
        plt.xticks(rotation=45)

        return plt

    except Exception as e:
        print("Visualization error:", e)
        return None
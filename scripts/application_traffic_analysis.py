import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def aggregate_traffic_per_application(data):
    """Aggregate total traffic per application and user."""
    app_traffic = (
        data.groupby(["application", "MSISDN"])
        .agg({"download_data": "sum", "upload_data": "sum"})
        .reset_index()
    )
    app_traffic["total_traffic"] = (
        app_traffic["download_data"] + app_traffic["upload_data"]
    )
    return app_traffic


def plot_top_applications(app_traffic, top_n=3):
    """Plot the top N applications by total traffic."""
    app_total_traffic = (
        app_traffic.groupby("application")["total_traffic"]
        .sum()
        .sort_values(ascending=False)
    )
    top_apps = app_total_traffic.head(top_n)

    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_apps.index, y=top_apps.values, palette="viridis")
    plt.title(f"Top {top_n} Applications by Total Traffic")
    plt.ylabel("Total Traffic (Bytes)")
    plt.xlabel("Application")
    plt.show()

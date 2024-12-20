import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_top_n_handsets(df, n=10):
    """Plot the top N handsets by user count."""
    top_handsets = df["handset"].value_counts().head(n)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_handsets.index, y=top_handsets.values, palette="viridis")
    plt.title(f"Top {n} Handsets Used")
    plt.ylabel("User Count")
    plt.xticks(rotation=45)
    plt.show()


def plot_user_segmentation(df):
    """Visualize user segmentation using k-means clusters."""
    sns.scatterplot(
        x="download_data", y="upload_data", hue="cluster", data=df, palette="tab10"
    )
    plt.title("User Segmentation by Engagement Metrics")
    plt.xlabel("Download Data (Bytes)")
    plt.ylabel("Upload Data (Bytes)")
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv("../data/engineered_telecom_data.csv")

    # Example: Visualize top handsets
    plot_top_n_handsets(data, n=10)

    # Example: Visualize user segmentation
    if "cluster" in data.columns:
        plot_user_segmentation(data)

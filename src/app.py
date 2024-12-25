import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
from urllib.parse import quote

# Add the parent directory of 'src' and 'scripts' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from engagement_metrics import aggregate_engagement_metrics
from clustering import normalize_data, find_optimal_k, cluster_users
from data_aggregation import aggregate_user_behavior
from cluster_analysis import compute_cluster_metrics
from data_cleaning import clean_data
from experience_metrics import aggregate_experience_metrics
from experience_analysis import compute_top_bottom_frequent
from experience_clustering import normalize_experience_data, cluster_experience_data
from scripts.task3_visualization import save_plot
from satisfaction_scores import compute_scores
from handset_analysis import handset_analysis
from satisfaction_model import train_satisfaction_model
from export_satisfaction_scores import export_to_database


if __name__ == "__main__":
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = quote(os.getenv("DB_PASSWORD", ""))
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "telecom_data")

    connection_string = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    query = """
    SELECT * FROM xdr_data;  -- Replace with your actual table name
    """
    user_behavior = aggregate_user_behavior()
    print(user_behavior.head())  # Verify the aggregated data
    handset_analysis()

    cleaned_data = clean_data(user_behavior)
    print(cleaned_data.describe())
    print(f"total cleaned data{cleaned_data.columns}")

    # Histogram for total duration
    sns.histplot(cleaned_data["total_duration"], kde=True, bins=30)
    plt.title("Distribution of Total Session Duration")
    plt.xlabel("Total Duration")
    plt.ylabel("Frequency")
    plt.show()

    # Scatter plot of download vs. upload
    sns.scatterplot(x="total_dl", y="total_ul", data=cleaned_data)
    plt.title("Download vs. Upload Data Volume")
    plt.xlabel("Total Download (Bytes)")
    plt.ylabel("Total Upload (Bytes)")
    plt.show()

    # raw_data = aggregate_engagement_metrics()
    normalized_data = normalize_data(
        cleaned_data, ["num_sessions", "total_duration", "total_data_volume"]
    )

    # Find optimal k
    find_optimal_k(normalized_data, max_k=10)

    # Cluster users (example: k=3)
    clustered_data, model = cluster_users(normalized_data, n_clusters=3)
    print("clustered data head: ", clustered_data.head())

    # Scatter plot of engagement clusters
    sns.scatterplot(
        x="total_duration",
        y="total_data_volume",
        hue="cluster",
        data=clustered_data,
        palette="viridis",
    )
    plt.title("Engagement Clusters")
    plt.xlabel("Total Duration (Normalized)")
    plt.ylabel("Total Traffic (Normalized)")
    plt.legend(title="Cluster")
    plt.show()

    # Bar plot for top 3 most used applications
    top_3_apps = (
        clustered_data[["total_data_volume", "engagement_cluster"]]
        .groupby("engagement_cluster")
        .sum()
        .nlargest(3, "total_data_volume")
    )
    top_3_apps.plot(kind="bar", legend=False)
    plt.title("Top 3 Most Used Applications by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Total Traffic (Bytes)")
    plt.show()
    save_plot(plt, "throughput_per_handset.png")

    summary = compute_cluster_metrics(clustered_data)
    print("summary: ", summary)

    # Scatter plot of engagement clusters
    sns.scatterplot(
        x="total_duration",
        y="total_data_volume",
        hue="cluster",
        data=clustered_data,
        palette="viridis",
    )
    plt.title("Engagement Clusters")
    plt.xlabel("Total Duration (Normalized)")
    plt.ylabel("Total Traffic (Normalized)")
    plt.legend(title="Cluster")
    plt.show()

    # Bar plot for top 3 most used applications
    top_3_apps = (
        clustered_data[["total_data_volume", "engagement_cluster"]]
        .groupby("engagement_cluster")
        .sum()
        .nlargest(3, "total_data_volume")
    )
    top_3_apps.plot(kind="bar", legend=False)
    plt.title("Top 3 Most Used Applications by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Total Traffic (Bytes)")
    plt.show()

    experience_data = aggregate_experience_metrics()
    print("Aggregated Experience Data:", experience_data.head())
    # Top, bottom, and frequent values for TCP retransmission
    top_tcp, bottom_tcp, frequent_tcp = compute_top_bottom_frequent(
        experience_data, "avg_tcp_retransmission"
    )
    print("Top TCP Retransmission:", top_tcp)
    print("Bottom TCP Retransmission:", bottom_tcp)
    print("Frequent TCP Retransmission:", frequent_tcp)

    normalized_data = normalize_experience_data(experience_data)
    print("Normalized data: ", normalized_data)
    print(normalized_data.isnull().sum())

    cluster_data, _ = cluster_experience_data(normalized_data, n_clusters=3)
    print("column  clustedred:", cluster_data.columns)  # View clustered data

    # Distribution of Throughput per Handset
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Handset Type", y="avg_throughput", data=clustered_data)
    plt.xticks(rotation=90)
    plt.title("Average Throughput per Handset Type")
    plt.xlabel("Handset Type")
    plt.ylabel("Average Throughput")
    save_plot(plt, "throughput_per_handset.png")

    # TCP Retransmission per Handset
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Handset Type", y="avg_tcp_retransmission", data=clustered_data)
    plt.xticks(rotation=90)
    plt.title("Average TCP Retransmission per Handset Type")
    plt.xlabel("Handset type")
    plt.ylabel("Average TCP Retransmission")
    save_plot(plt, "tcp_retransmission_per_handset.png")

    # Experience Clusters Visualization
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x="avg_rtt",
        y="avg_throughput",
        hue="experience_cluster",
        palette="viridis",
        data=clustered_data,
    )
    plt.title("Experience Clusters")
    plt.xlabel("Average RTT (Normalized)")
    plt.ylabel("Average Throughput (Normalized)")
    plt.legend(title="Cluster")
    save_plot(plt, "experience_clusters.png")

    # Compute scores
    scores = compute_scores(clustered_data, cluster_data)
    print(scores.head())  # Check satisfaction scores

    # Satisfaction Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(scores["satisfaction_score"], kde=True)
    plt.title("Satisfaction Score Distribution")
    plt.xlabel("Satisfaction Score")
    plt.ylabel("Frequency")
    save_plot(plt, "satisfaction_score_distribution.png")
    # Train model
    model = train_satisfaction_model(scores)
    export_to_database(scores, "telecom_data", connection_string)

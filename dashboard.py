import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add the parent directory of 'src' and 'scripts' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.clustering import normalize_data, find_optimal_k, cluster_users
from src.data_cleaning import clean_data
from src.data_aggregation import aggregate_user_behavior
from src.experience_metrics import aggregate_experience_metrics
from src.cluster_analysis import compute_cluster_metrics
from src.experience_analysis import compute_top_bottom_frequent
from src.experience_clustering import normalize_experience_data, cluster_experience_data
from src.satisfaction_scores import compute_scores
from src.satisfaction_model import train_satisfaction_model
from src.export_satisfaction_scores import export_to_database


def main():
    st.title("Telecom Data Analytics Dashboard")

    # Sidebar configuration
    st.sidebar.title("Navigation")
    options = [
        "User Behavior Aggregation",
        "Engagement Clustering",
        "Experience Metrics",
        "Satisfaction Analysis",
    ]
    choice = st.sidebar.radio("Select Analysis", options)

    # Database connection details
    username = "postgres"
    password = "125191"
    host = "localhost"
    port = 5432
    database_name = "telecom_data"
    connection_string = (
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
    )

    if choice == "User Behavior Aggregation":
        st.header("User Behavior Aggregation")
        user_behavior = aggregate_user_behavior()
        st.write("Aggregated User Behavior Data")
        st.dataframe(user_behavior.head())

        cleaned_data = clean_data(user_behavior)
        st.write("Cleaned Data")
        st.dataframe(cleaned_data.describe())

        # Histogram for total duration
        st.subheader("Distribution of Total Session Duration")
        fig, ax = plt.subplots()
        sns.histplot(cleaned_data["total_duration"], kde=True, bins=30, ax=ax)
        ax.set(
            title="Total Session Duration", xlabel="Total Duration", ylabel="Frequency"
        )
        st.pyplot(fig)

        # Scatter plot of download vs. upload
        st.subheader("Download vs. Upload Data Volume")
        fig, ax = plt.subplots()
        sns.scatterplot(x="total_dl", y="total_ul", data=cleaned_data, ax=ax)
        ax.set(
            title="Download vs. Upload",
            xlabel="Total Download (Bytes)",
            ylabel="Total Upload (Bytes)",
        )
        st.pyplot(fig)

    elif choice == "Engagement Clustering":
        st.header("Engagement Clustering")
        user_behavior = aggregate_user_behavior()
        cleaned_data = clean_data(user_behavior)

        normalized_data = normalize_data(
            cleaned_data, ["num_sessions", "total_duration", "total_data_volume"]
        )

        # Find optimal k
        st.subheader("Finding Optimal Number of Clusters")
        fig, ax = plt.subplots()
        find_optimal_k(normalized_data, max_k=10)
        st.pyplot(fig)

        # Cluster users (example: k=3)
        clustered_data, model = cluster_users(normalized_data, n_clusters=3)
        st.write("Clustered Data")
        st.dataframe(clustered_data.head())

        # Scatter plot of engagement clusters
        st.subheader("Engagement Clusters")
        fig, ax = plt.subplots()
        sns.scatterplot(
            x="total_duration",
            y="total_data_volume",
            hue="engagement_cluster",
            data=clustered_data,
            palette="viridis",
            ax=ax,
        )
        ax.set(
            title="Engagement Clusters",
            xlabel="Total Duration (Normalized)",
            ylabel="Total Traffic (Normalized)",
        )
        st.pyplot(fig)

    elif choice == "Experience Metrics":
        st.header("Experience Metrics")
        experience_data = aggregate_experience_metrics()
        st.write("Aggregated Experience Data")
        st.dataframe(experience_data.head())

        top_tcp, bottom_tcp, frequent_tcp = compute_top_bottom_frequent(
            experience_data, "avg_tcp_retransmission"
        )

        st.write("Top TCP Retransmission", top_tcp)
        st.write("Bottom TCP Retransmission", bottom_tcp)
        st.write("Frequent TCP Retransmission", frequent_tcp)

        normalized_data = normalize_experience_data(experience_data)
        clustered_data, _ = cluster_experience_data(normalized_data, n_clusters=3)

        # Experience Clusters Visualization
        st.subheader("Experience Clusters")
        fig, ax = plt.subplots()
        sns.scatterplot(
            x="avg_rtt",
            y="avg_throughput",
            hue="experience_cluster",
            palette="viridis",
            data=cluster_data,
            ax=ax,
        )
        ax.set(
            title="Experience Clusters",
            xlabel="Average RTT (Normalized)",
            ylabel="Average Throughput (Normalized)",
        )
        st.pyplot(fig)

    elif choice == "Satisfaction Analysis":
        st.header("Satisfaction Analysis")
        # Ensure engagement clustering is done
        engagement_features = ["num_sessions", "total_duration", "total_data_volume"]
        user_behavior = aggregate_user_behavior()
        cleaned_data = clean_data(user_behavior)

        normalized_engagement = normalize_data(cleaned_data, engagement_features)
        clustered_data, _ = cluster_users(normalized_engagement, n_clusters=3)

        experience_data = aggregate_experience_metrics()
        normalized_data = normalize_experience_data(experience_data)
        cluster_data, _ = cluster_experience_data(normalized_data, n_clusters=3)

        scores = compute_scores(clustered_data, cluster_data)
        st.write("Satisfaction Scores")
        st.dataframe(scores.head())

        # Satisfaction Distribution
        st.subheader("Satisfaction Score Distribution")
        fig, ax = plt.subplots()
        sns.histplot(scores["satisfaction_score"], kde=True, ax=ax)
        ax.set(
            title="Satisfaction Score Distribution",
            xlabel="Satisfaction Score",
            ylabel="Frequency",
        )
        st.pyplot(fig)


if __name__ == "__main__":
    main()

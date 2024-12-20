import pandas as pd
from user_engagement_metrics import (
    aggregate_metrics,
    normalize_metrics,
    cluster_users,
    compute_cluster_stats,
)
from application_traffic_analysis import (
    aggregate_traffic_per_application,
    plot_top_applications,
)
from elbow_method import find_optimal_k, plot_elbow_and_silhouette

# Load the dataset
data = pd.read_csv("telecom_data.csv")

# Task 2.1: Aggregate metrics
agg_metrics = aggregate_metrics(data)

# Normalize metrics
normalized_data, scaler = normalize_metrics(agg_metrics)

# Find optimal k using elbow method
k_range, inertia, silhouette_scores = find_optimal_k(normalized_data, max_k=10)
plot_elbow_and_silhouette(k_range, inertia, silhouette_scores)

# Perform clustering with k=3
cluster_labels, cluster_centers = cluster_users(normalized_data, k=3)
cluster_stats = compute_cluster_stats(agg_metrics, cluster_labels)
print("Cluster Statistics:\n", cluster_stats)

# Aggregate application traffic
app_traffic = aggregate_traffic_per_application(data)

# Plot top 3 applications
plot_top_applications(app_traffic, top_n=3)

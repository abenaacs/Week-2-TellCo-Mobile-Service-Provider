import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


def aggregate_metrics(data):
    """Aggregate user engagement metrics per MSISDN."""
    agg_metrics = (
        data.groupby("MSISDN")
        .agg(
            {
                "session_id": "count",
                "session_duration": "sum",
                "download_data": "sum",
                "upload_data": "sum",
            }
        )
        .reset_index()
    )
    agg_metrics["total_traffic"] = (
        agg_metrics["download_data"] + agg_metrics["upload_data"]
    )
    agg_metrics.rename(
        columns={
            "session_id": "session_frequency",
            "session_duration": "total_duration",
        },
        inplace=True,
    )
    return agg_metrics


def normalize_metrics(agg_metrics):
    """Normalize engagement metrics."""
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(
        agg_metrics[["session_frequency", "total_duration", "total_traffic"]]
    )
    return normalized_data, scaler


def cluster_users(normalized_data, k=3):
    """Cluster users using k-means."""
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(normalized_data)
    return labels, kmeans.cluster_centers_


def compute_cluster_stats(agg_metrics, cluster_labels):
    """Compute statistics for each cluster."""
    agg_metrics["cluster"] = cluster_labels
    cluster_stats = (
        agg_metrics.groupby("cluster")
        .agg(
            {
                "session_frequency": ["min", "max", "mean", "sum"],
                "total_duration": ["min", "max", "mean", "sum"],
                "total_traffic": ["min", "max", "mean", "sum"],
            }
        )
        .reset_index()
    )
    return cluster_stats

import logging


def compute_cluster_metrics(df):
    """
    Compute summary metrics for each cluster.

    Args:
        df (pd.DataFrame): Input DataFrame with cluster labels.

    Returns:
        pd.DataFrame: Cluster metrics summary.
    """
    try:
        cluster_summary = df.groupby("engagement_cluster").agg(
            min_sessions=("num_sessions", "min"),
            max_sessions=("num_sessions", "max"),
            avg_sessions=("num_sessions", "mean"),
            total_sessions=("num_sessions", "sum"),
            min_duration=("total_duration", "min"),
            max_duration=("total_duration", "max"),
            avg_duration=("total_duration", "mean"),
            total_duration=("total_duration", "sum"),
            min_traffic=("total_data_volume", "min"),
            max_traffic=("total_data_volume", "max"),
            avg_traffic=("total_data_volume", "mean"),
            total_data_volume=("total_data_volume", "sum"),
        )
        logging.info("Cluster metrics computed successfully.")
    except Exception as e:
        logging.error(f"Error during cluster metrics computation: {e}")
        raise

    return cluster_summary

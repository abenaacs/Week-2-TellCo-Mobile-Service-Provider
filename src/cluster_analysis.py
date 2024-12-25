def compute_cluster_metrics(df):
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
    return cluster_summary

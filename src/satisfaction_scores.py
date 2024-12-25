import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean


def compute_scores(clustered_engagement, clustered_experience):
    # Ensure required columns are present
    required_columns_engagement = [
        "num_sessions",
        "total_duration",
        "total_data_volume",
    ]
    required_columns_experience = [
        "avg_tcp_retransmission",
        "avg_rtt",
        "avg_throughput",
    ]

    for col in required_columns_engagement:
        if col not in clustered_engagement.columns:
            raise KeyError(f"Missing column {col} in clustered_engagement")

    for col in required_columns_experience:
        if col not in clustered_experience.columns:
            raise KeyError(f"Missing column {col} in clustered_experience")

    # Impute missing values in experience data
    clustered_experience = clustered_experience.fillna(
        {
            "avg_tcp_retransmission": clustered_experience[
                "avg_tcp_retransmission"
            ].mean(),
            "avg_rtt": clustered_experience["avg_rtt"].mean(),
            "avg_throughput": clustered_experience["avg_throughput"].mean(),
        }
    )

    # Compute engagement score: Euclidean distance from the least engaged cluster (cluster 0)
    engagement_cluster_0_mean = clustered_engagement[
        clustered_engagement["engagement_cluster"] == 0
    ][required_columns_engagement].mean()

    clustered_engagement["engagement_score"] = clustered_engagement.apply(
        lambda row: euclidean(
            row[required_columns_engagement],
            engagement_cluster_0_mean,
        ),
        axis=1,
    )

    # Compute experience score: Euclidean distance from the worst experience cluster (cluster 2)
    experience_cluster_2_mean = clustered_experience[
        clustered_experience["experience_cluster"] == 2
    ][required_columns_experience].mean()

    clustered_experience["experience_score"] = clustered_experience.apply(
        lambda row: euclidean(
            row[required_columns_experience],
            experience_cluster_2_mean,
        ),
        axis=1,
    )

    # Combine both engagement and experience scores
    scores = pd.merge(
        clustered_engagement[["MSISDN/Number", "engagement_score"]],
        clustered_experience[["MSISDN/Number", "experience_score"]],
        on="MSISDN/Number",
    )
    scores["satisfaction_score"] = (
        scores["engagement_score"] + scores["experience_score"]
    ) / 2

    return scores

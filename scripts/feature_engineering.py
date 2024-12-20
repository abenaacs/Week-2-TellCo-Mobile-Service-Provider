import pandas as pd


def calculate_engagement_metrics(df):
    """Calculate engagement metrics: sessions frequency, duration, and total traffic."""
    df["total_data"] = df["download_data"] + df["upload_data"]
    df["average_session_duration"] = df["total_session_duration"] / df["session_count"]
    return df


def segment_users(df):
    """Segment users into deciles based on total data usage."""
    df["usage_decile"] = pd.qcut(df["total_data"], 10, labels=False)
    return df


def aggregate_user_data(df):
    """Aggregate data per user (MSISDN)."""
    aggregated = (
        df.groupby("MSISDN")
        .agg(
            {
                "session_count": "sum",
                "total_session_duration": "sum",
                "download_data": "sum",
                "upload_data": "sum",
                "total_data": "sum",
            }
        )
        .reset_index()
    )
    return aggregated


if __name__ == "__main__":
    # Load the cleaned dataset
    data = pd.read_csv("../data/cleaned_telecom_data.csv")

    # Calculate engagement metrics
    data = calculate_engagement_metrics(data)

    # Segment users
    data = segment_users(data)

    # Aggregate user data
    user_data = aggregate_user_data(data)

    # Save the engineered data
    user_data.to_csv("../data/engineered_telecom_data.csv", index=False)

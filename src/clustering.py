from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import logging


def normalize_data(df, columns):
    """
    Normalize specified columns using MinMaxScaler.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): List of columns to normalize.

    Returns:
        pd.DataFrame: DataFrame with normalized columns.
    """
    try:
        scaler = MinMaxScaler()
        df[columns] = scaler.fit_transform(df[columns])
        logging.info("Data normalization completed successfully.")
    except Exception as e:
        logging.error(f"Error during data normalization: {e}")
        raise

    return df


def cluster_users(df, n_clusters):
    """
    Perform user clustering using KMeans.

    Args:
        df (pd.DataFrame): Input DataFrame with normalized columns.
        n_clusters (int): Number of clusters.

    Returns:
        pd.DataFrame: DataFrame with added cluster labels.
        KMeans: Fitted KMeans model.
    """
    required_columns = ["num_sessions", "total_duration", "total_data_volume"]
    try:
        # Check for required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Missing required columns for clustering: {missing_cols}")

        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df["engagement_cluster"] = kmeans.fit_predict(df[required_columns])
        logging.info("Clustering completed successfully.")
    except Exception as e:
        logging.error(f"Error during clustering: {e}")
        raise

    return df, kmeans

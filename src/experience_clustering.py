from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import pandas as pd


def normalize_experience_data(df):
    required_columns = ["avg_tcp_retransmission", "avg_rtt", "avg_throughput"]

    # Ensure required columns exist in the dataframe
    if not all(col in df.columns for col in required_columns):
        raise ValueError(
            f"Missing required columns: {set(required_columns) - set(df.columns)}"
        )

    scaler = MinMaxScaler()
    df[required_columns] = scaler.fit_transform(df[required_columns])
    return df


def cluster_experience_data(df, n_clusters=3):
    # Separate numeric and non-numeric data
    numeric_data = df.select_dtypes(include=["number"])
    non_numeric_data = df.select_dtypes(exclude=["number"])

    # Handle missing values in numeric columns
    numeric_imputer = SimpleImputer(strategy="mean")
    filled_numeric_data = pd.DataFrame(
        numeric_imputer.fit_transform(numeric_data),
        columns=numeric_data.columns,
        index=numeric_data.index,  # Ensure indices match
    )

    # Handle missing values in non-numeric columns
    non_numeric_imputer = SimpleImputer(strategy="most_frequent")
    filled_non_numeric_data = pd.DataFrame(
        non_numeric_imputer.fit_transform(non_numeric_data),
        columns=non_numeric_data.columns,
        index=non_numeric_data.index,  # Ensure indices match
    )

    # Combine numeric and non-numeric data
    filled_data = pd.concat([filled_numeric_data, filled_non_numeric_data], axis=1)

    # Perform clustering using selected numeric features
    required_features = ["avg_tcp_retransmission", "avg_rtt", "avg_throughput"]
    if not all(col in filled_data.columns for col in required_features):
        raise ValueError(
            f"Missing required clustering features: {set(required_features) - set(filled_data.columns)}"
        )

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    filled_data["experience_cluster"] = kmeans.fit_predict(
        filled_data[required_features]
    )

    return filled_data, kmeans

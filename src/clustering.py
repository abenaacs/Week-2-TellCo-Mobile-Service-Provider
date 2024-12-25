import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def normalize_data(df, columns):
    print(f"columns {columns}")
    print(f"data {df.columns}")
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def cluster_users(df, n_clusters):
    # Ensure necessary columns are present
    required_columns = ["num_sessions", "total_duration", "total_data_volume"]
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"Missing one or more required columns: {required_columns}")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["engagement_cluster"] = kmeans.fit_predict(df[required_columns])
    return df, kmeans


def find_optimal_k(df, max_k=10):
    distortions = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df[["num_sessions", "total_duration", "total_data_volume"]])
        distortions.append(kmeans.inertia_)
    plt.plot(range(1, max_k + 1), distortions, marker="o")
    plt.title("Elbow Method to Find Optimal K")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Distortion")
    plt.show()

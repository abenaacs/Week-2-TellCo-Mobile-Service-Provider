import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def find_optimal_k(normalized_data, max_k=10):
    """Find the optimal number of clusters using the elbow method."""
    inertia = []
    silhouette_scores = []
    k_range = range(2, max_k + 1)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(normalized_data)
        inertia.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(normalized_data, kmeans.labels_))

    return k_range, inertia, silhouette_scores


def plot_elbow_and_silhouette(k_range, inertia, silhouette_scores):
    """Plot the elbow and silhouette score methods."""
    plt.figure(figsize=(8, 6))
    plt.plot(k_range, inertia, marker="o")
    plt.title("Elbow Method for Optimal k")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.plot(k_range, silhouette_scores, marker="o", color="orange")
    plt.title("Silhouette Scores for Optimal k")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.show()

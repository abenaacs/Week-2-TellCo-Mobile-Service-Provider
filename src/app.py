import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
from urllib.parse import quote
import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Add the parent directory of 'src' and 'scripts' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import modules (ensure these modules exist and are documented)
from clustering import normalize_data, find_optimal_k, cluster_users
from data_aggregation import aggregate_user_behavior
from data_cleaning import clean_data
from scripts.task3_visualization import save_plot
from satisfaction_scores import compute_scores
from satisfaction_model import train_satisfaction_model
from export_satisfaction_scores import export_to_database


def main():
    """Main function to execute data processing, clustering, and visualization tasks."""
    try:
        # Load environment variables for DB connection
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = quote(os.getenv("DB_PASSWORD", ""))
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "telecom_data")

        # Validate DB credentials
        if not DB_USERNAME or not DB_PASSWORD:
            logging.error(
                "Database credentials are not properly set in environment variables."
            )
            return

        # Build connection string
        connection_string = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        logging.info("Starting data aggregation...")
        user_behavior = aggregate_user_behavior()
        if user_behavior.empty:
            logging.error("Aggregated user behavior data is empty.")
            return
        logging.info("Data aggregation completed successfully.")

        # Data cleaning
        logging.info("Cleaning data...")
        cleaned_data = clean_data(user_behavior)
        if cleaned_data.empty:
            logging.error("Cleaned data is empty.")
            return

        # Data visualization (example)
        try:
            logging.info("Creating data visualizations...")
            sns.histplot(cleaned_data["total_duration"], kde=True, bins=30)
            plt.title("Distribution of Total Session Duration")
            plt.xlabel("Total Duration")
            plt.ylabel("Frequency")
            plt.show()
        except Exception as e:
            logging.error(f"Error during visualization: {e}")

        # Clustering
        logging.info("Normalizing data and clustering...")
        normalized_data = normalize_data(
            cleaned_data, ["num_sessions", "total_duration", "total_data_volume"]
        )
        find_optimal_k(normalized_data, max_k=10)

        clustered_data, model = cluster_users(normalized_data, n_clusters=3)
        if clustered_data.empty:
            logging.error("Clustered data is empty.")
            return

        # Save results
        save_plot(plt, "engagement_clusters.png")
        logging.info("Clustering and visualization completed successfully.")

        # Compute scores and export
        scores = compute_scores(clustered_data)
        if scores.empty:
            logging.error("Satisfaction scores are empty.")
            return

        train_satisfaction_model(scores)
        export_to_database(scores, "telecom_data", connection_string)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return


if __name__ == "__main__":
    main()

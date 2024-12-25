import pandas as pd
from data_extraction import extract_data
import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def aggregate_user_behavior():
    """
    Aggregate user behavior data by computing session counts, total duration,
    and total data volume.

    Returns:
        pd.DataFrame: Aggregated user behavior DataFrame.
    """
    try:
        # Load raw data
        data = extract_data(None)

        # Rename columns for consistency
        data.rename(
            columns={
                "Column1": "MSISDN/Number",
                "Column3": "session_duration",
                "Column4": "Total DL (Bytes)",
                "Column5": "Total UL (Bytes)",
            },
            inplace=True,
        )

        # Convert relevant columns to numeric
        data["Total DL (Bytes)"] = pd.to_numeric(
            data["Total DL (Bytes)"], errors="coerce"
        )
        data["Total UL (Bytes)"] = pd.to_numeric(
            data["Total UL (Bytes)"], errors="coerce"
        )

        # Calculate total data volume
        data["Total Data (Bytes)"] = data["Total DL (Bytes)"] + data["Total UL (Bytes)"]

        # Aggregate user behavior
        user_behavior = (
            data.groupby("MSISDN/Number")
            .agg(
                num_sessions=("Bearer Id", "count"),
                total_duration=("session_duration", "sum"),
                total_dl=("Total DL (Bytes)", "sum"),
                total_ul=("Total UL (Bytes)", "sum"),
                total_data_volume=("Total Data (Bytes)", "sum"),
            )
            .reset_index()
        )

        logging.info("User behavior aggregation completed successfully.")
    except Exception as e:
        logging.error(f"Error during user behavior aggregation: {e}")
        raise

    return user_behavior

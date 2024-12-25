import pandas as pd
from data_extraction import extract_data


def aggregate_user_behavior():
    # Load the raw data
    data = extract_data(None)

    # Rename columns if needed
    data.rename(
        columns={
            "Column1": "MSISDN/Number",
            "Column2": "",
            "Column3": "session_duration",
            "Column4": "Total DL (Bytes)",
            "Column5": "Total UL (Bytes)",
        },
        inplace=True,
    )

    # Convert the relevant columns to numeric types (if not already)
    data["Total DL (Bytes)"] = pd.to_numeric(data["Total DL (Bytes)"], errors="coerce")
    data["Total UL (Bytes)"] = pd.to_numeric(data["Total UL (Bytes)"], errors="coerce")
    # Now, you can safely aggregate the data
    data["Total Data (Bytes)"] = data["Total DL (Bytes)"] + data["Total UL (Bytes)"]

    # Aggregate user behavior
    user_behavior = (
        data.groupby("MSISDN/Number")
        .agg(
            num_sessions=("Bearer Id", "count"),
            total_duration=("Dur. (ms)", "sum"),
            total_dl=("Total DL (Bytes)", "sum"),
            total_ul=("Total UL (Bytes)", "sum"),
            total_data_volume=("Total Data (Bytes)", "sum"),
        )
        .reset_index()
    )
    print(user_behavior.head())
    return user_behavior

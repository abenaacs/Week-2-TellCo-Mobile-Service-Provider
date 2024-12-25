import pandas as pd

# Load data
from data_extraction import extract_data


def handset_analysis():

    query = "SELECT msisdn, Handset Type, Handset Manufacturer FROM user_handset_data;"  # Replace table name
    handset_data = extract_data(query)

    # Top 10 Handsets
    top_handsets = handset_data["Handset Type"].value_counts().head(10)
    print("Top 10 Handsets:\n", top_handsets)

    # Top 3 Handset Manufacturers
    top_manufacturers = handset_data["Handset Manufacturer"].value_counts().head(3)
    print("Top 3 Manufacturers:\n", top_manufacturers)

    # Top 5 Handsets per Top 3 Manufacturers
    top_manufacturer_handsets = (
        handset_data[handset_data["Handset Manufacturer"].isin(top_manufacturers.index)]
        .groupby(["Handset Manufacturer", "Handset Type"])
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
    )
    print(
        "Top 5 Handsets per Top 3 Manufacturers:\n",
        top_manufacturer_handsets.groupby("Handset Manufacturer").head(5),
    )

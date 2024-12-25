import pandas as pd
from data_extraction import extract_data


def aggregate_engagement_metrics():

    engagement_data = extract_data(None)
    print(f"engangement data {engagement_data.columns}")
    return engagement_data

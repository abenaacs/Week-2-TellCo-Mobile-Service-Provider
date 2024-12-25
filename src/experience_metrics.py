import pandas as pd
from src.data_extraction import extract_data


def aggregate_experience_metrics():
    data = extract_data(None)
    # Compute averages for analysis
    data["avg_tcp_retransmission"] = (
        data["TCP DL Retrans. Vol (Bytes)"] + data["TCP UL Retrans. Vol (Bytes)"]
    ) / 2
    data["avg_rtt"] = (data["Avg RTT DL (ms)"] + data["Avg RTT UL (ms)"]) / 2
    data["avg_throughput"] = (
        data["TCP DL Retrans. Vol (Bytes)"] + data["Avg Bearer TP UL (kbps)"]
    ) / 2
    experience_data = (
        data.groupby(["MSISDN/Number", "Handset Type"])
        .agg(
            {
                "avg_tcp_retransmission": "mean",
                "avg_rtt": "mean",
                "avg_throughput": "mean",
            }
        )
        .reset_index()
    )
    return experience_data

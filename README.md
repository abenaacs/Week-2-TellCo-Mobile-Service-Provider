# Telco Mobile Service Provider Analysis

## Overview

This project analyzes mobile service provider data to derive meaningful insights and actionable recommendations. The analysis focuses on user behavior, device preferences, traffic patterns, and engagement metrics. It aims to provide a comprehensive understanding of customer segments and device performance to optimize service offerings, improve customer experience, and guide strategic decisions.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Data Analysis](#data-analysis)
3. [Clustering and Insights](#clustering-and-insights)
4. [Dashboard Development](#dashboard-development)
5. [Running the Application](#running-the-application)
6. [Recommendations](#recommendations)
7. [License](#license)

---

## Project Setup

This project includes data preprocessing, analysis, and visualization using Python libraries. The dashboard is developed using Streamlit to display insights interactively.

### Requirements

To run this project, you need the following Python libraries:

- `pandas` for data manipulation
- `numpy` for numerical operations
- `matplotlib` and `seaborn` for data visualization
- `scikit-learn` for clustering and model evaluation
- `streamlit` for building the interactive dashboard

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abenaacs/Week-2-TellCo-Mobile-Service-Provider.git
   cd Week-2-TellCo-Mobile-Service-Provider
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Data Analysis

The data used in this analysis consists of user behavior, handset types, traffic metrics, and engagement scores. The key steps involved in the analysis are:

- **Data Preprocessing**: Handling missing values, outliers, and normalizing data.
- **Segmentation**: Clustered users into different engagement levels based on their traffic and activity.
- **Device Analysis**: Analyzing the most popular handsets and manufacturers, along with their associated user behaviors.
- **Key Metrics**: Total sessions, total duration, download/upload traffic, and engagement scores.

---

## Clustering and Insights

### Clustering

The dataset was segmented into three clusters based on user traffic behavior:

- **Cluster 0**: 12% of users; highest average traffic and engagement.
- **Cluster 1**: 35% of users; moderate traffic and engagement.
- **Cluster 2**: 53% of users; minimal traffic and engagement.

### Key Insights

1. **Top Handsets**:

   - **Huawei B528S-23A**: 19,752 users
   - **Apple iPhone 6S (A1688)**: 9,419 users
   - **Apple iPhone 6 (A1586)**: 9,023 users
   - **Apple iPhone 7 (A1778)**: 6,326 users
   - **Apple iPhone Se (A1723)**: 5,187 users

2. **Market Share**:

   - **Apple**: 34% market share
   - **Samsung**: 24% market share
   - **Huawei**: 20% market share

3. **Engagement Clusters**:
   - **Cluster 0** (high engagement) should be the primary focus for retaining top-tier users.
   - **Cluster 2** (low engagement) users need further attention to improve service offerings and engagement.

---

## Dashboard Development

An interactive dashboard is developed using **Streamlit** to visualize the insights. The dashboard provides real-time interaction with key metrics, including:

- **Top Handsets**: View popular devices by manufacturer.
- **Engagement Segments**: Visualize user clusters and their traffic patterns.
- **Device Performance**: Display TCP retransmission, RTT, and throughput for top devices.

### Features:

- **Interactive Charts** for visualizing user segments, handset popularity, and engagement.
- **User Filtering** based on device type, traffic, and engagement clusters.
- **Real-Time Analysis** of user data for actionable insights.

---

# Testing

Run tests using:

```bash
pytest
```

## Running the Application

1. Start the Streamlit app:

   ```bash
   streamlit run src/app.py
   ```

2. The dashboard will open in your default web browser. You can explore the interactive visualizations and drill down into specific user segments, handsets, and engagement metrics.

---

## Recommendations

Based on the analysis, the following actions are recommended:

1. **Retention Strategies**: Focus on retaining users from **Cluster 0** (high engagement) with exclusive offers and loyalty programs.
2. **Targeted Marketing**: Create tailored marketing campaigns for users in **Cluster 1** (moderate engagement) to boost traffic and engagement.
3. **Improve Services for Cluster 2**: Engage with **Cluster 2** (low engagement) users by offering better network experiences and targeted promotions.
4. **Device-Specific Promotions**: Highlight top-selling devices like **Apple iPhones** and **Huawei** handsets, offering exclusive deals or discounts to attract new users.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

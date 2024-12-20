import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_variable_distribution(df, column, title):
    """Plot the distribution of a single variable."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.show()


def plot_correlation_matrix(df, title="Correlation Matrix"):
    """Plot a correlation matrix."""
    correlation = df.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # Load the engineered data
    data = pd.read_csv("../data/engineered_telecom_data.csv")

    # Plot distribution of total data usage
    plot_variable_distribution(data, "total_data", "Distribution of Total Data Usage")

    # Plot correlation matrix
    plot_correlation_matrix(data)

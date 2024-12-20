import pandas as pd
from sklearn.impute import SimpleImputer


def load_data(file_path):
    """Load dataset from a CSV file."""
    return pd.read_csv(file_path)


def handle_missing_values(df, strategy="mean"):
    """Fill missing values using the specified strategy."""
    imputer = SimpleImputer(strategy=strategy)
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df


def handle_outliers(df, z_threshold=3):
    """Remove outliers using the Z-score method."""
    from scipy.stats import zscore

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    z_scores = df[numeric_cols].apply(zscore)
    df_clean = df[(z_scores.abs() < z_threshold).all(axis=1)]
    return df_clean


if __name__ == "__main__":
    # Load the dataset
    data = load_data("../data/telecom_data.csv")

    # Handle missing values
    data = handle_missing_values(data)

    # Handle outliers
    data = handle_outliers(data)

    # Save cleaned data
    data.to_csv("../data/cleaned_telecom_data.csv", index=False)

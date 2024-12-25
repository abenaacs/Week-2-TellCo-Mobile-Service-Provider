import pandas as pd
from sklearn.impute import SimpleImputer


def clean_data(df):

    # Separate numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    non_numeric_cols = df.select_dtypes(exclude=["number"]).columns

    # Handle missing values for numeric columns (mean strategy)
    numeric_imputer = SimpleImputer(strategy="mean")
    df[numeric_cols] = numeric_imputer.fit_transform(df[numeric_cols])

    # Handle missing values for non-numeric columns (most frequent strategy)
    if not non_numeric_cols.empty:
        non_numeric_imputer = SimpleImputer(strategy="most_frequent")
        df[non_numeric_cols] = non_numeric_imputer.fit_transform(df[non_numeric_cols])

    return df

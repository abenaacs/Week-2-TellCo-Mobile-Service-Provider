def compute_top_bottom_frequent(df, column, top_n=10):
    if column not in df.columns:
        raise KeyError(f"Column {column} not found in DataFrame.")
    top_values = df.nlargest(top_n, column)
    bottom_values = df.nsmallest(top_n, column)
    frequent_values = df[column].value_counts().head(top_n)
    return top_values, bottom_values, frequent_values

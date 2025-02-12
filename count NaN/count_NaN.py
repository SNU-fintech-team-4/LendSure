import pandas as pd

# 1. Read the temp.csv file
df = pd.read_csv('temp.csv')

# 2. Create a new DataFrame with the specified columns
nan_counts = df.isna().sum()
nan_ratios = df.isna().mean()
data_types = df.dtypes

new_data = {
    'Column Name': df.columns,
    'NaN Count': nan_counts,
    'NaN Ratio': nan_ratios,
    'Data Type': data_types,
    'Unique Values': [df[col].unique() if data_types[col] == 'object' else None for col in df.columns]
}

new_df = pd.DataFrame(new_data)

# 3. Export the new DataFrame to a CSV file
new_df.to_csv('nan_summary.csv', index=False)

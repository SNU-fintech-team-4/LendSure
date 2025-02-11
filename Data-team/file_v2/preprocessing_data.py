import pandas as pd

# Load the CSV file
file_path = './data_preprocessed_v1.csv'
df = pd.read_csv(file_path)

# Drop columns with more than 30% missing values
threshold = 0.3
missing_percentage = df.isnull().mean()
columns_to_drop = missing_percentage[missing_percentage > threshold].index
df_dropped_columns = df.drop(columns=columns_to_drop)

# Create a matrix for dropped columns
dropped_columns_matrix = pd.DataFrame({
    'Column Name': columns_to_drop,
    'Missing Percentage': missing_percentage[columns_to_drop],
    'Data Type': df[columns_to_drop].dtypes,
    'Unique Values': [df[col].unique() if df[col].dtype == 'object' else None for col in columns_to_drop]
})

# Drop rows with more than 10% missing values
row_threshold = 0.1
rows_to_drop = df_dropped_columns.isnull().mean(axis=1) > row_threshold
df_dropped_rows = df_dropped_columns[~rows_to_drop]
dropped_rows = df_dropped_columns[rows_to_drop]

# Save the resulting dataframes to CSV files
dropped_columns_matrix.to_csv('./dropped_columns_matrix.csv', index=False)
dropped_rows.to_csv('./dropped_rows.csv', index=False)
df_dropped_rows.to_csv('./data_preprocessed_v2.csv', index=False)

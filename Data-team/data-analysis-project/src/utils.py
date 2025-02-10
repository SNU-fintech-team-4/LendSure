def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def summarize_data(df):
    return {
        'columns': df.columns.tolist(),
        'shape': df.shape,
        'info': df.info(),
        'description': df.describe(include='all')
    }
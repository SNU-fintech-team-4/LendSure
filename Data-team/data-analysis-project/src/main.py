import pandas as pd
from zip_code_mapping import zip_code_mapping
from addr_state_mapping import addr_state_mapping

def main():
    # Define the path to the CSV file
    csv_file_path = '/Users/hyunbin/Library/CloudStorage/OneDrive-Personal/05 빅데이터 전문가 과정/01 통계 데이터 사이언스/00 팀플/ori-analysis-project/ori/data_preprocessed_v1.csv'
    
    # Read the CSV file
    data = pd.read_csv(csv_file_path)
    
    # Specify the columns to keep
    columns_to_keep = [
        'grade', 'sub_grade', 'emp_title', 'emp_length', 
        'home_ownership', 'verification_status', 'loan_status', 
        'purpose', 'zip_code', 'addr_state', 
        'earliest_cr_line', 'initial_list_status', 
        'debt_settlement_flag'
    ]
    
    # Drop all columns except the specified ones
    filtered_data = data[columns_to_keep]
    
    # Create a DataFrame to store the unique values, their counts, and proportions
    unique_values_info = []

    for column in columns_to_keep:
        value_counts = filtered_data[column].value_counts()
        total_count = len(filtered_data)
        for value, count in value_counts.items():
            proportion = count / total_count
            unique_values_info.append([column, value, count, proportion])
    
    unique_values_df = pd.DataFrame(unique_values_info, columns=['Column', 'Value', 'Count', 'Proportion'])
    
    # Save the unique values information to a CSV file
    unique_values_file_path = '/Users/hyunbin/Library/CloudStorage/OneDrive-Personal/05 빅데이터 전문가 과정/01 통계 데이터 사이언스/00 팀플/ori-analysis-project/ori/unique_values_info.csv'
    unique_values_df.to_csv(unique_values_file_path, index=False)
    
    # Save each column's unique values to separate sheets in an Excel file
    with pd.ExcelWriter('/Users/hyunbin/Library/CloudStorage/OneDrive-Personal/05 빅데이터 전문가 과정/01 통계 데이터 사이언스/00 팀플/ori-analysis-project/ori/unique_values_info.xlsx') as writer:
        for column in columns_to_keep:
            column_data = unique_values_df[unique_values_df['Column'] == column].copy()
            if column == 'addr_state':
                column_data['Name'] = column_data['Value'].apply(
                    lambda x: addr_state_mapping[x] if x in addr_state_mapping else None
                )
            elif column == 'zip_code':
                column_data['Name'] = column_data['Value'].apply(
                    lambda x: zip_code_mapping[x] if x in zip_code_mapping else None
                )
            column_data.to_excel(writer, sheet_name=column, index=False)

if __name__ == "__main__":
    main()
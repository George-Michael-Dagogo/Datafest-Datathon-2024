import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_collection import dim_class_resources



# Data quality checks
def data_quality_checks(df):
    # Check for missing/null values
    if df.isnull().values.any():
        raise ValueError("Data contains null values")

    # Check if columns have correct data types
    if not pd.api.types.is_string_dtype(df['Class_ID']):
        raise ValueError("Class_ID should be a string")

    if not pd.api.types.is_numeric_dtype(df['Number_of_Students']):
        raise ValueError("Number_of_Students should be numeric")

    if not pd.api.types.is_numeric_dtype(df['Number_of_Teachers']):
        raise ValueError("Number_of_Teachers should be numeric")

    # Check for non-negative values in numerical columns
    numerical_columns = ['Number_of_Students', 'Number_of_Teachers', 'Weekly_Teaching_Hours',
                         'Weekly_Library_Time', 'Weekly_Computer_Training_Time', 'Weekly_Lab_Hours',
                         'Chalkboard', 'Basic_Textbooks', 'Chairs_Desks', 'Functional_Fans']
    
    for col in numerical_columns:
        if (df[col] < 0).any():
            raise ValueError(f"{col} contains negative values")

    # Check that number of chairs/desks is not less than number of students
    if (df['Chairs_Desks'] < df['Number_of_Students']).any():
        raise ValueError("Number of Chairs_Desks should be at least equal to Number_of_Students")

    # If all checks pass
    return True

# Perform data quality checks
if data_quality_checks(dim_class_resources):
    # Save DataFrame as parquet if all checks pass
    table = pa.Table.from_pandas(dim_class_resources)
    pq.write_table(table, 'class_resources_table.parquet')
    print("Data quality checks passed and data saved as parquet.")

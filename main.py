import os
# Run data quality script that triggers the data collection script
# os.system('python ./initial_data_flow/data_quality_to_parquet.py')

# os.system('python ./initial_data_flow/data_integration.py')



os.system('python ./subsequent_data_flow/data_quality_to_parquet.py')

os.system('python ./subsequent_data_flow/data_push_to_blob.py')

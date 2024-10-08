import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()


def push_to_blob():
    # Access the variables
    connection_string = os.getenv("CONNECTION_STRING")
    container_name = 'testtech'

    # Create the BlobServiceClient object which will be used to interact with Blob storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create the container client to interact with the container
    container_client = blob_service_client.get_container_client(container_name)

    # Function to determine the current quarter
    def get_current_quarter_and_date():
        current_month = datetime.now().month
        quarter = f"Q{(current_month - 1) // 3 + 1}"
        current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        return f"{quarter}_{current_date}"

    # Create the new folder name
    new_folder_name = get_current_quarter_and_date()

    # Define the directory where the parquet files are stored
    parquet_folder_path = './passed_basic_quality_checks'

    # Upload each file to the Blob storage container
    for filename in os.listdir(parquet_folder_path):
        if filename.endswith('.parquet'):
            file_path = os.path.join(parquet_folder_path, filename)
            
            # Create a blob client using the folder name and local file name as the name for the blob
            blob_client = container_client.get_blob_client(blob=os.path.join(new_folder_name, filename))
            
            # Open the file and upload its contents to Blob storage
            with open(file_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"Uploaded {filename} to Blob Storage in folder: {new_folder_name}")


push_to_blob()
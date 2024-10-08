import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()
# Access the variables

database_url = os.getenv("DATABASE_URL")


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




def push_to_database():    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    # Function to execute a raw SQL command
    def execute_sql(sql):
        cursor.execute(sql)
        conn.commit()

    # Function to create tables
    def create_tables():
        # Create class_resources_table
        execute_sql('''
            -- class_resources_table (with Class_ID as the primary key)
    CREATE TABLE IF NOT EXISTS class_resources_table (  
        Class_ID VARCHAR(20) PRIMARY KEY,
        Number_of_Students SMALLINT,
        Number_of_Teachers SMALLINT,
        Weekly_Teaching_Hours SMALLINT,
        Weekly_Library_Time SMALLINT,
        Weekly_Computer_Training_Time SMALLINT,
        Weekly_Lab_Hours SMALLINT,
        Chalkboard SMALLINT,
        Basic_Textbooks SMALLINT,
        Chairs_Desks SMALLINT,
        Functional_Fans SMALLINT
    );

    -- student_table (with Class_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS student_table (
        Student_ID VARCHAR(100) PRIMARY KEY,  -- Primary key for student_table
        Class_ID VARCHAR(20),  -- Foreign key to class_resources_table
        First_Name TEXT,
        Family_Name TEXT,
        Gender TEXT,
        Date_of_Birth DATE NOT NULL,
        State_of_Origin TEXT, 
        engagement_in_class TEXT,
        health_condition TEXT,
        Class_Spec TEXT,
        FOREIGN KEY (Class_ID) REFERENCES class_resources_table(Class_ID)  -- Foreign key to class_resources_table
    );


    -- parent_table (with Student_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS parent_table (
        Student_ID VARCHAR(100)PRIMARY KEY,  -- Using Student_ID as the primary key
        Fathers_Name TEXT,
        Mothers_Name TEXT,
        Family_Name TEXT,
        Father_Education TEXT,
        Mother_Education TEXT,
        Father_Occupation TEXT,
        Mother_Occupation TEXT,
        Annual_Household_Income_NGN TEXT,
        Household_Size INTEGER,
        Involvement_in_Kids_Education TEXT,
        FOREIGN KEY (Student_ID) REFERENCES student_table(Student_ID)  -- Foreign key to student_table
    );

    -- extracurricular_activity (with Student_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS extracurricular_activity (
        Student_ID VARCHAR(100) PRIMARY KEY,  -- Using Student_ID as the primary key
        Extracurricular_Activity TEXT,
        Weekly_Hours INTEGER,
        FOREIGN KEY (Student_ID) REFERENCES student_table(Student_ID)  -- Foreign key to student_table
    );

    -- student_performance (with Student_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS student_performance (
        Student_ID VARCHAR(100) PRIMARY KEY,  -- Using Student_ID as the primary key
        Mathematics INTEGER,
        English_Language INTEGER,
        Civic_Education INTEGER,
        Economics INTEGER,
        CRS_Islam INTEGER,
        Physics FLOAT,
        Chemistry FLOAT,
        Biology FLOAT,
        Geography FLOAT,
        Computer_Science FLOAT,
        Government FLOAT,
        Commerce FLOAT,
        Literature FLOAT,
        History FLOAT,
        Accounting FLOAT,
        FOREIGN KEY (Student_ID) REFERENCES student_table(Student_ID)  -- Foreign key to student_table
    );

    -- attendance_table (with Student_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS attendance_table (
        Student_ID VARCHAR(100) PRIMARY KEY,  -- Using Student_ID as the primary key
        Days_Attended INTEGER,
        Days_Missed INTEGER,
        Absence_Reason TEXT,
        FOREIGN KEY (Student_ID) REFERENCES student_table(Student_ID)  -- Foreign key to student_table
    );

    -- ss3_student_survey (with Student_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS ss3_student_survey (
        Student_ID VARCHAR(100) PRIMARY KEY,  -- Using Student_ID as the primary key
        Reason_For_Performance TEXT,
        Access_To_Resources TEXT,
        Study_Hours_Per_Week INTEGER,
        Health_Issues TEXT,
        Teacher_Support INTEGER,
        Parental_Support INTEGER,
        Stress_Level TEXT,
        Peer_Influence TEXT,
        Additional_Tutoring TEXT,
        Use_Of_Study_Groups TEXT,
        Exam_Anxiety TEXT,
        Jamb_Scores SMALLINT,
        Num_Credit_Passes_WAEC SMALLINT,
        Verdict TEXT,
        FOREIGN KEY (Student_ID) REFERENCES student_table(Student_ID)  -- Foreign key to student_table
    );

    -- staff_table (with Staff_ID as the primary key)
    CREATE TABLE IF NOT EXISTS staff_table (
        Staff_ID VARCHAR(100) PRIMARY KEY,  -- Primary key for staff_table
        Name TEXT,
        Gender TEXT,
        Position TEXT,
        Monthly_Pay INTEGER,
        Years_of_Experience INTEGER,
        Education_Level TEXT,
        Date_of_Hire TEXT,
        Full_time BOOLEAN
    );

    -- teachers_table (with Staff_ID as a foreign key)
    CREATE TABLE IF NOT EXISTS teachers_table (
        Teacher_ID VARCHAR(100)PRIMARY KEY,  -- Primary key for teachers_table
        Staff_ID VARCHAR(100),  -- Foreign key to staff_table
        Name TEXT,
        Teacher_Type TEXT,
        Subject_specialization TEXT,
        FOREIGN KEY (Staff_ID) REFERENCES staff_table(Staff_ID)  -- Foreign key to staff_table
    );


        ''')

        # Repeat similar for other tables (extracurricular_activity, staff_table, etc.)


    # Function to load data from parquet and insert into PostgreSQL table
    def load_data_from_parquet(table_name, parquet_file):
        # Load the parquet file into a pandas DataFrame
        df = pd.read_parquet(parquet_file)
        
        # Generate the INSERT query dynamically based on the DataFrame's column names
        columns = ', '.join(df.columns)
        values = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        
        # Insert rows into the table
        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)
        
        conn.commit()
        print(f"Data loaded into {table_name} from {parquet_file}")

    # List of tables and corresponding Parquet filenames
    table_files = {
        "class_resources_table": "class_resources_table.parquet",
        "student_table": "student_table.parquet",
        "parent_table": "parent_table.parquet",
        "extracurricular_activity": "extracurricular_activity.parquet",
        "staff_table": "staff_table.parquet",
        "teachers_table": "teachers_table.parquet",
        "student_performance": "student_performance.parquet",
        "attendance_table": "attendance_table.parquet",
        "ss3_student_survey": "ss3_student_survey.parquet"
    }

    # Create all the tables (assuming you have a `create_tables()` function already defined)
    create_tables()

    # Directory where parquet files are stored
    parquet_folder_path = './passed_basic_quality_checks'

    # Loop through each table and load the corresponding parquet data
    for table_name, parquet_file in table_files.items():
        parquet_path = os.path.join(parquet_folder_path, parquet_file)
        load_data_from_parquet(table_name, parquet_path)

    # Close the connection after loading data
    cursor.close()
    conn.close()


#push_to_blob()
push_to_database()
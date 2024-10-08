import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)

# Load environment variables from .env file
load_dotenv()
# Access the variables

database_url = os.getenv("DATABASE_URL")
# Function to hash passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Function to check hashed passwords
def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# Function to create a login session
def login_user(username, password):
    if username == "datafest_school" and check_hashes(password, make_hashes("datafest_school")):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        return True
    else:
        return False

# Function to log out
def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None

def generate_student_id():
    # Generate a random 8-digit number
    student_id = fake.unique.uuid4().replace('-','')

    
    return student_id

# Function to fetch a student record
def fetch_student_data(student_id):
    try:
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        select_query = "SELECT * FROM student_table WHERE student_id = %s"
        cursor.execute(select_query, (student_id,))
        student_data = cursor.fetchone()

        return student_data

    except (Exception, Error) as e:
        st.error(f"Error while fetching student data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to update student data
def update_student_data(student_id, first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec):
    try:
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        update_query = """UPDATE student_table 
                          SET First_Name = %s, Family_Name = %s, Gender = %s, Date_of_Birth = %s, 
                              State_of_Origin = %s, engagement_in_class = %s, health_condition = %s, Class_Spec = %s
                          WHERE Student_ID = %s"""
        cursor.execute(update_query, (first_name, family_name, gender, date_of_birth, state_of_origin, 
                                      engagement_in_class, health_condition, class_spec, student_id))
        connection.commit()
        st.success("Student data successfully updated in the PostgreSQL database")

    except (Exception, Error) as e:
        st.error(f"Error while updating student data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def insert_student_data(first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec):

    try:
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()
        student_id = generate_student_id()
        insert_query = """INSERT INTO student_table (student_id, First_Name, Family_Name, Gender, Date_of_Birth, State_of_Origin, engagement_in_class, health_condition, Class_Spec) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (student_id,first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec))
        connection.commit()
        st.success("Student data successfully inserted into the PostgreSQL database")

    except (Exception, Error) as e:
        st.error(f"Error while connecting to PostgreSQL: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to insert parent data into PostgreSQL
def insert_parent_data(student_id, father_name, mother_name, family_name, father_education, mother_education, father_occupation, mother_occupation):
    try:
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        insert_query = """INSERT INTO parent_table (Student_ID, Fathers_Name, Mothers_Name, Family_Name, Father_Education, Mother_Education, Father_Occupation, Mother_Occupation) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (student_id, father_name, mother_name, family_name, father_education, mother_education, father_occupation, mother_occupation))
        connection.commit()
        st.success("Parent data successfully inserted into the PostgreSQL database")

    except (Exception, Error) as e:
        st.error(f"Error while connecting to PostgreSQL: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to insert staff data into PostgreSQL
def insert_staff_data(staff_name, gender, position, monthly_pay, years_of_experience, education_level, date_of_hire, full_time):
    try:
        connection = psycopg2.connect(database_url)
        cursor = connection.cursor()

        insert_query = """INSERT INTO staff_table (staff_id,Name, Gender, Position, Monthly_Pay, Years_of_Experience, Education_Level, Date_of_Hire, Full_time) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (staff_id ,staff_name, gender, position, monthly_pay, years_of_experience, education_level, date_of_hire, full_time))
        connection.commit()
        st.success("Staff data successfully inserted into the PostgreSQL database")

    except (Exception, Error) as e:
        st.error(f"Error while connecting to PostgreSQL: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


# [Add similar fetch and update functions for parent and staff data]

def main():
    st.title("Datafest School Database Management")

       # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    # Sidebar for login/logout
    with st.sidebar:
        if not st.session_state['logged_in']:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                if login_user(username, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password")
        else:
            st.subheader(f"Welcome, {st.session_state['username']}!")
            if st.button("Logout"):
                logout_user()
                st.rerun()


    if st.session_state['logged_in']:
        # Sidebar Navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Choose a page", ["Student Data Entry", "Parent Data Entry", "Staff Data Entry", 
                                                      "Update Student Data", "Update Parent Data", "Update Staff Data"])

        
        # Page 1: Student Data Entry
        if page == "Student Data Entry":
            st.title("Student Data Entry Form")

            # Student input fields
            
            first_name = st.text_input("First Name")
            family_name = st.text_input("Family Name")
            gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
            date_of_birth = st.date_input("Date of Birth")
            state_of_origin = st.text_input("State of Origin")
            engagement_in_class = st.text_input("Engagement in Class")
            health_condition = st.text_input("Health Condition")
            class_spec = st.selectbox("Class Spec", options=['SS1 Class D', 'SS1 Class C', 'SS3 Class F', 'SS1 Class E','SS2 Class E', 'SS2 Class A', 'SS2 Class B', 'SS3 Class A','SS1 Class B', 'SS2 Class D', 'SS3 Class C', 'SS1 Class F','SS3 Class D', 'SS3 Class B', 'SS3 Class E', 'SS2 Class C','SS1 Class A', 'SS2 Class F'])

            if st.button("Submit Student Data"):
                if first_name and family_name and gender and date_of_birth and state_of_origin and engagement_in_class and health_condition and class_spec:
                    insert_student_data(student_id,first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec)
                else:
                    st.error("Please fill in all fields")

        # Page 2: Parent Data Entry
        elif page == "Parent Data Entry":
            st.title("Parent Data Entry Form")

            # Parent input fields
            student_id = st.text_input("Student ID")
            father_name = st.text_input("Father's Name")
            mother_name = st.text_input("Mother's Name")
            family_name = st.text_input("Family Name")
            father_education = st.text_input("Father's Education")
            mother_education = st.text_input("Mother's Education")
            father_occupation = st.text_input("Father's Occupation")
            mother_occupation = st.text_input("Mother's Occupation")

            if st.button("Submit Parent Data"):
                if student_id and father_name and mother_name and family_name and father_education and mother_education and father_occupation and mother_occupation:
                    insert_parent_data(student_id, father_name, mother_name, family_name, father_education, mother_education, father_occupation, mother_occupation)
                else:
                    st.error("Please fill in all fields")

        # Page 3: Staff Data Entry
        elif page == "Staff Data Entry":
            st.title("Staff Data Entry Form")

            # Staff input fields
            staff_name = st.text_input("Staff Name")
            gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
            position = st.text_input("Position")
            monthly_pay = st.number_input("Monthly Pay", min_value=0)
            years_of_experience = st.number_input("Years of Experience", min_value=0)
            education_level = st.text_input("Education Level")
            date_of_hire = st.date_input("Date of Hire")
            full_time = st.selectbox("Full-time", options=[True, False])

            if st.button("Submit Staff Data"):
                if staff_name and gender and position and monthly_pay and years_of_experience and education_level and date_of_hire:
                    insert_staff_data(staff_name, gender, position, monthly_pay, years_of_experience, education_level, date_of_hire, full_time)
                else:
                    st.error("Please fill in all fields")

        elif page == "Update Student Data":
            st.title("Update Student Data")
            student_id = st.text_input("Enter Student ID to update")
            if st.button("Fetch Student Data"):
                student_data = fetch_student_data(student_id)
                if student_data:
                    st.session_state['student_data'] = student_data
                    st.success("Student data fetched successfully")
                else:
                    st.error("No student found with the given ID")

            if 'student_data' in st.session_state:
                student = st.session_state['student_data']
                class_id = st.text_input("Class ID", value=student[1])
                first_name = st.text_input("First Name", value=student[2])
                family_name = st.text_input("Family Name", value=student[3])
                gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(student[4]))
                date_of_birth = st.date_input("Date of Birth", value=student[5])
                state_of_origin = st.text_input("State of Origin", value=student[6])
                engagement_in_class = st.text_input("Engagement in Class", value=student[7])
                health_condition = st.text_input("Health Condition", value=student[8])
                class_spec = st.text_input("Class Spec", value=student[9])

                if st.button("Update Student Data"):
                    update_student_data(class_id, first_name, family_name, gender, date_of_birth, state_of_origin, 
                                        engagement_in_class, health_condition, class_spec)

        # [Add similar update pages for Parent and Staff data]

if __name__ == '__main__':
    main()
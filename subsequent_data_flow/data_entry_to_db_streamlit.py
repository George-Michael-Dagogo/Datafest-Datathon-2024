import streamlit as st
import psycopg2
from psycopg2 import Error

# Authentication variables
correct_username = "datafest_school"
correct_password = "datafest_school"

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Authentication block
if not st.session_state['logged_in']:
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == correct_username and password == correct_password:
            st.session_state['logged_in'] = True
            st.success("Login successful")
            # Trigger a rerun by setting a query parameter 
        else:
            st.error("Incorrect username or password")

# If logged in, show the app
if st.session_state['logged_in']:
    # Function to insert student data into PostgreSQL
    def insert_student_data(first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec):
        try:
            connection = psycopg2.connect(
                host='your_database_host',
                database='your_database_name',
                user='your_db_user',
                password='your_db_password',
                port='your_db_port'
            )
            cursor = connection.cursor()

            insert_query = """INSERT INTO student_table (First_Name, Family_Name, Gender, Date_of_Birth, State_of_Origin, engagement_in_class, health_condition, Class_Spec) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec))
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
            connection = psycopg2.connect(
                host='your_database_host',
                database='your_database_name',
                user='your_db_user',
                password='your_db_password',
                port='your_db_port'
            )
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
            connection = psycopg2.connect(
                host='your_database_host',
                database='your_database_name',
                user='your_db_user',
                password='your_db_password',
                port='your_db_port'
            )
            cursor = connection.cursor()

            insert_query = """INSERT INTO staff_table (Name, Gender, Position, Monthly_Pay, Years_of_Experience, Education_Level, Date_of_Hire, Full_time) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (staff_name, gender, position, monthly_pay, years_of_experience, education_level, date_of_hire, full_time))
            connection.commit()
            st.success("Staff data successfully inserted into the PostgreSQL database")

        except (Exception, Error) as e:
            st.error(f"Error while connecting to PostgreSQL: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Student Data Entry", "Parent Data Entry", "Staff Data Entry"])

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
        class_spec = st.text_input("Class Spec")

        if st.button("Submit Student Data"):
            if first_name and family_name and gender and date_of_birth and state_of_origin and engagement_in_class and health_condition and class_spec:
                insert_student_data(first_name, family_name, gender, date_of_birth, state_of_origin, engagement_in_class, health_condition, class_spec)
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




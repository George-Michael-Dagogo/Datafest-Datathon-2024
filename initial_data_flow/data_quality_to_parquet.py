import pandas as pd
from data_generation_collection import * 
# Load the data
attendance_df = fact_attendance
student_df = dim_student
class_resources_df = dim_class_resources
extracurricular_df = dim_extracurricular_activity
parent_df = dim_parent_demographics
survey_df = ss3_student_survey
staff_df = staff_table
performance_df = student_performance
teachers_df = teachers_table

def attendance_quality_checks():
    total_school_days = 95

    # 1. Check for null values in all columns
    if attendance_df.isnull().values.any():
        print("Null values found in the dataframe:\n", attendance_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Student_ID is unique and matches with student_table
    if not attendance_df['Student_ID'].is_unique:
        print("Duplicate Student_IDs found.")
    else:
        print("Student_ID is unique.")

    unmatched_ids = attendance_df[~attendance_df['Student_ID'].isin(student_df['Student_ID'])]
    if not unmatched_ids.empty:
        print(f"Unmatched Student_IDs found:\n{unmatched_ids['Student_ID'].values}")
    else:
        print("All Student_IDs match with student_table.")

    # 3. Verify Days_Attended and Days_Missed are non-negative
    if (attendance_df['Days_Attended'] < 0).any() or (attendance_df['Days_Missed'] < 0).any():
        print("Found negative values in Days_Attended or Days_Missed.")
    else:
        print("Days_Attended and Days_Missed are non-negative.")

    # 4. Check if Days_Attended + Days_Missed equals total school days
    if (attendance_df['Days_Attended'] + attendance_df['Days_Missed'] != total_school_days).any():
        mismatches = attendance_df[attendance_df['Days_Attended'] + attendance_df['Days_Missed'] != total_school_days]
        print(f"Mismatches found:\n{mismatches[['Student_ID', 'Days_Attended', 'Days_Missed']]}")
    else:
        print("Days_Attended + Days_Missed matches total school days.")

    # 5. Ensure Absence_Reason is filled for all records where Days_Missed > 0
    missing_reasons = attendance_df[(attendance_df['Days_Missed'] > 0) & (attendance_df['Absence_Reason'].isnull())]
    if not missing_reasons.empty:
        print(f"Absence_Reason missing for records where Days_Missed > 0:\n{missing_reasons[['Student_ID', 'Days_Missed']]}")
    else:
        print("Absence_Reason is filled for all records where Days_Missed > 0.")

    # Save to parquet if all checks pass
    if (attendance_df.isnull().values.any() == False and
        attendance_df['Student_ID'].is_unique and
        unmatched_ids.empty and
        (attendance_df['Days_Attended'] >= 0).all() and
        (attendance_df['Days_Missed'] >= 0).all() and
        (attendance_df['Days_Attended'] + attendance_df['Days_Missed'] == total_school_days).all() and
        missing_reasons.empty):
        
        attendance_df.to_parquet('./passed_basic_quality_checks/attendance_table.parquet')
        print("All attendance data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")




def class_resources_quality_checks():
    # 1. Check for null values in all columns
    if class_resources_df.isnull().values.any():
        print("Null values found in the dataframe:\n", class_resources_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Class_ID is unique
    if not class_resources_df['Class_ID'].is_unique:
        print("Duplicate Class_IDs found.")
    else:
        print("Class_ID is unique.")

    # 3. Verify all numeric columns have non-negative values
    numeric_columns = ['Number_of_Students', 'Number_of_Teachers', 'Weekly_Teaching_Hours', 
                    'Weekly_Library_Time', 'Weekly_Computer_Training_Time', 'Weekly_Lab_Hours',
                    'Chalkboard', 'Basic_Textbooks', 'Chairs_Desks', 'Functional_Fans']

    if (class_resources_df[numeric_columns] < 0).any().any():
        print("Found negative values in numeric columns.")
    else:
        print("All numeric columns have non-negative values.")

    # 4. Check if Number_of_Students and Number_of_T are reasonable
    if class_resources_df['Number_of_Students'].max() > 100 or class_resources_df['Number_of_Teachers'].max() > 20:
        print("Unreasonable values in Number_of_Students or Number_of_Teachers.")
    else:
        print("Number_of_Students and Number_of_Teachers are within reasonable limits.")

    # 5. Ensure Weekly_Teaching_Hours is within a realistic range (e.g., 20-50 hours)
    if not class_resources_df['Weekly_Teaching_Hours'].between(20, 50).all():
        print("Weekly_Teaching_Hours not within realistic range (20-50 hours).")
    else:
        print("Weekly_Teaching_Hours is within realistic range.")



    # Save to parquet if all checks pass
    if (class_resources_df.isnull().values.any() == False and
        class_resources_df['Class_ID'].is_unique and
        (class_resources_df[numeric_columns] >= 0).all().all() and
        class_resources_df['Number_of_Students'].max() <= 100 and
        class_resources_df['Number_of_Teachers'].max() <= 20 and
        class_resources_df['Weekly_Teaching_Hours'].between(20, 50).all()):
        
        class_resources_df.to_parquet('./passed_basic_quality_checks/class_resources_table.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")




def extracurricular_activities_data_checks():
    # 1. Check for null values in all columns
    if extracurricular_df.isnull().values.any():
        print("Null values found in the dataframe:\n", extracurricular_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Student_ID exists in student_table
    missing_students = extracurricular_df[~extracurricular_df['Student_ID'].isin(student_df['Student_ID'])]
    if not missing_students.empty:
        print("Student_ID(s) missing in student_table:\n", missing_students['Student_ID'].unique())
    else:
        print("All Student_IDs exist in student_table.")

    # 3. Verify Weekly_Hours is non-negative and within a realistic range (0-20 hours)
    if not extracurricular_df['Weekly_Hours'].between(0, 20).all():
        print("Weekly_Hours not in the realistic range (0-20 hours) or contains negative values.")
    else:
        print("Weekly_Hours is within a realistic range (0-20 hours) and non-negative.")

    # Save to parquet if all checks pass
    if (extracurricular_df.isnull().values.any() == False and
        missing_students.empty and
        extracurricular_df['Weekly_Hours'].between(0, 20).all()):
        
        extracurricular_df.to_parquet('./passed_basic_quality_checks/extracurricular_activity.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")




def parent_data_quality_checks():
    # 1. Check for null values in all columns
    if parent_df.isnull().values.any():
        print("Null values found:\n", parent_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Student_ID is unique and matches with student_table
    duplicate_student_ids = parent_df['Student_ID'].duplicated().sum()
    if duplicate_student_ids > 0:
        print(f"Found {duplicate_student_ids} duplicate Student_IDs.")
    else:
        print("All Student_IDs are unique.")

    missing_students = parent_df[~parent_df['Student_ID'].isin(student_df['Student_ID'])]
    if not missing_students.empty:
        print("Student_ID(s) missing in student_table:\n", missing_students['Student_ID'].unique())
    else:
        print("All Student_IDs exist in student_table.")

    # 3. Verify Household_Size is positive and within a realistic range (e.g., 1-15)
    if not parent_df['Household_Size'].between(1, 15).all():
        print("Household_Size contains values outside the realistic range (1-15).")
    else:
        print("Household_Size is within the realistic range.")

    # 4. Check if Annual_Household_Income(NGN) is valid
    valid_income_ranges = ['Below 200,000', '200,000-400,000', '400,000-600,000', 'Above 600,000']
    if not parent_df['Annual_Household_Income_NGN'].isin(valid_income_ranges).all():
        print("Invalid values found in Annual_Household_Income(NGN).")
    else:
        print("Annual_Household_Income(NGN) has valid values.")

    # 5. Ensure Father_Education, Mother_Education, Father_Occupation, Mother_Occupation, and Involvement_in_Kids_Education have consistent categories
    consistent_columns = ['Father_Education', 'Mother_Education', 'Father_Occupation', 'Mother_Occupation', 'Involvement_in_Kids_Education']
    for col in consistent_columns:
        print(f"Unique values in {col}:\n", parent_df[col].unique())

    # Save to parquet if all checks pass
    if (parent_df.isnull().values.any() == False and
        duplicate_student_ids == 0 and
        missing_students.empty and
        parent_df['Household_Size'].between(1, 15).all() and
        parent_df['Annual_Household_Income_NGN'].isin(valid_income_ranges).all()):
        
        parent_df.to_parquet('./passed_basic_quality_checks/parent_table.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")



def survey_data_quality():
    # 1. Check for null values in all columns
    if survey_df.isnull().values.any():
        print("Null values found:\n", survey_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Student_ID is unique and matches with student_table
    if survey_df['Student_ID'].duplicated().any():
        print("Duplicate Student_IDs found.")
    else:
        print("All Student_IDs are unique.")

    missing_students_survey = survey_df[~survey_df['Student_ID'].isin(student_df['Student_ID'])]
    if not missing_students_survey.empty:
        print("Student_ID(s) missing in student_table:\n", missing_students_survey['Student_ID'].unique())
    else:
        print("All Student_IDs exist in student_table.")

    # 3. Verify Study_Hours_Per_Week is non-negative and within a realistic range (0-50)
    if not survey_df['Study_Hours_Per_Week'].between(0, 50).all():
        print("Study_Hours_Per_Week contains values outside the realistic range (0-50).")
    else:
        print("Study_Hours_Per_Week is within the realistic range.")

    # 4. Check if Teacher_Support and Parental_Support are within a specific range (1-5)
    support_cols = ['Teacher_Support', 'Parental_Support']
    for col in support_cols:
        if not survey_df[col].between(1, 5).all():
            print(f"{col} contains values outside the range 1-5.")
        else:
            print(f"{col} is within the range 1-5.")

    # 5. Ensure Stress_Level has consistent categories
    print("Unique values in Stress_Level:", survey_df['Stress_Level'].unique())

    # 6. Verify Jamb_Scores and Num_Credit_Passes_WAEC are within expected ranges
    if not survey_df['Jamb_Scores'].between(0, 400).all():
        print("Jamb_Scores contain values outside the expected range (0-400).")
    else:
        print("Jamb_Scores are within the expected range.")

    if not survey_df['Num_Credit_Passes_WAEC'].between(0, 9).all():
        print("Num_Credit_Passes_WAEC contains values outside the expected range (0-9).")
    else:
        print("Num_Credit_Passes_WAEC is within the expected range.")

    # 7. Check if verdict has consistent categories
    print("Unique values in verdict:", survey_df['verdict'].unique())

    # Save to parquet if all checks pass
    if (survey_df.isnull().values.any() == False and
        not survey_df['Student_ID'].duplicated().any() and
        missing_students_survey.empty and
        survey_df['Study_Hours_Per_Week'].between(0, 50).all() and
        survey_df[support_cols].apply(lambda x: x.between(1, 5).all()).all() and
        survey_df['Jamb_Scores'].between(0, 400).all() and
        survey_df['Num_Credit_Passes_WAEC'].between(0, 9).all()):
        
        survey_df.to_parquet('./passed_basic_quality_checks/ss3_student_survey.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")


def staff_data_quality():
    # 1. Check for null values in all columns
    if staff_df.isnull().values.any():
        print("Null values found:\n", staff_df.isnull().sum())
    else:
        print("No null values found.")

    # 2. Ensure Staff_ID is unique
    if staff_df['Staff_ID'].duplicated().any():
        print("Duplicate Staff_IDs found.")
    else:
        print("All Staff_IDs are unique.")

    # 3. Verify Monthly Pay and Years of Experience are non-negative
    if (staff_df[['Monthly_Pay', 'Years_of_Experience']] < 0).any().any():
        print("Monthly Pay or Years of Experience contains negative values.")
    else:
        print("Monthly Pay and Years of Experience are non-negative.")

    # 4. Check if Date of Hire is in a consistent date format and not in the future
    staff_df['Date_of_Hire'] = pd.to_datetime(staff_df['Date_of_Hire'], errors='coerce')
    future_dates = staff_df[staff_df['Date_of_Hire'] > pd.Timestamp.now()]
    if not future_dates.empty:
        print("Future Date of Hire values found:\n", future_dates['Date_of_Hire'])
    else:
        print("All Date of Hire values are valid.")

    # 5. Ensure Gender, Position, and Education Level have consistent categories
    print("Unique values in Gender:", staff_df['Gender'].unique())
    print("Unique values in Position:", staff_df['Position'].unique())
    print("Unique values in Education Level:", staff_df['Education_Level'].unique())

    # Save to parquet if all checks pass
    if (staff_df.isnull().values.any() == False and
        not staff_df['Staff_ID'].duplicated().any() and
        not (staff_df[['Monthly_Pay', 'Years_of_Experience']] < 0).any().any() and
        future_dates.empty):
        
        staff_df.to_parquet('./passed_basic_quality_checks/staff_table.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")



def performance_data_quality():

    # 1. Check for null values in relevant columns
    if performance_df[['Mathematics', 'English_Language', 'Civic_Education', 'Economics', 'CRS_Islam']].isnull().any().any():
        print("Null values found in key columns:\n", performance_df[['Mathematics', 'English Language', 'Civic Education', 'Economics', 'CRS_Islam']].isnull().sum())
    else:
        print("No null values found in the relevant columns.")

    # 2. Ensure Student_ID is unique and matches with student_table
    if performance_df['Student_ID'].duplicated().any():
        print("Duplicate Student_IDs found.")
    else:
        print("All Student_IDs are unique.")

    # Check if Student_IDs exist in student_table
    missing_students_perf = performance_df[~performance_df['Student_ID'].isin(student_df['Student_ID'])]
    if not missing_students_perf.empty:
        print("Student_ID(s) missing in student_table:\n", missing_students_perf['Student_ID'].unique())
    else:
        print("All Student_IDs exist in student_table.")

    # 3. Verify that scores for 'Mathematics', 'English Language', 'Civic Education', 'Economics', 'CRS_Islam' are within the expected range (0-100)
    columns_to_check = ['Mathematics', 'English_Language', 'Civic_Education', 'Economics', 'CRS_Islam']
    valid_scores = performance_df[columns_to_check].apply(lambda x: x.between(0, 100) | x.isna()).all()
    if not valid_scores.all():
        print("Some scores are outside the expected range (0-100) in these columns:", valid_scores[~valid_scores].index.tolist())
    else:
        print("All non-null scores are within the expected range (0-100).")

    # 4. Check for any outliers in the scores (based on z-scores), ignoring NaN
    z_scores = (performance_df[columns_to_check] - performance_df[columns_to_check].mean()) / performance_df[columns_to_check].std()
    outliers = z_scores.abs() > 3  # Threshold for outliers (z-score > 3)
    if outliers.any().any():
        print("Outliers found in the following columns:\n", outliers.columns[outliers.any()])
    else:
        print("No significant outliers found.")

    # 5. Ignore NaN columns, ensure decimal places for float64 columns are consistent
    float_columns = performance_df[columns_to_check].select_dtypes(include=['float64']).columns
    if performance_df[float_columns].apply(lambda x: x.apply(lambda v: len(str(v).split('.')[-1]) if '.' in str(v) else 0).nunique() > 1).any():
        print("Inconsistent decimal places in float64 columns.")
    else:
        print("Decimal places are consistent in float64 columns.")

    # Save to parquet if all checks pass
    if (performance_df[['Mathematics', 'English_Language', 'Civic_Education', 'Economics', 'CRS_Islam']].isnull().any().any() == False and
        not performance_df['Student_ID'].duplicated().any() and
        missing_students_perf.empty and
        valid_scores.all() and
        not outliers.any().any()):


        
        performance_df.to_parquet('./passed_basic_quality_checks/student_performance.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")



def student_data_quality_checks():
    # 1. Check for null values in all columns
    if student_df.isnull().any().any():
        print("Null values found in the following columns:\n", student_df.isnull().sum())
    else:
        print("No null values found in any columns.")

    # 2. Ensure Student_ID is unique
    if student_df['Student_ID'].duplicated().any():
        print("Duplicate Student_IDs found.")
    else:
        print("All Student_IDs are unique.")

    # 3. Verify Class_ID exists in class_resources_table
    missing_class_ids = student_df[~student_df['Class_ID'].isin(class_resources_df['Class_ID'])]
    if not missing_class_ids.empty:
        print("Class_ID(s) missing in class_resources_table:\n", missing_class_ids['Class_ID'].unique())
    else:
        print("All Class_IDs exist in class_resources_table.")

    # 4. Check if Date_of_Birth is in a consistent date format and makes sense for a student
    # Assuming the format is 'YYYY-MM-DD'
    def check_date_format(date_str):
        try:
            return pd.to_datetime(date_str, format='%Y-%m-%d', errors='raise')
        except Exception:
            return None

    invalid_dates = student_df['Date_of_Birth'].apply(check_date_format).isnull()
    if invalid_dates.any():
        print("Invalid Date_of_Birth found:\n", student_df[invalid_dates]['Date_of_Birth'])
    else:
        print("All Date_of_Births are in a consistent format.")

    # 5. Ensure Gender, State of Origin, engagement_in_class, health_condition, and Class Spec have consistent categories
    # Example categories
    gender_categories = ['Male', 'Female']
    state_origin_categories = nigeria_states  
    engagement_categories = ['Troublesome','Unactive','Slightly active','Active','Highly active']
    health_condition_categories = health_condition
    class_spec_categories = ['Science', 'Art']  

    if not student_df['Gender'].isin(gender_categories).all():
        print("Inconsistent categories found in Gender column.")
    if not student_df['State_of_Origin'].isin(state_origin_categories).all():
        print("Inconsistent categories found in State of Origin column.")
    if not student_df['engagement_in_class'].isin(engagement_categories).all():
        print("Inconsistent categories found in engagement_in_class column.")
    if not student_df['health_condition'].isin(health_condition_categories).all():
        print("Inconsistent categories found in health_condition column.")
    if not student_df['Class_Spec'].isin(class_spec_categories).all():
        print("Inconsistent categories found in Class Spec column.")

    # Save to parquet if all checks pass
    if (not student_df.isnull().any().any() and
        not student_df['Student_ID'].duplicated().any() and
        missing_class_ids.empty and not invalid_dates.any()):
        
        student_df.to_parquet('./passed_basic_quality_checks/student_table.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")



def teacher_data_quality_checks():

    # 1. Check for null values in all columns
    if teachers_df.isnull().any().any():
        print("Null values found in the following columns:\n", teachers_df.isnull().sum())
    else:
        print("No null values found in any columns.")

    # 2. Ensure Teacher_ID is unique
    if teachers_df['Teacher_ID'].duplicated().any():
        print("Duplicate Teacher_IDs found.")
    else:
        print("All Teacher_IDs are unique.")

    # 3. Verify Staff_ID exists in staff_table
    missing_staff_ids = teachers_df[~teachers_df['Staff_ID'].isin(staff_df['Staff_ID'])]
    if not missing_staff_ids.empty:
        print("Staff_ID(s) missing in staff_table:\n", missing_staff_ids['Staff_ID'].unique())
    else:
        print("All Staff_IDs exist in staff_table.")

    # 4. Ensure Teacher Type and Subject specialization have consistent categories
    # Example categories
    teacher_type_categories = teacher_type  # Update as per your data
    subject_specialization_categories =subjects  # Update as per your data

    if not teachers_df['Teacher_Type'].isin(teacher_type_categories).all():
        print("Inconsistent categories found in Teacher Type column.")
    if not teachers_df['Subject_specialization'].isin(subject_specialization_categories).all():
        print("Inconsistent categories found in Subject specialization column.")

    # Save to parquet if all checks pass
    if (not teachers_df.isnull().any().any() and
        not teachers_df['Teacher_ID'].duplicated().any() and
        missing_staff_ids.empty):
        
        teachers_df.to_parquet('./passed_basic_quality_checks/teachers_table.parquet')
        print("All data quality checks passed. Data saved as Parquet.")
    else:
        print("Data quality checks failed.")

student_data_quality_checks()

performance_data_quality()

staff_data_quality()

survey_data_quality()

parent_data_quality_checks()

extracurricular_activities_data_checks()

class_resources_quality_checks()

attendance_quality_checks()

teacher_data_quality_checks()
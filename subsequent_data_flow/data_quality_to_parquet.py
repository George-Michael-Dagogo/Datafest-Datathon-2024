import pandas as pd
from data_extraction_from_db import * 

comon_subjects = ['mathematics', 'english_language', 'Civic_education', 'economics', 'CRS_Islam']
science_subjects = ['physics', 'Chemistry', 'Biology', 'Geography', 'Computer_Science']
art_subjects = ['Government', 'Comerce', 'literature','history', 'Accounting']
subjects = comon_subjects + science_subjects + art_subjects
health_condition = ['Asthma'] * 3 + ['Sickle Cel'] * 2 + ['Ulcer'] * 3 + ['epilepsy']*1 + ['Dyslexia']*20 + ['None']*91
teacher_type =  ['Corper','Regular']

nigeria_states = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
    "Borno", "Cross River", "Delta", "ebonyi", "edo", "ekiti", "enugu", "Gombe",
    "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
    "lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "plateau",
    "Rivers", "Sokoto", "Taraba", "yobe", "Zamfara", "FCT"
]

# load the data
atendance_df = attendance_table
student_df = student_data
class_resources_df = class_resources_table 
extracurricular_df = extracurricular_activity
parent_df = parent_table
survey_df = ss3_student_survey
staff_df = staff_table
performance_df = student_performance 
teachers_df = teachers_table


#student_id	class_id	first_name	family_name	gender	date_of_birth	state_of_origin	engagement_in_class	health_condition	class_spec
def atendance_quality_checks():
    total_school_days = 95

    # 1. check for nul values in all columns
    if atendance_df.isnull().values.any():
        print("Nul values found in the dataframe:\n", atendance_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure student_id is unique and matches with student_table
    if not atendance_df['student_id'].is_unique:
        print("duplicate student_ids found.")
    else:
        print("student_id is unique.")

    unmatched_ids = atendance_df[~atendance_df['student_id'].isin(student_df['student_id'])]
    if not unmatched_ids.empty:
        print(f"Unmatched student_ids found:\n{unmatched_ids['student_id'].values}")
    else:
        print("all student_ids match with student_table.")

    # 3. Verify days_attended and days_missed are non-negative
    if (atendance_df['days_attended'] < 0).any() or (atendance_df['days_missed'] < 0).any():
        print("found negative values in days_attended or days_missed.")
    else:
        print("days_attended and days_missed are non-negative.")

    # 4. check if days_attended + days_missed equals totall school days
    if (atendance_df['days_attended'] + atendance_df['days_missed'] != total_school_days).any():
        mismatches = atendance_df[atendance_df['days_attended'] + atendance_df['days_missed'] != total_school_days]
        print(f"mismatches found:\n{mismatches[['student_id', 'days_attended', 'days_missed']]}")
    else:
        print("days_attended + days_missed matches totall school days.")

    # 5. ensure absence_reason is filed for all records where days_missed > 0
    missing_reasons = atendance_df[(atendance_df['days_missed'] > 0) & (atendance_df['absence_reason'].isnull())]
    if not missing_reasons.empty:
        print(f"absence_reason missing for records where days_missed > 0:\n{missing_reasons[['student_id', 'days_missed']]}")
    else:
        print("absence_reason is filed for all records where days_missed > 0.")

    # Save to parquet if all checks pass
    if (atendance_df.isnull().values.any() == False and
        atendance_df['student_id'].is_unique and
        unmatched_ids.empty and
        (atendance_df['days_attended'] >= 0).all() and
        (atendance_df['days_missed'] >= 0).all() and
        (atendance_df['days_attended'] + atendance_df['days_missed'] == total_school_days).all() and
        missing_reasons.empty):
        
        atendance_df.to_parquet('./passed_basic_quality_checks/attendance_table.parquet')
        print("all atendance data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")




def class_resources_quality_checks():
    # 1. check for nul values in all columns
    if class_resources_df.isnull().values.any():
        print("Nul values found in the dataframe:\n", class_resources_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure class_id is unique
    if not class_resources_df['class_id'].is_unique:
        print("duplicate class_ids found.")
    else:
        print("class_id is unique.")

    # 3. Verify all numeric columns have non-negative values
    numeric_columns = ['number_of_students', 'number_of_teachers', 'weekly_teaching_hours', 
                    'weekly_library_time', 'weekly_computer_training_time', 'weekly_lab_hours',
                    'chalkboard', 'basic_textbooks', 'chairs_desks', 'functional_fans']

    if (class_resources_df[numeric_columns] < 0).any().any():
        print("found negative values in numeric columns.")
    else:
        print("all numeric columns have non-negative values.")

    # 4. check if number_of_students and Number_of_t are reasonable
    if class_resources_df['number_of_students'].max() > 100 or class_resources_df['number_of_teachers'].max() > 20:
        print("Unreasonable values in number_of_students or number_of_teachers.")
    else:
        print("number_of_students and number_of_teachers are within reasonable limits.")

    # 5. ensure weekly_teaching_hours is within a realistic range (e.g., 20-50 hours)
    if not class_resources_df['weekly_teaching_hours'].between(20, 50).all():
        print("weekly_teaching_hours not within realistic range (20-50 hours).")
    else:
        print("weekly_teaching_hours is within realistic range.")



    # Save to parquet if all checks pass
    if (class_resources_df.isnull().values.any() == False and
        class_resources_df['class_id'].is_unique and
        (class_resources_df[numeric_columns] >= 0).all().all() and
        class_resources_df['number_of_students'].max() <= 100 and
        class_resources_df['number_of_teachers'].max() <= 20 and
        class_resources_df['weekly_teaching_hours'].between(20, 50).all()):
        
        class_resources_df.to_parquet('./passed_basic_quality_checks/class_resources_table.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")




def extracurricular_activities_data_checks():
    # 1. check for nul values in all columns
    if extracurricular_df.isnull().values.any():
        print("Nul values found in the dataframe:\n", extracurricular_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure student_id exists in student_table
    missing_students = extracurricular_df[~extracurricular_df['student_id'].isin(student_df['student_id'])]
    if not missing_students.empty:
        print("student_id(s) missing in student_table:\n", missing_students['student_id'].unique())
    else:
        print("all student_ids exist in student_table.")

    # 3. Verify weekly_hours is non-negative and within a realistic range (0-20 hours)
    if not extracurricular_df['weekly_hours'].between(0, 20).all():
        print("weekly_hours not in the realistic range (0-20 hours) or contains negative values.")
    else:
        print("weekly_hours is within a realistic range (0-20 hours) and non-negative.")

    # Save to parquet if all checks pass
    if (extracurricular_df.isnull().values.any() == False and
        missing_students.empty and
        extracurricular_df['weekly_hours'].between(0, 20).all()):
        
        extracurricular_df.to_parquet('./passed_basic_quality_checks/extracurricular_activity.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")




def parent_data_quality_checks():
    # 1. check for nul values in all columns
    if parent_df.isnull().values.any():
        print("Nul values found:\n", parent_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure student_id is unique and matches with student_table
    duplicate_student_ids = parent_df['student_id'].duplicated().sum()
    if duplicate_student_ids > 0:
        print(f"found {duplicate_student_ids} duplicate student_ids.")
    else:
        print("all student_ids are unique.")

    missing_students = parent_df[~parent_df['student_id'].isin(student_df['student_id'])]
    if not missing_students.empty:
        print("student_id(s) missing in student_table:\n", missing_students['student_id'].unique())
    else:
        print("all student_ids exist in student_table.")

    # 3. Verify household_Size is positive and within a realistic range (e.g., 1-15)
    if not parent_df['household_size'].between(1, 15).all():
        print("household_Size contains values outside the realistic range (1-15).")
    else:
        print("household_Size is within the realistic range.")

    # 4. check if Annual_household_Income(NGN) is valid
    valid_income_ranges = ['Below 200,000', '200,000-400,000', '400,000-600,000', 'Above 600,000']
    if not parent_df['annual_household_income_ngn'].isin(valid_income_ranges).all():
        print("Invalid values found in Annual_household_Income(NGN).")
    else:
        print("Annual_household_Income(NGN) has valid values.")

    # 5. ensure father_education, mother_education, fatheoccu, motheoccu, and Involvement_in_Kids_education have consistent categories
    consistent_columns = ['father_education', 'mother_education', 'father_occupation', 'mother_occupation', 'involvement_in_kids_education']
    for col in consistent_columns:
        print(f"Unique values in {col}:\n", parent_df[col].unique())

    # Save to parquet if all checks pass
    if (parent_df.isnull().values.any() == False and
        duplicate_student_ids == 0 and
        missing_students.empty and
        parent_df['household_size'].between(1, 15).all() and
        parent_df['annual_household_income_ngn'].isin(valid_income_ranges).all()):
        
        parent_df.to_parquet('./passed_basic_quality_checks/parent_table.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")



def survey_data_quality():
    # 1. check for nul values in all columns
    if survey_df.isnull().values.any():
        print("Nul values found:\n", survey_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure student_id is unique and matches with student_table
    if survey_df['student_id'].duplicated().any():
        print("duplicate student_ids found.")
    else:
        print("all student_ids are unique.")

    missing_students_survey = survey_df[~survey_df['student_id'].isin(student_df['student_id'])]
    if not missing_students_survey.empty:
        print("student_id(s) missing in student_table:\n", missing_students_survey['student_id'].unique())
    else:
        print("all student_ids exist in student_table.")

    # 3. Verify study_hours_per_week is non-negative and within a realistic range (0-50)
    if not survey_df['study_hours_per_week'].between(0, 50).all():
        print("study_hours_per_week contains values outside the realistic range (0-50).")
    else:
        print("study_hours_per_week is within the realistic range.")

    # 4. check if teacher_support and parental_Suport are within a specific range (1-5)
    suport_cols = ['teacher_support', 'parental_support']
    for col in suport_cols:
        if not survey_df[col].between(1, 5).all():
            print(f"{col} contains values outside the range 1-5.")
        else:
            print(f"{col} is within the range 1-5.")

    # 5. ensure Stress_level has consistent categories
    print("Unique values in Stress_level:", survey_df['stress_level'].unique())

    # 6. Verify Jamb_Scores and Num_credit_passes_WAec are within expected ranges
    if not survey_df['jamb_scores'].between(0, 400).all():
        print("Jamb_Scores contain values outside the expected range (0-400).")
    else:
        print("Jamb_Scores are within the expected range.")

    if not survey_df['num_credit_passes_waec'].between(0, 9).all():
        print("Num_credit_passes_WAec contains values outside the expected range (0-9).")
    else:
        print("Num_credit_passes_WAec is within the expected range.")

    # 7. check if verdict has consistent categories
    print("Unique values in verdict:", survey_df['verdict'].unique())

    # Save to parquet if all checks pass
    if (survey_df.isnull().values.any() == False and
        not survey_df['student_id'].duplicated().any() and
        missing_students_survey.empty and
        survey_df['study_hours_per_week'].between(0, 50).all() and
        survey_df[suport_cols].apply(lambda x: x.between(1, 5).all()).all() and
        survey_df['jamb_scores'].between(0, 400).all() and
        survey_df['num_credit_passes_waec'].between(0, 9).all()):
        
        survey_df.to_parquet('./passed_basic_quality_checks/ss3_student_survey.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")


def staf_data_quality():
    # 1. check for nul values in all columns
    if staff_df.isnull().values.any():
        print("Nul values found:\n", staff_df.isnull().sum())
    else:
        print("No nul values found.")

    # 2. ensure staff_id is unique
    if staff_df['staff_id'].duplicated().any():
        print("duplicate staff_ids found.")
    else:
        print("all staff_ids are unique.")

    # 3. Verify monthly pay and years of experience are non-negative
    if (staff_df[['monthly_pay', 'years_of_experience']] < 0).any().any():
        print("monthly pay or years of experience contains negative values.")
    else:
        print("monthly pay and years of experience are non-negative.")

    # 4. check if date of hire is in a consistent date format and not in the future
    staff_df['date_of_hire'] = pd.to_datetime(staff_df['date_of_hire'], errors='coerce')
    future_dates = staff_df[staff_df['date_of_hire'] > pd.Timestamp.now()]
    if not future_dates.empty:
        print("future date of hire values found:\n", future_dates['date_of_hire'])
    else:
        print("all date of hire values are valid.")

    # 5. ensure gender, position, and education level have consistent categories
    print("Unique values in gender:", staff_df['gender'].unique())
    print("Unique values in position:", staff_df['position'].unique())
    print("Unique values in education level:", staff_df['education_level'].unique())

    # Save to parquet if all checks pass
    if (staff_df.isnull().values.any() == False and
        not staff_df['staff_id'].duplicated().any() and
        not (staff_df[['monthly_pay', 'years_of_experience']] < 0).any().any() and
        future_dates.empty):
        
        staff_df.to_parquet('./passed_basic_quality_checks/staff_table.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")



def performance_data_quality():

    # 1. check for nul values in relevant columns
    if performance_df[['mathematics', 'english_language', 'civic_education', 'economics', 'crs_islam']].isnull().any().any():
        print("Nul values found in key columns:\n", performance_df[['mathematics', 'english language', 'civic education', 'economics', 'cRS_Islam']].isnull().sum())
    else:
        print("No nul values found in the relevant columns.")

    # 2. ensure student_id is unique and matches with student_table
    if performance_df['student_id'].duplicated().any():
        print("duplicate student_ids found.")
    else:
        print("all student_ids are unique.")

    # check if student_ids exist in student_table
    missing_students_perf = performance_df[~performance_df['student_id'].isin(student_df['student_id'])]
    if not missing_students_perf.empty:
        print("student_id(s) missing in student_table:\n", missing_students_perf['student_id'].unique())
    else:
        print("all student_ids exist in student_table.")

    # 3. Verify that scores for 'mathematics', 'english language', 'civic education', 'economics', 'cRS_Islam' are within the expected range (0-100)
    columns_to_check = ['mathematics', 'english_language', 'civic_education', 'economics', 'crs_islam']
    valid_scores = performance_df[columns_to_check].apply(lambda x: x.between(0, 100) | x.isna()).all()
    if not valid_scores.all():
        print("Some scores are outside the expected range (0-100) in these columns:", valid_scores[~valid_scores].index.tolist())
    else:
        print("all non-nul scores are within the expected range (0-100).")

    # 4. check for any outliers in the scores (based on z-scores), ignoring NaN
    z_scores = (performance_df[columns_to_check] - performance_df[columns_to_check].mean()) / performance_df[columns_to_check].std()
    outliers = z_scores.abs() > 3  # threshold for outliers (z-score > 3)
    if outliers.any().any():
        print("Outliers found in the folowing columns:\n", outliers.columns[outliers.any()])
    else:
        print("No significant outliers found.")

    # 5. Ignore NaN columns, ensure decimall places for float64 columns are consistent
    float_columns = performance_df[columns_to_check].select_dtypes(include=['float64']).columns
    if performance_df[float_columns].apply(lambda x: x.apply(lambda v: len(str(v).split('.')[-1]) if '.' in str(v) else 0).nunique() > 1).any():
        print("Inconsistent decimall places in float64 columns.")
    else:
        print("decimall places are consistent in float64 columns.")

    # Save to parquet if all checks pass
    if (performance_df[['mathematics', 'english_language', 'civic_education', 'economics', 'crs_islam']].isnull().any().any() == False and
        not performance_df['student_id'].duplicated().any() and
        missing_students_perf.empty and
        valid_scores.all() and
        not outliers.any().any()):


        
        performance_df.to_parquet('./passed_basic_quality_checks/student_performance.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")



def student_data_quality_checks():
    # 1. check for nul values in all columns
    if student_df.isnull().any().any():
        print("Nul values found in the folowing columns:\n", student_df.isnull().sum())
    else:
        print("No nul values found in any columns.")

    # 2. ensure student_id is unique
    if student_df['student_id'].duplicated().any():
        print("duplicate student_ids found.")
    else:
        print("all student_ids are unique.")

    # 3. Verify class_id exists in class_resources_table
    missing_class_ids = student_df[~student_df['class_id'].isin(class_resources_df['class_id'])]
    if not missing_class_ids.empty:
        print("class_id(s) missing in class_resources_table:\n", missing_class_ids['class_id'].unique())
    else:
        print("all class_ids exist in class_resources_table.")

    # 4. check if date_of_birth is in a consistent date format and makes sense for a student
    # Assuming the format is 'y-m-d'
    def check_date_format(date_str):
        try:
            return pd.to_datetime(date_str, format='%y-%m-%d', errors='raise')
        except exception:
            return None

    invalid_dates = student_df['date_of_birth'].apply(check_date_format).isnull()
    if invalid_dates.any():
        print("Invalid date_of_birth found:\n", student_df[invalid_dates]['date_of_birth'])
    else:
        print("all date_of_births are in a consistent format.")

    # 5. ensure gender, State of Origin, engagement_in_class, health_condition, and class Spec have consistent categories
    # example categories
    gender_categories = ['male', 'female']
    state_origin_categories = nigeria_states  
    engagement_categories = ['troublesome','Unactive','Slightly active','Active','highly active']
    health_condition_categories = health_condition
    class_spec_categories = ['Science', 'Art']  

    if not student_df['gender'].isin(gender_categories).all():
        print("Inconsistent categories found in gender column.")
    if not student_df['state_of_origin'].isin(state_origin_categories).all():
        print("Inconsistent categories found in State of Origin column.")
    if not student_df['engagement_in_class'].isin(engagement_categories).all():
        print("Inconsistent categories found in engagement_in_class column.")
    if not student_df['health_condition'].isin(health_condition_categories).all():
        print("Inconsistent categories found in health_condition column.")
    if not student_df['class_spec'].isin(class_spec_categories).all():
        print("Inconsistent categories found in class Spec column.")

    # Save to parquet if all checks pass
    if (not student_df.isnull().any().any() and
        not student_df['student_id'].duplicated().any() and
        missing_class_ids.empty and not invalid_dates.any()):
        
        student_df.to_parquet('./passed_basic_quality_checks/student_table.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")



def teacher_data_quality_checks():

    # 1. check for nul values in all columns
    if teachers_df.isnull().any().any():
        print("Nul values found in the folowing columns:\n", teachers_df.isnull().sum())
    else:
        print("No nul values found in any columns.")

    # 2. ensure teacher_id is unique
    if teachers_df['teacher_id'].duplicated().any():
        print("duplicate teacher_ids found.")
    else:
        print("all teacher_ids are unique.")

    # 3. Verify staff_id exists in staf_table
    missing_staff_ids = teachers_df[~teachers_df['staff_id'].isin(staff_df['staff_id'])]
    if not missing_staff_ids.empty:
        print("staff_id(s) missing in staf_table:\n", missing_staff_ids['staff_id'].unique())
    else:
        print("all staff_ids exist in staf_table.")

    # 4. ensure teacher type and Subject specialization have consistent categories
    # example categories
    teacher_type_categories = teacher_type  # Update as per your data
    subject_specialization_categories =subjects  # Update as per your data

    if not teachers_df['teacher_type'].isin(teacher_type_categories).all():
        print("Inconsistent categories found in teacher type column.")
    if not teachers_df['subject_specialization'].isin(subject_specialization_categories).all():
        print("Inconsistent categories found in Subject specialization column.")

    # Save to parquet if all checks pass
    if (not teachers_df.isnull().any().any() and
        not teachers_df['teacher_id'].duplicated().any() and
        missing_staff_ids.empty):
        
        teachers_df.to_parquet('./passed_basic_quality_checks/teachers_table.parquet')
        print("all data quality checks passed. data saved as parquet.")
    else:
        print("data quality checks failed.")

student_data_quality_checks()

performance_data_quality()

staf_data_quality()

survey_data_quality()

parent_data_quality_checks()

extracurricular_activities_data_checks()

class_resources_quality_checks()

atendance_quality_checks()

teacher_data_quality_checks()
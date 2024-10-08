import random
import pandas as pd
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import csv

def scrape_behindthename(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = soup.select('div.browsename')
    return [name.text.strip() for name in names]

def scrape_momjunction(base_url, gender):
    all_names = []
    page = 1
    while True:
        url = f"{base_url}?gender={gender}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': f'baby-name-{gender}'})
        
        if not table:
            break
        
        rows = table.find_all('tr')[1:]  # Skip header row
        names = [row.find_all('td')[1].text.strip() for row in rows]
        
        if not names:
            break
        
        all_names.extend(names)
        page += 1
    
    return all_names


female_names = scrape_behindthename('https://www.behindthename.com/names/gender/feminine/usage/nigerian')
male_names = scrape_behindthename('https://www.behindthename.com/names/gender/masculine/usage/nigerian')
unisex_names = scrape_behindthename('https://www.behindthename.com/names/gender/unisex/usage/nigerian')

momjunction_url = 'https://www.momjunction.com/baby-names/nigerian/'
female_names.extend(scrape_momjunction(momjunction_url, 'girl'))
male_names.extend(scrape_momjunction(momjunction_url, 'boy'))

# Remove duplicates and sort
female_names = sorted(set(female_names))
male_names = sorted(set(male_names))
unisex_names = sorted(set(unisex_names))

def parse_name_data(name_data):
    parts = name_data.split(' ')
    first_name = parts[0]  
    ethnic_group = (
        'Hausa' if 'Hausa' in name_data else
        'Yoruba' if 'Yoruba' in name_data else
        'Igbo' if 'Igbo' in name_data else
        'Urhobo' if 'Urhobo' in name_data else
        'Ibibio' if 'Ibibio' in name_data else
        'Other'
    )
    return first_name, ethnic_group

# Create dictionary by parsing each entry
name_ethnic_male = {parse_name_data(name)[0]: parse_name_data(name)[1] for name in male_names}
name_ethnic_female = {parse_name_data(name)[0]: parse_name_data(name)[1] for name in female_names}



# Initialize Faker and set random seeds
fake = Faker()
Faker.seed(42)
np.random.seed(42)

# Define constants
regions = ['North Central', 'North East', 'North West', 'South East', 'South South', 'South West']
nigeria_states = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe",
    "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
    "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau",
    "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "FCT"
]

education_levels = ['None', 'Primary', 'Secondary', 'Tertiary']
occupations = ['Farmer', 'Trader', 'Teacher', 'Civil Servant', 'Engineer', 'Unemployed', 'Doctor', 'Nurse']
extracurricular_activities = ['Sports', 'Drama', 'Debate Club', 'Art','Jet club','Press club','Literature club']
common_subjects = ['Mathematics', 'English_Language', 'Civic_Education', 'Economics', 'CRS_Islam']
science_subjects = ['Physics', 'Chemistry', 'Biology', 'Geography', 'Computer_Science']
art_subjects = ['Government', 'Commerce', 'Literature','History', 'Accounting']
subjects = common_subjects + science_subjects + art_subjects
health_condition = ['Asthma'] * 3 + ['Sickle Cell'] * 2 + ['Ulcer'] * 3 + ['Epilepsy']*1 + ['Dyslexia']*20 + ['None']*91
teacher_type =  ['Corper','Regular']
weights = [0.2, 0.8]  

# Define staff positions with number of positions and pay grade
staff_positions = {
    "Teacher": {"count": len(subjects), "pay_grade": 100000},
    "Principal": {"count": 1, "pay_grade": 170000},
    "Vice Principal": {"count": 1, "pay_grade": 150000},
    "Librarian": {"count": 2, "pay_grade": 80000},
    "School Nurse": {"count": 2, "pay_grade": 120000},
    "Administrative Assistant": {"count": 3, "pay_grade": 80000},
    "Cleaner": {"count": 3, "pay_grade": 30000},
    "Vendor": {"count": 2, "pay_grade": 40000},
    "Bus Driver": {"count": 2, "pay_grade": 70000},
    "Lab attendant": {"count": 2, "pay_grade": 90000},
    "Security Guard": {"count": 2, "pay_grade": 70000}
}

# Helper functions
def random_dobs(min_age, max_age):
    now = datetime.now()
    return (now - timedelta(days=random.randint(min_age*365, max_age*365))).strftime("%Y-%m-%d")

def assign_scores(subjects):
    return {subject: random.randint(0, 100) for subject in subjects}

# Generate class resources data
def generate_dim_class_resources():
    data = []
    levels = ['SS1', 'SS2', 'SS3']
    segments = ['A', 'B', 'C', 'D', 'E', 'F']
    
    for level in levels:
        for segment in segments:
            class_name = f"{level} Class {segment}"
            num_students = random.randint(50, 60)
            data.append({
                'Class_ID': class_name,
                'Number_of_Students': num_students,
                'Number_of_Teachers': random.randint(5, 10),
                'Weekly_Teaching_Hours': random.randint(20, 35),
                'Weekly_Library_Time': random.randint(1, 5),
                'Weekly_Computer_Training_Time': random.randint(2, 3),
                'Weekly_Lab_Hours': random.randint(0, 4),
                'Chalkboard': random.randint(1, 3),
                'Basic_Textbooks': random.randint(0, 4),
                'Chairs_Desks': num_students,
                'Functional_Fans': random.randint(0, 4)
            })
    
    return pd.DataFrame(data)

dim_class_resources = generate_dim_class_resources()
NUM_STUDENTS = sum(dim_class_resources.Number_of_Students)

# Generate staff data
def generate_staff_data():
    data = []
    for position, details in staff_positions.items():
        for _ in range(details["count"]):
            staff_member = {
                'Staff_ID': fake.unique.uuid4(),
                "Name": ', '.join(random.sample(list(name_ethnic_male.keys()), 2)),
                'Gender': random.choice(['Male', 'Female']),
                "Position": position,
                "Monthly_Pay": details["pay_grade"],
                "Years_of_Experience": random.randint(0, 30),
                "Education_Level": fake.random_element(elements=("High School", "Associate's", "Bachelor's", "Master's", "PhD")),
                "Date_of_Hire": fake.date_between(start_date="-30y", end_date="today"),
                "Full_time": fake.boolean(chance_of_getting_true=80)
            }
            data.append(staff_member)
    return data

staff_data = generate_staff_data()
staff_table = pd.DataFrame(staff_data)
staff_table['Staff_ID'] = staff_table['Staff_ID'].str.replace('-', '', regex=False)

# Generate teacher data
def generate_teacher_table():
    teachers_table = staff_table[staff_table['Position'] == 'Teacher'][['Staff_ID', 'Name']].copy()
    teachers_table['Teacher_ID'] = [fake.unique.uuid4() for i in range(len(teachers_table))]
    teachers_table['Teacher_ID'] = teachers_table['Teacher_ID'].str.replace('-', '', regex=False)
    teachers_table['Teacher_Type'] = random.choices(teacher_type, weights=weights, k=len(teachers_table))
    teachers_table['Subject_specialization'] = subjects
    teachers_table = teachers_table[['Teacher_ID', 'Staff_ID', 'Name', 'Teacher_Type', 'Subject_specialization']]
    return teachers_table

teachers_table = generate_teacher_table()

# Generate student data
def generate_dim_student(num_students, dim_class):
    data = []
    for _ in range(num_students):
        student_id = fake.unique.uuid4()
        gender = random.choice(['Male', 'Female'])
        DOB = random_dobs(14, 18) 
        region = random.choice(regions)
        class_id = random.choice(dim_class['Class_ID'].tolist())
        data.append({
            'Student_ID': student_id,
            'Class_ID': class_id,
            'First_Name': ', '.join(random.sample(list(name_ethnic_male.keys()), 1)),
            'Family_Name': ', '.join(random.sample(list(name_ethnic_male.keys()), 1)),
            'Gender': gender,
            'Date_of_Birth': DOB,
            'State_of_Origin': random.choice(nigeria_states),
            'engagement_in_class': random.choice(['Troublesome','Unactive','Slightly active','Active','Highly active']),
            'health_condition': random.choice(health_condition),
            'Class_Spec': random.choice(['Art','Science'])
        })
    return pd.DataFrame(data)

dim_student = generate_dim_student(NUM_STUDENTS, dim_class_resources)
dim_student['Student_ID'] = dim_student['Student_ID'].str.replace('-', '', regex=False)

# Generate parent demographics data
def generate_dim_parent_demographics(dim_student):
    data = []
    for _, student in dim_student.iterrows():
        data.append({
            'Student_ID': student['Student_ID'],
            'Fathers_Name': ', '.join(random.sample(list(name_ethnic_male.keys()), 1)),
            'Mothers_Name': ', '.join(random.sample(list(name_ethnic_female.keys()), 1)),
            'Family_Name' : ', '.join(random.sample(list(name_ethnic_male.keys()), 1)),
            'Father_Education': random.choice(education_levels),
            'Mother_Education': random.choice(education_levels),
            'Father_Occupation': random.choice(occupations),
            'Mother_Occupation': random.choice(occupations),
            'Annual_Household_Income_NGN': random.choice(['Below 200,000', '200,000-400,000', '400,000-600,000', 'Above 600,000']),
            'Household_Size': random.choice(np.arange(2, 7)),
            'Involvement_in_Kids_Education': random.choice(['Always busy', 'Slightly involved', 'Involved', 'Very Involved'])
        })
    return pd.DataFrame(data)

dim_parent_demographics = generate_dim_parent_demographics(dim_student)

# Generate extracurricular activity data
def generate_dim_extracurricular_activity(dim_student):
    data = []
    for _, student in dim_student.iterrows():
        extracurricular = random.choice(extracurricular_activities)
        weekly_hours_in_activity = random.randint(1, 10) if extracurricular != 'None' else 0
        data.append({
            'Student_ID': student['Student_ID'],
            'Extracurricular_Activity': extracurricular,
            'Weekly_Hours': weekly_hours_in_activity
        })
    return pd.DataFrame(data)

dim_extracurricular_activity = generate_dim_extracurricular_activity(dim_student)

# Generate attendance data
def generate_fact_attendance(dim_student): 
    data = []
    students_missing_school = random.sample(dim_student.index.tolist(), random.randint(10, 50))
    
    for idx, student in dim_student.iterrows():
        if idx in students_missing_school:
            days_attended = random.randint(60, 94)
            days_missed = 95 - days_attended
            absence_reason = random.choice(['Illness', 'Family Event', 'Other','Truancy','School fees drive','Insecurity'])
        else:
            days_attended = 95
            days_missed = 0
            absence_reason = 'Full Attendance'
        
        data.append({
            'Student_ID': student['Student_ID'],
            'Days_Attended': days_attended,
            'Days_Missed': days_missed,
            'Absence_Reason': absence_reason
        })
        
    return pd.DataFrame(data)

fact_attendance = generate_fact_attendance(dim_student)

# Generate student performance data
def generate_student_performance(dim_student):
    dim_student_copy = dim_student[['Student_ID', 'Class_Spec']].copy()
    data = []
    
    for _, row in dim_student_copy.iterrows():
        student_id = row['Student_ID']
        class_spec = row['Class_Spec']
        
        performance = assign_scores(common_subjects)
        
        if class_spec == 'Science':
            performance.update(assign_scores(science_subjects))
            performance.update({subject: None for subject in art_subjects})
        else:
            performance.update(assign_scores(art_subjects))
            performance.update({subject: None for subject in science_subjects})
        
        data.append({
            'Student_ID': student_id,
            **performance
        })
    
    return pd.DataFrame(data)

student_performance = generate_student_performance(dim_student)

# Generate SS3 student performance survey data
def generate_ss3_student_performance_survey(dim_student):
    ss3_students = dim_student[dim_student['Class_ID'].str.startswith('SS3')]
    reasons_for_performance = ['Lack of preparation', 'Difficulty understanding topics', 
                               'Personal issues', 'Health challenges', 'Confidence issues', 
                               'Lack of resources']
    data = []
    for _, student in ss3_students.iterrows():
        data.append({
            'Student_ID': student['Student_ID'],
            'Reason_For_Performance': random.choice(reasons_for_performance),
            'Access_To_Resources': random.choice(['Yes', 'No']),
            'Study_Hours_Per_Week': random.randint(0, 40),
            'Health_Issues': random.choice(['Yes', 'No']),
            'Teacher_Support': random.randint(1, 5),
            'Parental_Support': random.randint(1, 5),
            'Stress_Level': random.choice(['Yes', 'No']),
            'Peer_Influence': random.choice(['Yes', 'No']),
            'Additional_Tutoring': random.choice(['Yes', 'No']),
            'Use_Of_Study_Groups': random.choice(['Yes', 'No']),
            'Exam_Anxiety': random.choice(['Yes', 'No']),
            'Jamb_Scores': random.randint(100, 400),
            'Num_Credit_Passes_WAEC': random.randint(2, 9)
        })
    
    return pd.DataFrame(data)

ss3_student_survey = generate_ss3_student_performance_survey(dim_student)
ss3_student_survey['verdict'] = ss3_student_survey.apply(lambda row: 'Pass' if row['Jamb_Scores'] >= 200 and row['Num_Credit_Passes_WAEC'] >= 5 else 'Fail', axis=1)

# Save all tables to CSV files
dim_class_resources
dim_student
dim_parent_demographics
dim_extracurricular_activity
staff_table
teachers_table
student_performance
fact_attendance
ss3_student_survey
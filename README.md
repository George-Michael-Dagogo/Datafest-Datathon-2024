## I'm attempting to create a comprehensive dataset that simulates a Nigerian secondary school environment. My goal is to generate realistic, interconnected data that can be used for various educational analytics and data science projects. 

## Here's a breakdown of my approach:

### Data Generation: I'm using Python libraries like Faker, random, and numpy to generate synthetic data. This allows me to create a large volume of realistic-looking data without compromising real students' privacy.
### School Structure: I've modeled the school with Senior Secondary (SS) classes from SS1 to SS3, each with segments A through F. This reflects a typical Nigerian secondary school structure.
### Diverse Data Points: I'm generating a wide range of data points including student demographics, parent information, staff details, class resources, academic performance, attendance records, and extracurricular activities. This comprehensive approach allows for rich, multi-faceted analysis.
### Nigerian Context: I've incorporated Nigerian-specific elements like regions, states, and name patterns to make the data more authentic to the Nigerian educational context.
### Interconnected Tables: I'm creating several interconnected tables (dimensions and facts) that follow a star schema design. This structure is ideal for data warehousing and facilitates easier querying and analysis.
### Realistic Constraints: I'm implementing realistic constraints and distributions in the data. For example, the number of students per class, the range of test scores, and the distribution of health conditions are all designed to reflect real-world scenarios.
### Special Focus on SS3: I've added a special survey for SS3 students, including mock JAMB scores and WAEC results. This allows for more detailed analysis of final-year students' performance and factors affecting their outcomes.
### Flexibility and Scalability: My approach allows for easy scaling of the dataset size and modification of parameters. This flexibility makes it adaptable for various research questions or analytical needs.
### Data Quality checks: I added data quality checks(assuming this was real world data) that needs to be passed befoe the data is saved as parquet.
### Parquet Output:I'm saving all generated data as parquet files. Saving as Parquet ensures efficient storage, faster data access, and better compatibility with big data tools.
### Saving to data lake on Azure: 
### Saving to Postgres on Aiven: 
### Web Interface for New Data:

#### The reason I took this approach is to create a rich, realistic dataset that can be used for educational data mining, predictive analytics, and decision support systems in the context of Nigerian secondary education. By simulating a complete school ecosystem, I'm providing a sandbox for testing various hypotheses about factors influencing student performance, resource allocation, and overall school management.
#### This dataset could be valuable for researchers, data scientists, or education policymakers looking to develop insights or predictive models without the need for sensitive, real-world student data. It also serves as a great teaching tool for data science students learning about educational data analysis.

## School Database Data Dictionary (Updated)

### class_resources_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Class_ID | VARCHAR(20) | 20 | Primary key, unique identifier for each class | SS1 Class A |
| Number_of_Students | SMALLINT | 2 bytes | Number of students in the class | 60 |
| Number_of_Teachers | SMALLINT | 2 bytes | Number of teachers assigned to the class |82 |
| Weekly_Teaching_Hours | SMALLINT | 2 bytes | Total teaching hours per week for the class | 40 |
| Weekly_Library_Time | SMALLINT | 2 bytes | Hours per week spent in the library | 5 |
| Weekly_Computer_Training_Time | SMALLINT | 2 bytes | Hours per week spent on computer training | 3 |
| Weekly_Lab_Hours | SMALLINT | 2 bytes | Hours per week spent in the laboratory | 4 |
| Chalkboard | SMALLINT | 2 bytes | Quantity or condition of chalkboards | 2 |
| Basic_Textbooks | SMALLINT | 2 bytes | Quantity or availability of basic textbooks | 25 |
| Chairs_Desks | SMALLINT | 2 bytes | Quantity or condition of chairs and desks | 60 |
| Functional_Fans | SMALLINT | 2 bytes | Number of functional fans in the classroom | 3 |

## student_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key, unique identifier for each student| ccf3a17156dc4907ba6c34ab6712303a |
| Class_ID | VARCHAR(20) | 20 | Foreign key referencing class_resources_table | SS3 Class F |
| First_Name | TEXT | Variable | Student's first name | "Okorie" |
| Family_Name | TEXT | Variable | Student's family name | "Dubem" |
| Gender | TEXT | Variable | Student's gender | "Male" |
| Date_of_Birth | DATE | 3 bytes | Student's date of birth | "2005-07-15" |
| State_of_Origin | TEXT | Variable | Student's state of origin | "Lagos" |
| engagement_in_class | TEXT | Variable | Level or description of student's engagement in class | Unactive |
| health_condition | TEXT | Variable | Description of student's health condition | "None" |
| Class_Spec | TEXT | Variable | Specific class or stream the student belongs to | "Science" |

## parent_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key and foreign key referencing student_table | ccf3a17156dc4907ba6c34ab6712303a |
| Fathers_Name | TEXT | Variable | Name of the student's father | "Michael" |
| Mothers_Name | TEXT | Variable | Name of the student's mother | "Silver" |
| Family_Name | TEXT | Variable | Family name of the parents | "Mbawike" |
| Father_Education | TEXT | Variable | Educational level of the father | Tetiary |
| Mother_Education | TEXT | Variable | Educational level of the mother | Secondary |
| Father_Occupation | TEXT | Variable | Occupation of the father | "Engineer" |
| Mother_Occupation | TEXT | Variable | Occupation of the mother | "Teacher" |
| Annual_Household_Income_NGN | TEXT | Variable | Annual household income in Nigerian Naira | 400,000-600,000 |
| Household_Size | INTEGER | 4 bytes | Number of people in the household | 5 |
| Involvement_in_Kids_Education | TEXT | Variable | Level or description of parental involvement in child's education | Very Involved |

## extracurricular_activity

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key and foreign key referencing student_table | ccf3a17156dc4907ba6c34ab6712303a |
| Extracurricular_Activity | TEXT | Variable | Name or type of extracurricular activity | "Chess Club" |
| Weekly_Hours | INTEGER | 4 bytes | Hours per week spent on the activity | 6 |

## student_performance

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key and foreign key referencing student_table | ccf3a17156dc4907ba6c34ab6712303a |
| Mathematics | INTEGER | 4 bytes | Student's score in Mathematics | 85 |
| English_Language | INTEGER | 4 bytes | Student's score in English Language | 78 |
| Civic_Education | INTEGER | 4 bytes | Student's score in Civic Education | 90 |
| Economics | INTEGER | 4 bytes | Student's score in Economics | 82 |
| CRS_Islam | INTEGER | 4 bytes | Student's score in Christian Religious Studies or Islamic Studies | 88 |
| Physics | FLOAT | 4 bytes | Student's score in Physics | 76.5 |
| Chemistry | FLOAT | 4 bytes | Student's score in Chemistry | 81.0 |
| Biology | FLOAT | 4 bytes | Student's score in Biology | 79.5 |
| Geography | FLOAT | 4 bytes | Student's score in Geography | 85.0 |
| Computer_Science | FLOAT | 4 bytes | Student's score in Computer Science | 92.5 |
| Government | FLOAT | 4 bytes | Student's score in Government | 88.0 |
| Commerce | FLOAT | 4 bytes | Student's score in Commerce | 77.5 |
| Literature | FLOAT | 4 bytes | Student's score in Literature | 83.0 |
| History | FLOAT | 4 bytes | Student's score in History | 86.5 |
| Accounting | FLOAT | 4 bytes | Student's score in Accounting | 80.0 |

## attendance_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key and foreign key referencing student_table | ccf3a17156dc4907ba6c34ab6712303a |
| Days_Attended | INTEGER | 4 bytes | Number of days the student attended | 90 |
| Days_Missed | INTEGER | 4 bytes | Number of days the student missed | 5 |
| Absence_Reason | TEXT | Variable | Reason for student's absence | "Illness" |

## ss3_student_survey

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Student_ID | VARCHAR(100) | 100 | Primary key and foreign key referencing student_table | ccf3a17156dc4907ba6c34ab6712303a |
| Reason_For_Performance | TEXT | Variable | Student's explanation for their academic performance | "Regular study and parental support" |
| Access_To_Resources | TEXT | Variable | Description of student's access to educational resources | "Good access to textbooks and internet" |
| Study_Hours_Per_Week | INTEGER | 4 bytes | Number of hours spent studying per week | 20 |
| Health_Issues | TEXT | Variable | Description of any health issues affecting studies | "None" |
| Teacher_Support | INTEGER | 4 bytes | Level of support received from teachers (likely a scale) | 8 |
| Parental_Support | INTEGER | 4 bytes | Level of support received from parents (likely a scale) | 9 |
| Stress_Level | TEXT | Variable | Description of student's stress level | "Moderate" |
| Peer_Influence | TEXT | Variable | Description of peer influence on academic performance | "Positive" |
| Additional_Tutoring | TEXT | Variable | Information about any additional tutoring received | "Math tutor twice a week" |
| Use_Of_Study_Groups | TEXT | Variable | Information about participation in study groups | "Weekly science study group" |
| Exam_Anxiety | TEXT | Variable | Description of student's exam anxiety level | "Low" |
| Jamb_Scores | SMALLINT | 2 bytes | Student's JAMB (Joint Admissions and Matriculation Board) scores | 280 |
| Num_Credit_Passes_WAEC | SMALLINT | 2 bytes | Number of credit passes in WAEC (West African Examinations Council) exams | 7 |
| Verdict | Text | Variable | Pass or Fail based on getting above 200 and above 5 in Jamb and WAEC respectively  | Pass |

## staff_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Staff_ID | VARCHAR(100) | 100 | Primary key, unique identifier for each staff member | bdd640fb06674ad19c80317fa3b1799d |
| Name | TEXT | Variable | Name of the staff member | "Alice Johnson" |
| Gender | TEXT | Variable | Gender of the staff member | "Female" |
| Position | TEXT | Variable | Position or role of the staff member | "Teacher" |
| Monthly_Pay | INTEGER | 4 bytes | Monthly salary of the staff member | 150000 |
| Years_of_Experience | INTEGER | 4 bytes | Number of years of work experience | 8 |
| Education_Level | TEXT | Variable | Highest level of education attained | "Master's" |
| Date_of_Hire | TEXT | Variable | Date when the staff member was hired | "2015-09-01" |
| Full_time | BOOLEAN | 1 byte | Indicates whether the staff member is full-time (true) or part-time (false) | true |

## teachers_table

| Column Name | Data Type | Field Size | Description | Example |
|-------------|-----------|------------|-------------|---------|
| Teacher_ID | VARCHAR(100) | 100 | Primary key, unique identifier for each teacher | anf476539s674ad19c80317fa334g9f |
| Staff_ID | VARCHAR(100) | 100 | Foreign key referencing staff_table | bdd640fb06674ad19c80317fa3b1799d |
| Name | TEXT | Variable | Name of the teacher | "Alice Johnson" |
| Teacher_Type | TEXT | Variable | Type or category of teacher | "Senior Teacher" |
| Subject_specialization | TEXT | Variable | Subject area of specialization for the teacher | "Mathematics" |

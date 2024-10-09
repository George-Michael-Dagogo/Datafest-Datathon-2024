# Improving  Academic Outcome For Secondary Education in Nigeria -- DataFestAfrica Hackathon 2024

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/Secondary%20school%20kids.jpg" alt="Secondary school kids">
</p>
<div align="center">
  <p style="font-size: 7px;"><i>© UNICEF/UN0270198/Knowles-Coursin</i></p>
</div>


# Background: Problem statement

Goodness and Mercy School (GMS) is what we can call a budget private primary and secondary school in Kaduna South local government of Kaduna state, Nigeria. A hypothetical situation featured a stakeholders meeting highlighting the lack of infrastructure for digital data collection plus the inadequate paper records being kept. Also, according to JAMB the results from the 2024 UTME showed that 76% (approx. 4 out of 5) of students who participated in the 2024 UTME scored [less than 200](https://www.premiumtimesng.com/news/690022-updated-jamb-releases-2024-utme-results-76-scores-below-200.html). This has raised a huge concern for the stakeholders and hence they have decided to take proactive measures to guard against this failure rate for their next batch of students in their upcoming final exams and consequently the JAMB and WASSCE exams.

**P.S. Budget private school refers to a private school that falls between a public school and a low-cost private school.**

The **Phoenix team (Hannah Igboke, Michael George, and Olawumi Olabode)** has been called in as consultants by the stakeholders at GMS to set up a scalable data infrastructure system and build a solution that proactively leverages data to improve candidates’ performance in not just JAMB, but all their upcoming final exams. After a careful review of the state of the school's data system, the team has broken down the problem statement into the following objectives to be tackled.

## Objectives

1. Identify possible problems students might be facing while writing these exams
2. Since no concrete data was provided, we are required to generate data that adequately reflects the state of the Nigerian education ecosystem
3. Design an enterprise data solution for GMS’s data collection, pipelining, warehousing, automation, and reporting needs.
4. Create an optimized model that predicts the likelihood of a student passing or failing their upcoming exam based on their academic history while considering all factors that could affect a student's upcoming result aside from their previous exam scores.
5. Make relevant recommendations to the Stakeholders on how they can help improve the performance of the students based on your solution

The solution workflow can be seen below.

# Workflow
- [Background: Problem statement](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#background-problem-statement)
  - [Objectives](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#objectives)
- [School operations](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#school-operations)
- [Data generation, and infrastructure](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#data-generation-and-infrastructure)
  - [About the data](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#about-the-data)
- [Model development](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#model-development)
  - [How exam scores and other factors affected Science students' performance in an academic year](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#how-exam-scores-and-other-factors-affected-science-students-performance-in-an-academic-year)
  - [How exam scores and other factors affected Art students' performance in an academic year](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#how-exam-scores-and-other-factors-affected-art-students-performance-in-an-academic-year)
- [Data analysis](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#data-analytics)
  - [Data importation](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#data-importation)
  - [Data Cleaning/Preparation](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#data-cleaningpreparation)
  - [Exploratory Data Analysis](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#exploratory-data-analysis-eda)
  - [Further analysis](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#further-analysis-included)
  - [Data Visualization](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#data-visualization)
- [Recommendations](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#recommendations-1)
- [Conclusion](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#conclusion)
- [References](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#references)

# School operations
This refers to systems and principles by which the school - GMS- located in a typical African society follows. These systems guided our solution-building process.
1.	Compulsory extra-curricular activities. This includes sports and club activities.
2.	Each senior secondary school class has 6 subdivisions (A-F) and is further divided into Art and Science classes
3.	10 subjects are being offered by students in both specializations – Art and Science, with 5 subjects common between them.
4.	Each student is allowed to select between Art and Science
5.	An academic session in senior secondary school - GMS- is made up of three terms, each term comprising 3 months of dedicated studies


# Data generation and infrastructure
_Everything on the data engineering section of this project can be found [here](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024)._

GMS as we already established lacked a scalable data infrastructure system that allows for the school's data collection, pipelining, warehousing, automation, and reporting needs. Moreso, since the school provided no base data to work with, the task falls on us the consultants to create synthetic data that reflects the Nigeria secondary school ecosystem.

The primary goal here is to create rich, realistic datasets that can be used for educational data mining, predictive analytics, and decision support systems in the context of Nigerian secondary education. By simulating a complete school ecosystem, the datasets provide a valuable resource for school stakeholders, researchers, data scientists, and education policymakers to explore factors influencing student performance, resource allocation, and overall school management without compromising real student privacy.

To achieve this, Python libraries like Faker, Random, and Numpy were utilized to generate realistic-looking data while safeguarding student identities. The simulated data covers a broad range of areas, including student demographics, parent and staff information, academic performance, and extracurricular activities, all while incorporating Nigerian-specific elements like regions and states. The data is organized using a star schema design, ensuring efficient querying and analysis, and is saved in Parquet format for compatibility with big data tools. This dataset is stored in a data lake on Azure, as well as in a database like Postgres on Aiven, with a web interface developed for easy access and data entry. 

The [Data Collection Plan](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Data%20Collection%20Plan.pdf) further outlines the methods and tools used for data generation/ collection, pipelining, warehousing, automation, and reporting needs. The [Data warehouse dictionary](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Database%20Data%20Dictionary.pdf) provides detailed information about our data warehouse design, including database, schema, tables, relationships, data types, etc.

The database diagram for Goodness and Mercy School can be seen below: 

![Database diagram](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/main/Images/school_data_model.png)

To facilitate real-time data collection and updates, we developed a custom [web application](https://datafestschoolapp.streamlit.app/) using Streamlit. This application enables GMS school administrators to easily insert new data and update existing records for students, parents, staff, etc in the database. The app as seen below allows for seamless data entry, ensuring that the school's database remains current.

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/Streamlit%20app.JPG" alt="Streamlit app">
</p>

New data collected through this web interface is pushed to the PostgreSQL database where it is further connected to Microsoft Power BI where it handles the data reporting needs of the school as in the image below. 

<p align="center">
    <img width="1000" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/GMS_reporting%20needs.JPG" alt="Reporting needs">
</p>


### About the data

Based on the data generated we have the following tables:
1. students table: shows the bio-data for all different students in senior secondary schools
2. student_performance table: the historical record of students' exam scores. It contains aggregate records of students in the last academic session (2023/2024) in their respective subjects. P.S. The next academic session is 2024/2025.
3. class_resources_table: comprising the allocation of resources like functional fans, weekly library hours, etc for each class in the school.
4. parent_table: data on the parents of students at GMS
5. extracurricular_activity: information on the amount of time spent weekly by each student in an extracurricular activity
6. attendance_table: record of attendance level of students in each class for one academic year
7. ss3_student_survey: survey data on the factors impacting the academic performance of SS3 students
8. staff_table: contains details about every staff at GMS
9. teachers_table: details about all teachers at GMS



# Model development

The task here involves creating a predictive model that can adequately inform the stakeholders at GMS of the likelihood of a student passing or failing their upcoming exams. In this scenario, the upcoming exams refer to their mock exams written to prepare students for their JAMB and WASSCE exams. At GMS, if a student can do well in the mock exams, then they can do well in the JAMB and WASSCE exams. Furthermore, GMS is concerned about other factors that can affect a student's upcoming results aside from their previous exam scores in class and is open to recommendations based on that.

## Solution

The optimized model built is divided into two for art and for science students. The notebook [here](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Model%20development/Model%20development.ipynb) contains the comprehensive steps taken for model development and the final prediction models for the science and art categories. The steps taken include:
- Connection to PostgreSQL database (connection details and password can be found in the [notebook](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Model%20development/Model%20development.ipynb)).
- Data preparation
- Exploratory Data Analysis
- Data preprocessing
- Feature selection
- Model Training
- Testing phase
- Model evaluation

Additionally, we considered what factors played a role in determining the pass/fail rate of SS3 students. In the following section below, for both art and science students, we examined 5 additional factors aside from their exam scores that played an influential role in student's academic performance in an academic year.

### How exam scores and other factors affected Science students' performance in an academic year

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/Science%20students.JPG" alt="Science students">
</p>

In the Nigerian educational system, a student is usually considered for admission if he/she has at least 5 credit passes for relevant subjects in the WASSCE exams and a JAMB score that meets the cut-off mark (usually based on the school and the course of study).

From the plot above, aside from the 10 subjects that play a role in determining the pass/fail of a student, 5 other factors impacted students performance:

1. Number of study hours per week: this speaks to whether or not the students had enough number of hours to study per week. Were there other activities taking up this study time? EDA shows that the average number of hours spent per week by science students is 19.6 hours. Further analysis can reveal if this number of hours is enough or if increasing the number of study hours would improve student performance.

2. Extracurricular hours per week: at GMS, extracurricular activities are compulsory. Does the number of hours spent in weekly extracurriculars positively or negatively impact the student's performance? Would making extracurriculars optional improve the student's chances of performing better academically? Are the students unhappy with these extracurriculars being forced down their throats? Or does their participation in any of these clubs improve their academic performance? From our EDA, we noticed that science students spend between 1 - 10 hours weekly on extracurricular activities like sports or being part of the Jet club, debate club, drama club, etc.

3. Teacher Support: EDA revealed that 22% of the science students felt less support from the teachers while 23% felt the teachers provided enough support for them in class through the availability of these teachers to provide clarifications both within and outside the classroom. Could these percentages be attributed to the dense population of students in a class and the number of teachers

4. Parental support: A similar case applies here where 48% of the students stated an average level of support from parents. Where parental support includes:
   - Parental supervision of student's school work and grades
   - Parental overall attitude towards education and atmosphere at home (peaceful/quarrelsome, accommodating/tight-fisted).

To this point, research done by Uzochukwu and Uchechukwu (2023) (refer to the references section [below](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/tree/Data-science#references)) shows that unhealthy parenting wheels a tremendous negative influence on the schooling of secondary school students

5. Lack of resources & additional tutoring: Again, EDA showed that 17% of the science students at GMS noted a lack of necessary resources like textbooks, study guides, practical lessons, etc as a reason for their performance. It is known that study and practice make perfect but what happens when adequate resources/learning opportunities are limited for students to learn from? Also, aside from class teachings, are the students enrolled in extra lessons? 51% of the students reported not being enrolled in any additional lessons or tutoring.

At the end of the day, it does matter if a student is happy at school because according to the European Online Journal of Natural and Social Sciences, there is “a significant positive relationship between happiness and achievement of students.” The authors (Tabbodi, Rahgozar, Mozaffari, and Abadi, 2015) of the study also found a significant correlation “between happiness and the progress of students, stating that an increase or decrease in happiness increases or decreases the level of academic achievement.”

The questions posed here and in the next section guide our analysis to provide answers to these questions and offer proactive measures and recommendations tat can be put in place to ensure that an overwhelming majority passes their upcoming exams.

### How exam scores and other factors affected Art students' performance in an academic year

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/Art%20students.JPG" alt="Art students">
</p>

Similar to science students, art students would need to meet a university school's criteria before gaining admission.

Again, aside from the subjects being offered other factors included:

- Study hours per week
- Extracurricular hours
- Teacher support
- Parental support
- Health issues

The same reasoning for science students also applies to art students since they share similar characteristics or factors that affect their overall performance. The exception here is that 54% of art students (according to EDA) noted that their academic performance was due to health challenges they experienced within their academic here. 

# Data Analytics

## Data Importation

The required datasets (attendance, class resources, extracurricular activities, parental involvement, SS3 student surveys, staff, student performance, student information, and teachers) were imported as CSV files into MySQL Workbench for structured analysis. [SQL queries](https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Analysis/Analysis_queries.sql) were used for data cleaning, manipulation, and analysis within MySQL. After processing, the data was exported to Power BI for visualization and advanced analysis. You can interact with the dashboard [here](https://app.powerbi.com/view?r=eyJrIjoiNTI5YTcyZDEtZTZkMS00ODBlLWFlNGYtMjhiMGJkMzRhYTc4IiwidCI6IjJkMGNjMjNiLWEwNGUtNDg5MS1iYjM0LTZmYTQzODJlZGFmYyJ9&pageName=f3a6bd0614a41d032dd9).

## Data Cleaning/Preparation
This included:
- Checking for missing values in core subjects such as Mathematics, English Language, Civic Education, Economics, and CRS/Islam.
- Identifying and resolving duplicate records in the student_performance table to ensure data integrity.
- Creating a new column - average_score- to calculate students' average scores across all subjects.

## Exploratory Data Analysis (EDA)
The EDA process revealed some Key Performance Indicators (KPIs) for GMS, including:
- Total number of students: 983.
- Average attendance rate: 99.67%. Students had a high attendance rate at school throughout the academic year being considered (2023/2024). There were cases of absenteeism which were attributed to cases like illnesses, insecurity (given that the school is located in the northern part of Nigeria), etc.
- Percentage of students participating in extracurricular activities: 100%. This is explained given the fact that all students are mandated to be a part of an extracurricular activity
- Average weekly study hours: 19.93 hours. For senior secondary school at GMS, students are allocated approximately 20 hours of study on average.
- Teacher-to-student ratio: 1:65.

Ogunode Niyi Jacob, & Ahaotu Godwin Ndubuisi (2020) in their research noted the standard for teacher-to-student ratio as 1:40 for secondary schools. However, GMS fails to adhere to this standard, thereby joining other educational institutions in the country with overpopulated classrooms. 

- Gender distribution: 50.15% female, 49.85% male. There is a healthy ratio of males to females with only a slight difference in distribution.

## Further analysis included

1. Performance Distribution: Performance was analyzed across different classes and segments (SS1, SS2, SS3). It was found that attendance had no significant correlation with student performance.

2. Correlation Analysis:

- Attendance vs. Performance: No significant correlation between attendance days and average performance scores.
- Study Hours vs. Performance: Weekly study hours showed no strong relationship with student performance.
- Resource Access vs. Performance: Students with resource access scored slightly higher (34 vs. 33).
- Parental Involvement: Students with highly involved parents performed marginally better (25.12%) than others.
- Extracurricular Participation: Students involved in arts, debate club, and press club achieved slightly better average scores (34), whereas those in literature and drama had marginally lower scores (32-33).

3. Class Segment Analysis:
- Class-based Performance: SS1 Class E had the highest average performance (35.11), while SS1 Class D had the lowest (31.00).
- Resource Allocation: Teaching hours, textbooks, and teachers showed slight positive effects on performance, though the impact was minimal.

4. Factor Analysis: While resource access, parental involvement, and extracurricular participation showed slight correlations with higher average scores, attendance and study hours did not demonstrate strong correlations.

## Data Visualization

The dashboard can be found [here](https://app.powerbi.com/view?r=eyJrIjoiNTI5YTcyZDEtZTZkMS00ODBlLWFlNGYtMjhiMGJkMzRhYTc4IiwidCI6IjJkMGNjMjNiLWEwNGUtNDg5MS1iYjM0LTZmYTQzODJlZGFmYyJ9&pageName=f3a6bd0614a41d032dd9)

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest-Datathon-2024/blob/Data-science/Images/Student%20performance%20dashboard.JPG" alt=" Dashboard">
</p>

## Recommendations
1. Optimize Study Hours

The current average study time of 20 hours per week for students showed no strong correlation with academic performance. GMS needs to reassess the quality of these study hours rather than just increasing them. Conducting workshops on effective study techniques and providing personalized study plans may yield better outcomes.

2. Increase Teacher Support

With 22% of science students feeling unsupported by teachers, there is a need for more teacher-student engagement. GMS should invest in teacher development programs aimed at improving in-class and out-of-class support. Additionally, the teacher-student ratio of 1:65 is above the recommended standard of 1:40. Hiring more teachers could greatly reduce the class size, improve individual attention, and likely increase overall academic performance.

3. Parental Involvement
Students with highly involved parents performed slightly better. Since parental involvement has shown a positive correlation with student performance, GMS should actively engage parents in their children’s academic lives. Initiatives such as regular progress updates, parent-teacher meetings, and workshops that emphasize the importance of educational support can help increase parental participation. A focused effort on improving the home environment for learning could further enhance student outcomes

4. Extracurricular Programs
Students participating in Debates, Press Club, and Arts extracurriculars scored higher. Expanding these programs or encouraging greater student participation could improve overall engagement and performance. However, some students may feel that extracurricular activities are being forced upon them and are therefore taking a lot of their time. GMS should conduct surveys to assess students' satisfaction with extracurricular activities and adjust the program to align more with students' interests and academic needs, potentially enhancing both student happiness and performance

5. Balanced Resource Distribution
Classes with more resources, such as textbooks and teaching hours, showed slight performance improvements. Schools should ensure the equitable distribution of resources to provide all students with similar opportunities.

6. Health and Well-being

A significant number of art students (54%) attributed their academic struggles to health issues. GMS should provide better health support, including access to school counselors and healthcare services, and promote initiatives aimed at improving students’ overall well-being. A healthy student body is more likely to succeed academically.


# Conclusion

With the aforementioned recommendations, GMS can act proactively with this new information to make the necessary adjustments required ensuring a more balanced and supportive learning environment that boosts academic achievement. 

Additionally, the optimized model created provides a data-backed approach for GMS stakeholders to tell whether or not a student with certain scores and responses to highlighted factors would either pass or fail their upcoming mock exams. As for GMS data collection and automation needs, the data infrastructure is built in a way that accommodates expansion and scalability as needed. 

In conclusion, the Phoneix team consultancy believes that her solution is implementable if followed as directed.

# References

This consists of a list of journals, articles, and websites consulted which aided our solution-building process. 

1. Afe Babalola University. (2024). The decline in quality education in Nigeria (2) The role of parents in a child’s education. – Afe Babalola University. Abuad.edu.ng. https://www.abuad.edu.ng/the-decline-in-quality-education-in-nigeria-2/
2. Aiven. (2024). How to Connect to PostgreSQL Database from Power BI. Aiven Community. https://aiven.io/community/forum/t/how-to-connect-to-postgresql-database-from-power-bi/1384
3. Azure-storage-blob. (2024). PyPI. https://pypi.org/project/azure-storage-blob/
4. Faker 30.3.0 documentation. (n.d.). Welcome to Faker’s documentation! — Faker 5.0.1 documentation. Faker.readthedocs.io. https://faker.readthedocs.io/en/master/
5. FreeCodeCamp. (2024). “Basic Node and Express - Use the .env File” - .env should be removed from .gitignore. The FreeCodeCamp Forum. https://forum.freecodecamp.org/t/basic-node-and-express-use-the-env-file-env-should-be-removed-from-gitignore/668556
6. GitHub. (2024). GitHub Actions Documentation - GitHub Docs. Docs.github.com. https://docs.github.com/en/actions
7. Microsoft. (n.d.). Azure Blob Storage | Microsoft Azure. Azure.microsoft.com. https://azure.microsoft.com/en-us/products/storage/blobs
8. National Bureau of Statistics. (n.d.). Reports | National Bureau of Statistics. Nigerianstat.gov.ng. https://nigerianstat.gov.ng/elibrary/read/1241213?fbclid=IwAR3Wi9f-o20ZMM0v5hgIE5AmLQPV6dc25vCRE88UFmYlwVawveWfNO-c-lE
9. Nuffic. (2023). Primary and secondary education - Nigeria | Nuffic. Nuffic.nl. https://www.nuffic.nl/en/education-systems/nigeria/primary-and-secondary-education
10. Ogunode Niyi Jacob, & Ahaotu Godwin Ndubuisi. (2020). Challenges Facing the Implementation of Teacher-Students Ratio Policy in Nigerian Educational System and the Ways Forward. International Journal on Integrated Education, 3(9), 189–197. https://doi.org/10.31149/ijie.v3i9.619
11. Olaitan Titilayo Akinola, Abiodun Adesope Fadiya, Ibukun Akeredolu, & Funmilola, H. (2023). Impact of Class Size on Teaching and Learning of Social Studies in Abuja Municipal Area Council, FCT-Abuja, Nigeria. Journal of Education and Practice. https://doi.org/10.7176/jep/14-19-06
12. Streamlit. (2024). Execution flow - Streamlit Docs. Streamlit.io. https://docs.streamlit.io/develop/api-reference/execution-flow
13. Tabbodi, M., Rahgozar, H., Mozaffari, M., & Abadi, M. (2015). The Relationship between Happiness and Academic Achievements. In European Online Journal of Natural and Social Sciences.
14. Techpoint Africa. (2023). How much do Nigerians earn? https://techpoint.africa/2023/11/06/how-much-do-nigerians-earn/
15. Uzochukwu, O., & Uchechukwu Okorie, H. (2023). Impact Of Unhealthy Parenting On Schooling Of Secondary School Students In Anambra State-Nigeria: Gender As A Mediating Variable.

# Improving  Academic Outcome For Secondary Education in Nigeria -- DataFestAfrica Hackathon 2024

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Images/Secondary%20school%20kids.jpg" alt="Secondary school kids">
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
- [Background: Problem statement](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#background-problem-statement)
  - [Objectives](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#objectives)
- [School operations](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#school-operations)
- [Data generation, and infrastructure](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#data-generation-and-infrastructure)
  - [About the data](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#about-the-data)
- [Model development](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#model-development)
- [Data analysis](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#data-analytics)
- [Recommendations]()
  - Solution statement
- [Conclusion](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#conclusion)
- [References](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/README.md#references)

# School operations
This refers to systems and principles by which the school - GMS- located in a typical African society follows. These systems guided our solution building process.
1.	Compulsory extra-curricular activities. This includes sports and club activities.
2.	10 subjects are being offered by students in both specializations – Art and Science, with 5 subjects common between them.
3.	Each senior secondary school class has 6 subdivisions (A-F) and is further divided into Art and Science classes
4.	Each student is allowed to select between Art and Science
5.	An academic session in senior secondary school - GMS- is made up of three terms, each term comprising 3 months of dedicated studies


# Data generation, and infrastructure

GMS as we already established lacked a scalable data infrastructure system that allows for the school's data collection, pipelining, warehousing, automation, and reporting needs. Moreso, since the school provided no base data to work with, the task falls on us the consultants to create synthetic data that reflects the Nigeria secondary school ecosystem.

## Data generation

The primary goal here is to create rich, realistic datasets that can be used for educational data mining, predictive analytics, and decision support systems in the context of Nigerian secondary education. By simulating a complete school ecosystem, the datasets provide a valuable resource for researchers, data scientists, and education policymakers to explore factors influencing student performance, resource allocation, and overall school management without compromising real student privacy.

To create a synthetic dataset that respects student privacy, we leveraged Python libraries like Faker, random, and Numpy to generate a substantial amount of realistic-looking data without compromising real students' personal information. The following were put in place:

- School Structure: The simulated school is modeled after a typical Nigerian secondary school, featuring Senior Secondary (SS) classes from SS1 to SS3, each divided into segments A through F. This structure accurately reflects the common organization of Nigerian secondary education.

- Diverse Data Points: To ensure comprehensive analysis, we generated a wide range of data points, including student demographics, parent information, staff details, class resources, academic performance, attendance records, and extracurricular activities. This multifaceted approach enables in-depth exploration of various aspects of the school environment.

- Nigerian Context: To make the data more authentic, we incorporated Nigerian-specific elements such as regions, states, and name patterns. This aligns the dataset with the unique characteristics of the Nigerian educational context.

- Interconnected Tables: The data is organized into interconnected tables, following a star schema design. This structure is well-suited for data warehousing and facilitates efficient querying and analysis.

- Realistic Constraints: To maintain data realism, we implemented realistic constraints and distributions. For example, the number of students per class, the range of test scores, and the distribution of health conditions were designed to reflect real-world scenarios.

- Flexibility and Scalability: our approach ensures flexibility and scalability by allowing for easy adjustment of the dataset size and modification of parameters. This adaptability makes the dataset suitable for various research questions and analytical needs.

- Data Quality Checks: To ensure data integrity, I implemented data quality checks before saving the data as parquet files. These checks help maintain the accuracy and reliability of the dataset.

Parquet Output: All generated data is saved as parquet files. Parquet is an efficient storage format that enables faster data access and better compatibility with big data tools.

Data Storage and Access: The dataset is stored in a data lake on Azure and on a database like Postgres on Aiven. Additionally, a web interface is developed to allow for easy data input and access.



The database diagram for Goodness and Mercy School can be seen below:

![alt text](https://github.com/George-Michael-Dagogo/Datafest/blob/main/Images/school_data_model.png)


## About the data

Based on the data generated:
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

The task here involves creating a forecasting model that can adequately inform the stakeholders at GMS of the likelihood of a student passing or failing their upcoming exams. In this scenario, the upcoming exams refer to their mock exams written to prepare students for their JAMB and WASSCE exams. At GMS, if a student can do well in the mock exams, then they can do well in the JAMB and WASSCE exams. Furthermore, GMS is concerned about other factors that can affect a student's upcoming results aside from their previous exam scores in class and is open to recommendations based on that.

## Solution

The optimized model built is divided into two for art and for science students. The notebook [here](https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Model%20development/Model%20development.ipynb) contains the comprehensive steps taken for model development and the final prediction models for the science and art categories.


<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Images/Science%20students.JPG" alt="Science students">
</p>

In the Nigerian educational system, a student is usually considered for admission if he/she has at least 5 credit passes for relevant subjects in the WASSCE exams and a JAMB score that meets the cut off mark (usually based on the school and the course of study).

From the plot above, asides from the 10 subjects that play a role in determining the pass/fail of a student, there were 5 other factors that impacted students performance:

1. Number of study hours per week: this speaks to whether or not the students had enough number of hours to study per week. Were they other activities taking up this study time? EDA shows that the average number of hours spent per week by science students is 19.6 hours. Further analysis can reveal if this number of hours is enough or if increasing the number of study hours would improve student performance.

2. Extracurricular hours per week: at GMS, extracurricular activities are compulsory. Does the number of hours spent in weekly extracurriculars positively or negatively impact the student's performance? Would making extracurriculars optional improve the student's chances of performing better academically? Are the students unhappy with these extracurriculars being forced down their throats? From our EDA, we noticed that science students spend between 1 - 10 hours weekly on extracurricular activities like sports or being part of the Jet club, debate club, drama club, etc.

3. Teacher Support: EDA revealed that 22% of the science students felt less support from the teachers while 23% felt the teachers provided enough support for them in class through the availability of these teachers to provide clarifications both within and outside the classroom.

4. Parental support: A similar case applies here where 48% of the students stated an average level of support from parents. Where parental support includes:
   - Parental supervision of student's school work and grades
   - Parental overall attitude towards education and atmosphere at home (peaceful/quarrelsome, accommodating/tight-fisted).

To this point, research done by Uzochukwu and Uchechukwu (2023) (refer to the references section) shows that unhealthy parenting wheels a tremendous negative influence on the schooling of secondary school students

5. Lack of resources & additional tutoring: Again, EDA showed that 17% of the science students at GMS noted a lack of necessary resources like textbooks, study guides, practical lessons, etc as a reason for their performance. It is known that study and practice make perfect but what happens when adequate resources/avenues are unavailable for students to learn from? Also, aside from class teachings, are the students enrolled in extra lessons? 51% of the students reported not being enrolled in any additional lessons or tutoring.

The questions posed here are experiments the management at GMS can carry out, collect data from, and analyze whether there was a change in academic performance.

At the end of the day, it does matter if a student is happy at school because according to the European Online Journal of Natural and Social Sciences, there is “a significant positive relationship between happiness and achievement of students.” The authors (Tabbodi, Rahgozar, Mozaffari, and Abadi, 2015) of the study also found a significant correlation “between happiness and the progress of students… an increase or decrease in happiness increases or decreases the level of academic achievement.”


<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Images/Art%20students.JPG" alt="Art students">
</p>


Similar to science students, art students would need to meet a university school's criteria before gaining admission.

Again, aside from the subjects being offered other factors included:

- Study hours per week
- Extracurricular hours
- Teacher support
- Parental support
- Health issues

The same reasoning for science students also applies to art students since they share similar characteristics or factors that affect their overall performance. The exception here is that 54% of art students (according to EDA) noted that their academic performance was due to health challenges they experienced.



# Data Analytics


# Recommendations



# Conclusion



# References

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



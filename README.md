# Improving  Academic Outcome For Secondary Education in Nigeria -- DataFestAfrica Hackathon 2024

<p align="center">
    <img width="600" src="https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Images/Secondary%20school%20kids.jpg" alt="Secondary school kids">
</p>
<div align="center">
  <p style="font-size: 7px;"><i>© UNICEF/UN0270198/Knowles-Coursin</i></p>
</div>


# Background: Problem statement

Goodness and Mercy School (GMS) is what we can call a budget private primary and secondary school in Kaduna South local government of Kaduna state, Nigeria. A hypothetical situation featured a stakeholders meeting highlighting the lack of infrastructure for digital data collection plus the inadequate paper records being kept. Also, the results from the 2024 UTME showed that 76% (approx. 4 out of 5) of students who participated in the 2024 UTME scored [less than 200](https://www.premiumtimesng.com/news/690022-updated-jamb-releases-2024-utme-results-76-scores-below-200.html). This has raised a huge concern for the stakeholders and hence they have decided to take proactive measures to guard against this failure rate for their next batch of students in their upcoming final exams and consequently the JAMB and WASSCE exams.

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
- [Background]()
  - Objectives
- [School operation]()
- [Data collection/generation]()
  - About the data
- [Data infrastructure]()
- [Model development and deployment]()
- [Data analysis]()
- [Recommendations]()
  - Solution statement
- [Conclusion]()
- [References]()

# School operations
This refers to systems and principles by which the school - GMS- loacted in a typical african society follows. These systems guided our solution
1.	Compulsory extra-curricular activities. This includes sports and club actvities.
2.	10 subjects are being offered by students in both specializations – Art and Science, with 5 subjects common between them.
3.	Each senior secondary school class has 6 subdivisions (A-F) and is further divided into Art and Science classes
4.	Each student is allowed to select between Art and Science
5.	An academic session in senior secondary school - GMS- is made up of three terms, each term comprising 3 months of dedicated studies


## About the data

Based on the data generated:
1. students table: shows the bio-data for all different students in senior secondary schools
2. student_performance table: the historical record of students' exam scores. It contains aggregate records of students in the last academic session (2023/2024) in their respective subjects. P.S. The next academic session is 2024/2025.



# Model development and deployment

The task here involves creating a forecasting model that can adequately inform the stakeholders at GMS of the likelihood of a student passing or failing their upcoming exams. In this scenario, the upcoming exams refer to their mock exams written to prepare students for their JAMB and WASSCE exams. At GMS, if a student can do well in the mock exams, then they can do well in the JAMB and WASSCE exams. Furthermore, GMS is concerned about other factors that can affect a student's upcoming results aside from their previous exam scores in class.

## Solution

The optimized model built is divided into two for art and for science students. The notebook [here]() contains the comprehensive steps taken.

1. Connecting to the postgresql
2. Joining relevant tables - student_performance, students, extracurricular, and ss3_student_survey tables
Below is a view of all the columns in the final table

<p align="center">
    <img width="300" src="https://github.com/George-Michael-Dagogo/Datafest/blob/Data-science/Images/Table_information.JPG" alt="Table_information">
</p>

3. Exploratory data analysis
   - No missing values was identified









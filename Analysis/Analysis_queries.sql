-- DATA CLEANING

-- Check for missing values
SELECT * FROM student_performance 
WHERE Mathematics IS NULL OR English_Language IS NULL OR Civic_Education OR Economics OR CRS_Islam;

-- Check for duplicates
SELECT student_id, COUNT(*) 
FROM student_performance
 GROUP BY student_id 
 HAVING COUNT(*) > 1;
 
 -- Exploratory Data Analysis (EDA)
 
 -- Add the average_score column
 ALTER TABLE student_performance 
ADD average_score DECIMAL(5, 2);

UPDATE student_performance
SET average_score = (
    (mathematics + English_language + Civic_education + economics + 
     crs_islam + physics + chemistry + biology + 
     geography + computer_science + government + 
     commerce + literature + history + accounting) / 15);
     
     -- KPIs 
     
-- Total Number of Students
SELECT COUNT(*) AS total_students
FROM student_table;

-- Average Attendance Rate
SELECT AVG((days_attended / (days_attended + days_missed)) * 100) AS avg_attendance_rate
FROM attendance_table;

-- Percentage of Students Participating in Extracurricular Activities
SELECT (COUNT(DISTINCT student_id) / (SELECT COUNT(*) 
FROM student_table)) * 100 AS extracurricular_participation_rate
FROM extracurricular_activity;

-- Percentage of Attendance to Non-Attendance
SELECT (SUM(days_attended) / (SUM(days_attended) + SUM(days_missed))) * 100 AS attendance_rate
FROM attendance_table;

-- Average Weekly Study Hours (SS3 Student Survey)
SELECT AVG(study_hours_per_week) AS avg_weekly_study_hours
FROM SS3_student_survey;

-- Teacher-to-Student Ratio
SELECT (SELECT COUNT(*) 
FROM student_table) / (SELECT COUNT(*) 
FROM staff_table 
WHERE position = 'Teacher') AS teacher_to_student_ratio;

-- Percentage of Male to Female Students
SELECT 
    (SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS male_percentage,
    (SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS female_percentage
FROM student_table;

    
 -- a) Student Performance Distribution Across Segments:
 -- Gender-based Performance Distribution:
SELECT s.gender, 
AVG(sp.Mathematics) AS Avg_Maths, 
AVG(sp.English_Language) AS Avg_Eng,
AVG(sp.Civic_Education) AS Avg_Civic,
AVG(sp.CRS_Islam) AS Avg_Religion,
AVG(sp.Economics) AS Avg_Econs
FROM student_performance AS sp
JOIN student_table AS s 
ON sp.student_id = s.student_id
GROUP BY s.gender;

-- Class-based Performance Distribution:
SELECT s.class_id, 
AVG(sp.Mathematics) AS Avg_maths, 
AVG(sp.English_Language) AS Avg_Eng,
AVG(sp.Civic_Education) AS Avg_Civic,
AVG(sp.CRS_Islam) AS Avg_Religion,
AVG(sp.Economics) AS Avg_Econs
FROM student_performance AS sp
JOIN student_table AS s 
ON sp.student_id = s.student_id
GROUP BY s.class_id;

-- Attendance-based Performance Distribution:
SELECT a.days_attended, 
AVG(sp.Mathematics) AS Avg_maths, 
AVG(sp.English_Language) AS Avg_Eng,
AVG(sp.Civic_Education) AS Avg_Civic,
AVG(sp.CRS_Islam) AS Avg_Religion,
AVG(sp.Economics) AS Avg_Econs
FROM attendance_table AS a
JOIN student_performance AS sp 
ON a.student_id = sp.student_id
GROUP BY a.days_attended;

-- Parental Involvement and Performance:
SELECT p.involvement_in_kids_education, 
AVG(sp.Mathematics) AS Avg_maths, 
AVG(sp.English_Language) AS Avg_Eng,
AVG(sp.Civic_Education) AS Avg_Civic,
AVG(sp.CRS_Islam) AS Avg_Religion,
AVG(sp.Economics) AS Avg_Econs
FROM parent_table AS p
JOIN student_performance AS sp 
ON p.student_id = sp.student_id
GROUP BY p.involvement_in_kids_education;

 -- Average score of all the sujects and overall average
 SELECT 
    AVG(Mathematics) AS average_maths,
    AVG(English_Language) AS average_english,
    AVG(Civic_Education) AS average_civic_education,
    AVG(economics) AS average_economics,
    AVG(CRS_Islam) AS average_crs_islam,
    AVG(physics) AS average_physics,
    AVG(chemistry) AS average_chemistry,
    AVG(biology) AS average_biology,
    AVG(geography) AS average_geography,
    AVG(computer_science) AS average_computer_science,
    AVG(government) AS average_government,
    AVG(commerce) AS average_commerce,
    AVG(literature) AS average_literature,
    AVG(History) AS average_history,
    AVG(accounting) AS average_accounting,
    (AVG(Mathematics) + AVG(English_Language) + AVG(Civic_Education) + AVG(economics) + 
     AVG(crs_islam) + AVG(physics) + AVG(chemistry) + AVG(biology) + 
     AVG(geography) + AVG(computer_science) + AVG(government) + 
     AVG(commerce) + AVG(literature) + AVG(history) + AVG(accounting)) / 15 AS overall_average
FROM student_performance;

-- b) Correlation Between Key Variables (Attendance, Study Hours, Performance):
-- Attendance vs. Performance:
SELECT a.days_attended, avg(average_score) AS avg_score
FROM attendance_table AS a
JOIN student_performance sp 
ON a.student_id = sp.student_id
GROUP BY a.days_attended;

-- Study Hours vs. Performance:
SELECT ss.study_hours_per_week, AVG(average_score) AS avg_score
FROM SS3_student_survey AS ss
JOIN student_performance AS sp
 ON ss.student_id = sp.student_id
GROUP BY ss.study_hours_per_week;

-- Resource Access vs. Performance:
SELECT ss.access_to_resources, AVG(average_score) AS avg_score
FROM SS3_student_survey AS ss
JOIN student_performance AS sp 
ON ss.student_id = sp.student_id
GROUP BY ss.access_to_resources;

-- Factor Analysis & Insights
-- Analyzing Factors Affecting Student Performance
-- Factors with Strongest Correlation:
-- Parental Involvement:
SELECT p.involvement_in_kids_education, AVG(average_score) AS avg_score
FROM parent_table AS p
JOIN student_performance AS sp 
ON p.student_id = sp.student_id
GROUP BY p.involvement_in_kids_education;

-- Extracurricular Participation vs. Performance:
SELECT e.extracurricular_activity, AVG(sp.average_score) AS avg_score
FROM extracurricular_activity AS e
JOIN student_performance AS sp 
ON e.student_id = sp.student_id
GROUP BY e.extracurricular_activity
ORDER BY avg_score DESC;

-- Class Segment Performance:
SELECT s.class_id, AVG(average_score) AS avg_score
FROM student_performance AS sp
JOIN student_table AS s 
ON sp.student_id = s.student_id
GROUP BY s.class_id
ORDER BY avg_score DESC;

-- Resource Allocation and Student Performance:
SELECT 
    cr.weekly_teaching_hours, 
    cr.Basic_Textbooks, 
    cr.Number_of_Teachers,
    AVG(sp.average_score) AS avg_score
FROM class_resources_table AS cr
JOIN student_table AS s 
    ON cr.class_name = s.class_id
JOIN student_performance AS sp
    ON s.student_id = sp.student_id
GROUP BY cr.weekly_teaching_hours, cr.Basic_Textbooks, cr.Number_of_Teachers;

-- Attendance and Performance:
SELECT a.days_missed, AVG(average_score) AS avg_score
FROM attendance_table AS a
JOIN student_performance AS sp 
ON a.student_id = sp.student_id
GROUP BY a.days_missed;

SELECT s.gender, 
COUNT(*) AS count
FROM student_table AS s
GROUP BY s.gender;
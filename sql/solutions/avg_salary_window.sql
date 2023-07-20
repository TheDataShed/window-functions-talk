-- The difference to the average salary for each person
SELECT first_name
     , department
     , salary
     , ROUND((salary - AVG (salary) OVER (
         PARTITION BY department
       )), 0) AS avg_salary_diff
FROM   employees
ORDER
    BY avg_salary_diff
;

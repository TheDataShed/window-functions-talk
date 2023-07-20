-- The difference to the average salary for their department for each person

SELECT first_name
     , department
     , salary
     -- The difference between an employee's salary
     -- and the average for their department
     , ROUND((salary - AVG (salary) OVER (
         PARTITION BY department
       )), 0) AS avg_salary_diff
FROM   employees
ORDER
    BY avg_salary_diff
;

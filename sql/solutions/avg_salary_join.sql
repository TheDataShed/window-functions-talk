-- The difference to the average salary for their department for each person

-- A CTE for the average salary per department
WITH avg_salaries AS (
    SELECT department
         , AVG (salary) AS avg_salary
    FROM   employees
    GROUP
        BY department
)
SELECT employees.first_name
     , employees.department
     , employees.salary
     -- The difference between an employee's salary
     -- and the average for their department
     , ROUND(employees.salary - avg_salaries.avg_salary, 0) AS avg_salary_diff
FROM   employees
INNER
  JOIN avg_salaries
    ON employees.department = avg_salaries.department
ORDER
    BY avg_salary_diff
;

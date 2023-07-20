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
     , ROUND(employees.salary - avg_salaries.avg_salary, 0) AS avg_salary_diff
FROM   employees
INNER
  JOIN avg_salaries
    ON employees.department = avg_salaries.department
ORDER
    BY avg_salary_diff
;

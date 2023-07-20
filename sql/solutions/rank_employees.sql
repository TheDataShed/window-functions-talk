-- Employees ranked by salary
SELECT first_name
     , department
     , salary
     , RANK () OVER (
         ORDER BY salary DESC
       ) AS salary_rank
FROM   employees
;
-- Employees ranked by salary per department
-- SELECT first_name
--      , department
--      , salary
--      , RANK () OVER (
--          PARTITION BY department
--          ORDER BY salary DESC
--        ) AS salary_rank
-- FROM   employees
-- ;

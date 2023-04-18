SELECT *,
    RANK () OVER (ORDER BY salary desc)
FROM employees
;

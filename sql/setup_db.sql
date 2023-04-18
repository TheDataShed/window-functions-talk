DROP TABLE IF EXISTS website_visits
;

CREATE TABLE website_visits (
    user_id int,
    website_id int,
    event_datetime timestamp
)
;

DROP TABLE IF EXISTS website_sessions
;

CREATE TABLE website_sessions (
    user_id int,
    website_id int,
    event_datetime timestamp,
    session_id varchar(255)
)
;

DROP TABLE IF EXISTS employees
;

CREATE TABLE employees (
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    phone varchar(255),
    department varchar(255),
    job_title varchar(255),
    experience_years int,
    salary int
)
;

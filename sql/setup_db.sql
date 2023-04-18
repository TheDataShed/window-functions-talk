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

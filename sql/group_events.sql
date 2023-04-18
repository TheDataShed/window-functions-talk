with previous_times AS (
    SELECT
        user_id,
        website_id,
        event_datetime,
        LAG(event_datetime, 1) OVER(
            PARTITION BY user_id, website_id
            ORDER BY event_datetime
        ) AS previous_event_datetime
    FROM
        website_visits
),
time_differences AS (
    SELECT
        user_id,
        website_id,
        event_datetime,
        CASE
            WHEN previous_event_datetime IS NULL THEN 1
            WHEN EXTRACT(EPOCH FROM (event_datetime - previous_event_datetime)) >= 1800 THEN 1
            ELSE 0
        END AS new_session_required
    FROM
        previous_times
),
counted_session_resets AS (
    SELECT
        user_id,
        website_id,
        event_datetime,
        SUM(new_session_required) OVER(
            PARTITION BY user_id, website_id
            ORDER BY event_datetime
        ) AS session_reset_count
    FROM
        time_differences
),
session_ids AS (
    SELECT
        user_id,
        website_id,
        event_datetime,
        -- Datetime of the first value in each partition
        FIRST_VALUE(event_datetime) OVER(
            PARTITION BY user_id, website_id, session_reset_count
            ORDER BY event_datetime
        ) AS session_datetime,
        -- Generate a session ID for the first value in each partition
        FIRST_VALUE(
            MD5(
                CONCAT(
                    user_id,
                    '-',
                    website_id,
                    '-',
                    TO_CHAR(event_datetime, 'YYYY-MM-DD"T"HH12:MM:SS')
                )
            )
        ) OVER(
            PARTITION BY user_id, website_id, session_reset_count
            ORDER BY event_datetime
        ) AS session_id
    FROM
        counted_session_resets
)
SELECT
    *
FROM
    session_ids
;

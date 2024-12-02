SELECT pid, usename, application_name, state, query, age(clock_timestamp(), query_start) AS runtime
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY runtime DESC;

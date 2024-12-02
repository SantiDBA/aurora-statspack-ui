SELECT relname AS table_name, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
FROM pg_stat_all_tables
ORDER BY seq_scan DESC LIMIT 10;

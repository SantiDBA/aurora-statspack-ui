SELECT snap_id, snap_timestamp 
FROM statspack.hist_snapshots 
WHERE snap_id in ( %(begin_snap)s , %(end_snap)s )
ORDER BY snap_id;
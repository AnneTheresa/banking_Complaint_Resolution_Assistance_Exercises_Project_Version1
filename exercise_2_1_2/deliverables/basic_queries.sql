

-- 1
SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    c.channel,
    c.category,
    c.priority,
    c.status,
    c.received_at,
    c.assigned_analyst_id
FROM complaint AS c
WHERE c.status = 'OPEN'
ORDER BY c.received_at DESC, c.complaint_id ASC;


-- 2
SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    c.channel,
    c.category,
    c.priority,
    c.status,
    c.received_at,
    c.assigned_analyst_id
FROM complaint AS c
WHERE c.priority = 'High'
  AND c.status IN ('OPEN', 'IN_PROGRESS', 'UNDER_REVIEW')
ORDER BY c.received_at DESC, c.complaint_id ASC;


-- 3. Count complaints by status.
SELECT
    c.status,
    COUNT(*) AS complaint_count
FROM complaint AS c
GROUP BY c.status
ORDER BY complaint_count DESC, c.status ASC;



-- 4. Count complaints by category.
SELECT
    c.category,
    COUNT(*) AS complaint_count
FROM complaint AS c
GROUP BY c.category
ORDER BY complaint_count DESC, c.category ASC;



-- 5. Show complaints for a supplied customer ID.
SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    c.channel,
    c.category,
    c.priority,
    c.status,
    c.received_at,
    c.assigned_analyst_id
FROM complaint AS c
WHERE c.customer_id = :customer_id
ORDER BY c.received_at DESC, c.complaint_id ASC;

-- 6
SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    c.channel,
    c.category,
    c.priority,
    c.status,
    c.received_at,
    c.assigned_analyst_id
FROM complaint AS c
WHERE c.received_at >= datetime(:start_date)
  AND c.received_at < datetime(:end_date, '+1 day')
ORDER BY c.received_at ASC, c.complaint_id ASC;



-- 7.
SELECT
    c.complaint_id,
    c.customer_id,
    c.status,
    c.received_at
FROM complaint AS c
WHERE c.status = 'CLOSED'
  AND NOT EXISTS (
      SELECT 1
      FROM complaint_status_history AS h
      WHERE h.complaint_id = c.complaint_id
        AND h.new_status = 'CLOSED'
        AND h.changed_at IS NOT NULL
  )
ORDER BY c.complaint_id ASC;

-- 8. Show ten most recently opened complaints.
SELECT
    c.complaint_id,
    c.customer_id,
    c.account_id,
    c.channel,
    c.category,
    c.priority,
    c.status,
    c.received_at,
    c.assigned_analyst_id
FROM complaint AS c
ORDER BY c.received_at DESC, c.complaint_id ASC
LIMIT 10;
-- END Q8

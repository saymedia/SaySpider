
-- average page load time
SELECT SUM(response_time) AS total_response_time
	 , SUM(articles) AS articles
	 , SUM(response_time)/SUM(articles) AS average_response_time

FROM (
	SELECT SUM(response_time) AS response_time
	     , COUNT(1) AS articles
	  FROM page
	 WHERE external = 0
	   AND origin_host = 'readwrite_com'
	 UNION 
	SELECT SUM(response_time) AS response_time
		 , COUNT(1) AS articles
	 FROM asset 
	WHERE external = 1
	  AND origin_host = 'readwrite_com'
	) sub



-- status code counts
SELECT status_code
	 , sum(counts)

FROM (
	SELECT status_code
	     , COUNT(1) AS counts
	  FROM page
	 WHERE external = 0
	   AND origin_host = 'readwrite_com'
	 GROUP BY status_code
	 UNION 
	SELECT status_code
		 , COUNT(1) AS counts
	 FROM asset
	WHERE external = 1
	  AND origin_host = 'readwrite_com'
	GROUP BY status_code
	) sub



-- average size 
SELECT SUM(size) AS total_size
	 , SUM(articles) AS articles
	 , SUM(size)/SUM(articles) AS average_size

FROM (
	SELECT SUM(size) AS size
	     , COUNT(1) AS articles
	  FROM page
	 WHERE external = 0
	   AND origin_host = 'readwrite_com'
	 UNION 
	SELECT SUM(size) AS size
		 , COUNT(1) AS articles
	 FROM asset 
	WHERE external = 1
	  AND origin_host = 'readwrite_com'
	) sub


-- assets per articles

-- article vs. asset counts






-- counting the line columns and lint percentage
SELECT SUM(lint_critical) AS lint_critical
	, SUM(lint_warn) AS lint_warn
	, SUM(lint_error) AS lint_error
	, SUM(lint_info) AS lint_info
	, COUNT(1) AS articles
 FROM page 
WHERE external = 0
AND origin_host = 'readwrite_com'





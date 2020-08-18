-- BigQuery query for HN URLs
select id, timestamp, time, score, url from `bigquery-public-data.hacker_news.full` 
where url != 'null'
and dead is not true
and deleted is not true
limit 10000
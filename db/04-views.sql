CREATE OR REPLACE VIEW reviewer.movie_with_genres
AS
SELECT
m.movie_id
,m.movie_name
,m.release_date
,EXTRACT(year FROM m.release_date) AS release_year
,g.genre_id
,g.genre_name
FROM reviewer.movie m
JOIN reviewer.movie_genre_bridge mg ON m.movie_id = mg.movie_id
JOIN reviewer.genre g ON mg.genre_id = g.genre_id;

CREATE OR REPLACE VIEW reviewer.movie_with_workers
AS
SELECT
m.movie_id
,m.movie_name
,m.release_date
,EXTRACT(year FROM m.release_date) AS release_year
,STRING_AGG(CAST(mw.movie_worker_position AS TEXT), ' / ' ORDER BY CAST(mw.movie_worker_position AS TEXT)) AS positions
,w.worker_id
,w.worker_name
FROM reviewer.movie m
JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
JOIN reviewer.worker w ON mw.worker_id = w.worker_id
GROUP BY m.movie_id, w.worker_id;

CREATE OR REPLACE VIEW reviewer.review_with_person_and_movie
AS
SELECT
r.review_id
,r.review_score
,r.review_timestamp
,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
,p.person_id
,p.person_name AS reviewer
,m.movie_id
,m.movie_name
FROM reviewer.review r
JOIN reviewer.person p ON r.person_id = p.person_id
JOIN reviewer.movie m ON r.movie_id = m.movie_id;

CREATE OR REPLACE VIEW reviewer.reply_with_review
AS
SELECT
rp.reply_id
,rp.reply_timestamp
,TO_CHAR(rp.reply_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS reply_date
,rp.person_id
,rv.review_id
,rv.review_score
,TO_CHAR(rv.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
,p.person_name AS reviewer
,m.movie_id
,m.movie_name
FROM reviewer.reply rp
JOIN reviewer.review rv ON rp.review_id = rv.review_id
JOIN reviewer.person p ON rv.person_id = p.person_id
JOIN reviewer.movie m ON rv.movie_id = m.movie_id;

CREATE OR REPLACE VIEW reviewer.statistic_with_object
AS
SELECT
s.statistic_id
,s.statistic_name
,s.statistic_type
,s.person_id
,w.worker_id
,w.worker_name
,r.review_id
,r.review_score
,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
,m.movie_id
,m.movie_name
FROM reviewer.statistic s
LEFT OUTER JOIN reviewer.worker w ON s.worker_id = w.worker_id
LEFT OUTER JOIN reviewer.review r ON s.review_id = r.review_id
LEFT OUTER JOIN reviewer.movie m ON r.movie_id = m.movie_id;
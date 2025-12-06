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
LEFT OUTER JOIN reviewer.movie_genre_bridge mg ON m.movie_id = mg.movie_id
LEFT OUTER JOIN reviewer.genre g ON mg.genre_id = g.genre_id;

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
LEFT OUTER JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
LEFT OUTER JOIN reviewer.worker w ON mw.worker_id = w.worker_id
GROUP BY m.movie_id, w.worker_id;
CREATE USER reviewer_user WITH PASSWORD TODO;

GRANT USAGE ON SCHEMA reviewer TO reviewer_user;

GRANT SELECT ON reviewer.worker TO reviewer_user;
GRANT SELECT ON reviewer.genre TO reviewer_user;
GRANT SELECT ON reviewer.movie TO reviewer_user;
GRANT SELECT ON reviewer.movie_worker_bridge TO reviewer_user;
GRANT SELECT ON reviewer.movie_genre_bridge TO reviewer_user;
GRANT SELECT ON reviewer.person TO reviewer_user;
GRANT SELECT ON reviewer.review TO reviewer_user;
GRANT SELECT ON reviewer.review_reaction TO reviewer_user;
GRANT SELECT ON reviewer.reply TO reviewer_user;
GRANT SELECT ON reviewer.reply_reaction TO reviewer_user;
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
GRANT SELECT ON reviewer.statistic TO reviewer_user;

GRANT INSERT ON reviewer.review TO reviewer_user;
GRANT INSERT ON reviewer.reply TO reviewer_user;
GRANT INSERT ON reviewer.review_reaction TO reviewer_user;
GRANT INSERT ON reviewer.reply_reaction TO reviewer_user;
GRANT INSERT ON reviewer.statistic TO reviewer_user;

GRANT UPDATE ON reviewer.person TO reviewer_user;
GRANT UPDATE ON reviewer.review TO reviewer_user;
GRANT UPDATE ON reviewer.reply TO reviewer_user;

GRANT DELETE ON reviewer.person TO reviewer_user;
GRANT DELETE ON reviewer.review TO reviewer_user;
GRANT DELETE ON reviewer.reply TO reviewer_user;
GRANT DELETE ON reviewer.review_reaction TO reviewer_user;
GRANT DELETE ON reviewer.reply_reaction TO reviewer_user;
GRANT DELETE ON reviewer.statistic TO reviewer_user;
INSERT INTO reviewer.worker (name)
VALUES ('Ryan Coogler');

INSERT INTO reviewer.worker (name)
VALUES ('Michael B. Jordan');

INSERT INTO reviewer.worker (name)
VALUES ('Hailee Steinfeld');

INSERT INTO reviewer.genre (name)
VALUES ('Thriller');

INSERT INTO reviewer.genre (name)
VALUES ('Action');

INSERT INTO reviewer.genre (name)
VALUES ('Horror');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Sinners', DATE '2025-04-18');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (1, 1, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (1, 1, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (1, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (1, 3, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 1);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 3);

INSERT INTO reviewer.worker (name)
VALUES ('Ray Mendoza');

INSERT INTO reviewer.worker (name)
VALUES ('Alex Garland');

INSERT INTO reviewer.worker (name)
VALUES ('D''Pharaoh Woon-A-Tai');

INSERT INTO reviewer.worker (name)
VALUES ('Will Poulter');

INSERT INTO reviewer.worker (name)
VALUES ('Cosmo Jarvis');

INSERT INTO reviewer.genre (name)
VALUES ('War');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Warfare', DATE '2025-04-11');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 4, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 4, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 5, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 5, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 6, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 7, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (2, 8, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 4);

INSERT INTO reviewer.worker (name)
VALUES ('Aaron Covington');

INSERT INTO reviewer.worker (name)
VALUES ('Sylvester Stallone');

INSERT INTO reviewer.worker (name)
VALUES ('Tessa Thompson');

INSERT INTO reviewer.genre (name)
VALUES ('Drama');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Creed', DATE '2015-11-25');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 1, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 1, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 9, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 10, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (3, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 5);

INSERT INTO reviewer.worker (name)
VALUES ('Steven Caple Jr.');

INSERT INTO reviewer.worker (name)
VALUES ('Juel Taylor');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Creed II', DATE '2018-11-21');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 12, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 10, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 13, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 10, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, position)
VALUES (4, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 5);

-- TODO - test below SQL statements

INSERT INTO reviewer.user (username, email_address, hashed_password)
VALUES ('White Cat', 'whitecat@gmail.com', 'placeholder');

INSERT INTO reviewer.user (username, email_address, hashed_password)
VALUES ('Potato Eel', 'potatoeel@hotmail.com', 'placeholder');

INSERT INTO reviewer.user (username, email_address, hashed_password)
VALUES ('Reviewer In the Woods', 'reviewinthewoods@yahoo.com', 'placeholder');

INSERT INTO reviewer.user (username, email_address, hashed_password)
VALUES ('My Pet Seel Reviews', 'mypetseelreviews@gmail.com', 'placeholder');

INSERT INTO reviewer.review (score, content, user_id, movie_id)
VALUES (8, 'Pretty good!', 1, 4);

INSERT INTO reviewer.review (score, content, user_id, movie_id)
VALUES (3, 'Absolutely awful...', 2, 1);

INSERT INTO reviewer.review (score, content, user_id, movie_id)
VALUES (7, 'Solid. I had a fun time', 2, 2);

INSERT INTO reviewer.review (score, content, user_id, movie_id)
VALUES (10, 'Amazing! Best move of the year', 4, 1);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('dislike', 4, 2);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('dislike', 3, 2);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('like', 2, 2);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('dislike', 1, 2);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('like', 1, 4);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('like', 3, 4);

INSERT INTO reviewer.review_reaction (type, user_id, review_id)
VALUES ('dislike', 2, 3);

INSERT INTO reviewer.comment (content, user_id, review_id)
VALUES ('Wow, you have a bad taste in movies', 3, 2);

INSERT INTO reviewer.comment (content, user_id, review_id)
VALUES ('Who are you?', 4, 2);

INSERT INTO reviewer.comment (content, user_id, review_id)
VALUES ('Potato Eel is cancer', 1, 2);

INSERT INTO reviewer.comment (content, user_id, review_id)
VALUES ('Yeah, I thought this was the best as well!', 3, 4);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('dislike', 2, 1);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('dislike', 2, 2);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('dislike', 2, 3);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('like', 1, 1);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('like', 1, 2);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('like', 4, 1);

INSERT INTO reviewer.comment_reaction (type, user_id, comment_id)
VALUES ('like', 3, 2);
-- Sinners

INSERT INTO reviewer.worker (worker_name)
VALUES ('Ryan Coogler');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Michael B. Jordan');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Hailee Steinfeld');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Thriller');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Action');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Horror');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Sinners', DATE '2025-04-18');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (1, 1, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (1, 1, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (1, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (1, 3, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 1);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 3);

-- Warfare

INSERT INTO reviewer.worker (worker_name)
VALUES ('Ray Mendoza');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Alex Garland');

INSERT INTO reviewer.worker (worker_name)
VALUES ('D''Pharaoh Woon-A-Tai');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Will Poulter');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Cosmo Jarvis');

INSERT INTO reviewer.genre (genre_name)
VALUES ('War');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Warfare', DATE '2025-04-11');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 4, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 4, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 5, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 5, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 6, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 7, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (2, 8, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 4);

-- Creed

INSERT INTO reviewer.worker (worker_name)
VALUES ('Aaron Covington');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Sylvester Stallone');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Tessa Thompson');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Drama');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Creed', DATE '2015-11-25');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 1, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 1, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 9, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 10, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (3, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 5);

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('White Cat', 'whitecat@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$1N2rjz9e1/OVaPENfJFTXA$og654YPv3+njL27g0aLggny+NPQeosI/klklyq5PUfY');

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('Reviewer in the Woods', 'reviewinthewoods@yahoo.com', '$argon2id$v=19$m=65536,t=3,p=4$kc1VeMcRlCQZ8TnYcrJy1Q$oyXR4fvudLUkFtl5ipFumvItv/Q+ZE1w11IL4Gh+mZA');

INSERT INTO reviewer.review (review_score, review_content, review_timestamp, person_id, movie_id)
VALUES (3, 'Absolutely awful...', CURRENT_TIMESTAMP - INTERVAL '2 days', 2, 2);
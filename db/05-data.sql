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

-- Creed II

INSERT INTO reviewer.worker (worker_name)
VALUES ('Steven Caple Jr.');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Juel Taylor');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Creed II', DATE '2018-11-21');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 12, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 10, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 13, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 10, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (4, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 5);

-- Civil War

INSERT INTO reviewer.worker (worker_name)
VALUES ('Kirsten Dunst');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Wagner Moura');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Cailee Spaeny');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Civil War', DATE '2024-04-12');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (5, 5, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (5, 5, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (5, 14, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (5, 15, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (5, 16, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (5, 4);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (5, 5);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (5, 2);

-- Ex Machina

INSERT INTO reviewer.worker (worker_name)
VALUES ('Domhnall Gleeson');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Alicia Vikander');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Oscar Isaac');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Science Fiction');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Ex Machina', DATE '2015-04-10');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (6, 5, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (6, 5, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (6, 17, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (6, 18, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (6, 19, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (6, 6);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (6, 5);

-- Spider-Man

INSERT INTO reviewer.worker (worker_name)
VALUES ('Tobey Maguire');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Willem Dafoe');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Sam Raimi');

INSERT INTO reviewer.worker (worker_name)
VALUES ('David Koepp');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Spider-Man', DATE '2002-05-03');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (7, 22, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (7, 23, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (7, 20, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (7, 21, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (7, 14, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (7, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (7, 6);

-- Spider-Man 2

INSERT INTO reviewer.worker (worker_name)
VALUES ('James Franco');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Alvin Sargent');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Adventure');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Spider-Man 2', DATE '2004-06-30');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (8, 22, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (8, 25, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (8, 20, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (8, 14, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (8, 24, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (8, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (8, 6);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (8, 7);

-- Spider-Man 3

INSERT INTO reviewer.worker (worker_name)
VALUES ('Ivan Raimi');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Spider-Man 3', DATE '2007-05-03');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 22, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 25, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 22, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 26, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 20, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 14, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (9, 24, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (9, 6);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (9, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (9, 7);

-- Nosferatu

INSERT INTO reviewer.worker (worker_name)
VALUES ('Lily-Rose Depp');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Nicholas Hoult');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Bill Skarsgård');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Robert Eggers');

INSERT INTO reviewer.genre (genre_name)
VALUES ('Fantasy');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Nosferatu', DATE '2024-12-25');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (10, 30, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (10, 30, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (10, 27, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (10, 28, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (10, 29, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (10, 8);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (10, 3);

-- The Northman

INSERT INTO reviewer.worker (worker_name)
VALUES ('Alexander Skarsgård');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Nicole Kidman');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Claes Bang');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Sjón');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('The Northman', DATE '2022-04-22');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 30, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 34, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 30, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 31, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 32, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (11, 33, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (11, 7);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (11, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (11, 8);

-- The Lighthouse

INSERT INTO reviewer.worker (worker_name)
VALUES ('Robert Pattinson');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Valeriia Karaman');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Max Eggers');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('The Lighthouse', DATE '2019-10-18');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 30, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 30, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 37, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 35, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 21, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (12, 36, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (12, 1);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (12, 8);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (12, 3);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (12, 5);

-- Creed III

INSERT INTO reviewer.worker (worker_name)
VALUES ('Jonathan Majors');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Keenan Coogler');

INSERT INTO reviewer.worker (worker_name)
VALUES ('Zach Baylin');

INSERT INTO reviewer.movie (movie_name, release_date)
VALUES ('Creed III', DATE '2023-03-03');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 2, 'Director');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 39, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 40, 'Writer');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 2, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 11, 'Actor');

INSERT INTO reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position)
VALUES (13, 38, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (13, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (13, 5);

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('White Cat', 'whitecat@gmail.com', 'placeholder');

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('Potato Eel', 'potatoeel@hotmail.com', 'placeholder');

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('Reviewer In the Woods', 'reviewinthewoods@yahoo.com', 'placeholder');

INSERT INTO reviewer.person (person_name, email_address, hashed_password)
VALUES ('My Pet Seel Reviews', 'mypetseelreviews@gmail.com', 'placeholder');

INSERT INTO reviewer.review (review_score, review_content, review_date, person_id, movie_id)
VALUES (8, 'Pretty good!', CURRENT_TIMESTAMP - INTERVAL '3 days', 1, 4);

INSERT INTO reviewer.review (review_score, review_content, review_date, person_id, movie_id)
VALUES (3, 'Absolutely awful...', CURRENT_TIMESTAMP - INTERVAL '2 days', 2, 1);

INSERT INTO reviewer.review (review_score, review_content, review_date, person_id, movie_id)
VALUES (7, 'Solid. I had a fun time', CURRENT_TIMESTAMP - INTERVAL '1 day 23 hours', 2, 2);

INSERT INTO reviewer.review (review_score, review_content, review_date, person_id, movie_id)
VALUES (10, 'Amazing! Best move of the year', CURRENT_TIMESTAMP - INTERVAL '1 day 12 hours', 4, 1);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('dislike', 4, 2);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('dislike', 3, 2);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('like', 2, 2);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('dislike', 1, 2);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('like', 1, 4);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('like', 3, 4);

INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
VALUES ('dislike', 3, 3);

INSERT INTO reviewer.reply (reply_content, reply_date, person_id, review_id)
VALUES ('Wow, you have a bad taste in movies', CURRENT_TIMESTAMP - INTERVAL '23 hours', 3, 2);

INSERT INTO reviewer.reply (reply_content, reply_date, person_id, review_id)
VALUES ('Who are you?', CURRENT_TIMESTAMP - INTERVAL '22 hours', 4, 2);

INSERT INTO reviewer.reply (reply_content, reply_date, person_id, review_id)
VALUES ('Potato Eel is cancer', CURRENT_TIMESTAMP - INTERVAL '21 hours', 1, 2);

INSERT INTO reviewer.reply (reply_content, reply_date, person_id, review_id)
VALUES ('Yeah, I thought this was the best as well!', CURRENT_TIMESTAMP - INTERVAL '20 hours', 3, 4);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('dislike', 2, 1);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('dislike', 2, 2);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('dislike', 2, 3);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('like', 1, 1);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('like', 1, 2);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('like', 4, 1);

INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
VALUES ('like', 3, 2);
INSERT INTO reviewer.crew (name)
VALUES ('Ryan Coogler');

INSERT INTO reviewer.crew (name)
VALUES ('Michael B. Jordan');

INSERT INTO reviewer.crew (name)
VALUES ('Hailee Steinfeld');

INSERT INTO reviewer.genre (name)
VALUES ('Thriller');

INSERT INTO reviewer.genre (name)
VALUES ('Action');

INSERT INTO reviewer.genre (name)
VALUES ('Horror');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Sinners', DATE '2025-04-18');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (1, 1, 'Director');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (1, 1, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (1, 2, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (1, 3, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 1);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (1, 3);

INSERT INTO reviewer.crew (name)
VALUES ('Ray Mendoza');

INSERT INTO reviewer.crew (name)
VALUES ('Alex Garland');

INSERT INTO reviewer.crew (name)
VALUES ('D''Pharaoh Woon-A-Tai');

INSERT INTO reviewer.crew (name)
VALUES ('Will Poulter');

INSERT INTO reviewer.crew (name)
VALUES ('Cosmo Jarvis');

INSERT INTO reviewer.genre (name)
VALUES ('War');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Warfare', DATE '2025-04-11');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 4, 'Director');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 4, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 5, 'Director');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 5, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 6, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 7, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (2, 8, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (2, 4);

INSERT INTO reviewer.crew (name)
VALUES ('Aaron Covington');

INSERT INTO reviewer.crew (name)
VALUES ('Sylvester Stallone');

INSERT INTO reviewer.crew (name)
VALUES ('Tessa Thompson');

INSERT INTO reviewer.genre (name)
VALUES ('Drama');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Creed', DATE '2015-11-25');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 1, 'Director');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 1, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 9, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 2, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 10, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (3, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (3, 5);

INSERT INTO reviewer.crew (name)
VALUES ('Steven Caple Jr.');

INSERT INTO reviewer.crew (name)
VALUES ('Juel Taylor');

INSERT INTO reviewer.movie (name, release_date)
VALUES ('Creed II', DATE '2018-11-21');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 12, 'Director');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 10, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 13, 'Writer');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 2, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 10, 'Actor');

INSERT INTO reviewer.movie_crew_bridge (movie_id, crew_id, position)
VALUES (4, 11, 'Actor');

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 2);

INSERT INTO reviewer.movie_genre_bridge (movie_id, genre_id)
VALUES (4, 5);
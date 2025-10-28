CREATE TABLE reviewer.crew (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT
);

CREATE TABLE reviewer.genre (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE reviewer.movie (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    release_date DATE
);

CREATE TABLE reviewer.movie_crew_bridge (
    movie_id INTEGER,
    crew_id INTEGER,
    position TEXT
);

CREATE TABLE reviewer.movie_genre_bridge (
    movie_id INTEGER,
    genre_id INTEGER
);
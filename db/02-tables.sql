CREATE TABLE reviewer.crew (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE reviewer.genre (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE reviewer.movie (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    release_date DATE NOT NULL
);

CREATE TABLE reviewer.movie_crew_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(id),
    crew_id INTEGER NOT NULL REFERENCES crew(id),
    position TEXT NOT NULL

);

CREATE TABLE reviewer.movie_genre_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(id),
    genre_id INTEGER NOT NULL REFERENCES genre(id)
);
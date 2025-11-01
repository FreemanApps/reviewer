CREATE TABLE reviewer.worker (
    worker_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE reviewer.genre (
    genre_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE reviewer.movie (
    movie_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    release_date DATE NOT NULL
);

CREATE TABLE reviewer.movie_worker_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    worker_id INTEGER NOT NULL REFERENCES worker(worker_id) ON DELETE CASCADE,
    position TEXT NOT NULL
);

CREATE TABLE reviewer.movie_genre_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genre(genre_id) ON DELETE CASCADE
);
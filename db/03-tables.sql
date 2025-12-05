CREATE TABLE reviewer.worker (
    worker_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    worker_name TEXT NOT NULL
);

CREATE TABLE reviewer.genre (
    genre_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    genre_name TEXT UNIQUE NOT NULL
);

CREATE TABLE reviewer.movie (
    movie_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movie_name TEXT NOT NULL,
    release_date DATE NOT NULL
);

CREATE TABLE reviewer.movie_worker_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    worker_id INTEGER NOT NULL REFERENCES worker(worker_id) ON DELETE CASCADE,
    movie_worker_position TEXT NOT NULL
);

CREATE TABLE reviewer.movie_genre_bridge (
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.person (
    person_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_name TEXT UNIQUE NOT NULL,
    email_address TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE reviewer.review (
    review_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    review_score INTEGER CHECK (review_score >= 0 AND review_score <= 10),
    review_content TEXT,
    review_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    person_id INTEGER NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE
    CHECK (review_score IS NOT NULL OR review_content IS NOT NULL)
);

CREATE TABLE reviewer.review_reaction (
    review_reaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    review_reaction_type reaction_type NOT NULL,
    person_id INTEGER NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,    
    review_id INTEGER NOT NULL REFERENCES review(review_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.reply (
    reply_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reply_content TEXT NOT NULL,
    reply_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    person_id INTEGER NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    review_id INTEGER NOT NULL REFERENCES review(review_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.reply_reaction (
    reply_reaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reply_reaction_type reaction_type NOT NULL,
    person_id INTEGER NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    reply_id INTEGER NOT NULL REFERENCES reply(reply_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.statistic (
    statistic_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    statistic_name statistic_name NOT NULL,
    statistic_type statistic_type NOT NULL,
    person_id INTEGER NOT NULL REFERENCES person(person_id) ON DELETE CASCADE,
    worker_id INTEGER REFERENCES worker(worker_id) ON DELETE CASCADE,
    review_id INTEGER REFERENCES review(review_id) ON DELETE CASCADE
);
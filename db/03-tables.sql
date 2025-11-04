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

-- TODO - test below SQL statements

CREATE TABLE reviewer.user (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email_address TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
);

CREATE TABLE reviewer.review (
    review_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    score INTEGER CHECK (score >= 0 AND score <= 10),
    content TEXT,
    user_id INTEGER NOT NULL REFERENCES user(user_id) ON DELETE CASCADE,
    movie_id INTEGER NOT NULL REFERENCES movie(movie_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.review_reaction (
    review_reaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type reaction_type NOT NULL,
    user_id INTEGER NOT NULL REFERENCES user(user_id) ON DELETE CASCADE,    
    review_id INTEGER NOT NULL REFERENCES review(review_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.comment (
    comment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES user(user_id) ON DELETE CASCADE,
    review_id INTEGER NOT NULL REFERENCES review(review_id) ON DELETE CASCADE
);

CREATE TABLE reviewer.comment_reaction (
    comment_reaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type reaction_type NOT NULL,
    user_id INTEGER NOT NULL REFERENCES user(user_id) ON DELETE CASCADE,
    comment_id INTEGER NOT NULL REFERENCES comment(comment_id) ON DELETE CASCADE
);
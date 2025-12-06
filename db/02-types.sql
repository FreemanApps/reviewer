CREATE TYPE reviewer.movie_worker_position AS ENUM ('actor', 'writer', 'director');

CREATE TYPE reviewer.reaction_type AS ENUM ('like', 'dislike');

CREATE TYPE reviewer.statistic_name AS ENUM ('most_reviewed_director', 'highest_rated_director', 'most_controversial_review');

CREATE TYPE reviewer.statistic_type AS ENUM ('worker','review');
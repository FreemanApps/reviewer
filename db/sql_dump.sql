--
-- PostgreSQL database dump
--

\restrict 9XGyodjbUIjc9ZHg5kwwX3Z5DHTTwW1g6RuSmV3j7JEufqRRlfcXRl7AAFSIGKF

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP ROLE IF EXISTS reviewer_user;
CREATE ROLE reviewer_user WITH LOGIN PASSWORD 'AmzhSWV>qXy6vxD+g<6>{,s)R~Dgg~';

--
-- Name: reviewer; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA reviewer;


--
-- Name: movie_worker_position; Type: TYPE; Schema: reviewer; Owner: -
--

CREATE TYPE reviewer.movie_worker_position AS ENUM (
    'actor',
    'writer',
    'director'
);


--
-- Name: reaction_type; Type: TYPE; Schema: reviewer; Owner: -
--

CREATE TYPE reviewer.reaction_type AS ENUM (
    'like',
    'dislike'
);


--
-- Name: statistic_name; Type: TYPE; Schema: reviewer; Owner: -
--

CREATE TYPE reviewer.statistic_name AS ENUM (
    'most_reviewed_director',
    'highest_rated_director',
    'most_controversial_review'
);


--
-- Name: statistic_type; Type: TYPE; Schema: reviewer; Owner: -
--

CREATE TYPE reviewer.statistic_type AS ENUM (
    'worker',
    'review'
);


--
-- Name: generate_person_statistics(integer); Type: PROCEDURE; Schema: reviewer; Owner: -
--

CREATE PROCEDURE reviewer.generate_person_statistics(IN p_person_id integer)
    LANGUAGE sql
    AS $$

    DELETE FROM reviewer.statistic

    WHERE person_id = p_person_id;



    -- most viewed director

    INSERT INTO reviewer.statistic (statistic_name, statistic_type, person_id, worker_id)

    SELECT 'most_reviewed_director', 'worker', p_person_id, worker_id FROM (

        SELECT mw.worker_id, COUNT(*) AS num_reviewed

        FROM reviewer.review r

        LEFT OUTER JOIN reviewer.movie m ON r.movie_id = m.movie_id

        LEFT OUTER JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id

        WHERE r.person_id = p_person_id

        AND mw.movie_worker_position = 'director'

        GROUP BY mw.worker_id

        ORDER BY num_reviewed DESC, mw.worker_id

        LIMIT 1

    );



    -- highest rated director

    INSERT INTO reviewer.statistic (statistic_name, statistic_type, person_id, worker_id)

    SELECT 'highest_rated_director', 'worker', p_person_id, worker_id FROM (

        SELECT mw.worker_id, AVG(r.review_score) AS average_rating

        FROM reviewer.review r

        LEFT OUTER JOIN reviewer.movie m ON r.movie_id = m.movie_id

        LEFT OUTER JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id

        WHERE r.person_id = p_person_id

        AND mw.movie_worker_position = 'director'

        GROUP BY mw.worker_id

        ORDER BY average_rating DESC, mw.worker_id

        LIMIT 1

    );



    -- most controversial review

    INSERT INTO reviewer.statistic (statistic_name, statistic_type, person_id, review_id)

    SELECT 'most_controversial_review', 'review', p_person_id, review_id FROM (

        SELECT review_id, total / GREATEST(ABS(likes - dislikes), 1) AS controversial FROM (

            SELECT

            r.review_id

            ,COUNT(*) total

            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes

            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes

            FROM reviewer.review r

            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id

            WHERE r.person_id = p_person_id

            GROUP BY r.review_id

        )

        ORDER BY controversial DESC, review_id

        LIMIT 1

    );

$$;


--
-- Name: reply_with_reaction_type(reviewer.reaction_type, integer); Type: FUNCTION; Schema: reviewer; Owner: -
--

CREATE FUNCTION reviewer.reply_with_reaction_type(p_reply_reaction_type reviewer.reaction_type, p_current_person_id integer) RETURNS TABLE(reply_id integer, has_reacted integer, reaction_count integer)
    LANGUAGE sql
    AS $$

    SELECT

    r.reply_id

    ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = p_reply_reaction_type AND rr.person_id = p_current_person_id) has_reacted

    ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = p_reply_reaction_type) reaction_count

    FROM reviewer.reply r

    LEFT OUTER JOIN reviewer.reply_reaction rr ON r.reply_id = rr.reply_id

    GROUP BY r.reply_id

$$;


--
-- Name: reply_with_reactions(integer); Type: FUNCTION; Schema: reviewer; Owner: -
--

CREATE FUNCTION reviewer.reply_with_reactions(p_current_person_id integer) RETURNS TABLE(reply_id integer, reply_content text, reply_timestamp timestamp with time zone, reply_date text, person_id integer, person_name text, review_id integer, has_liked integer, likes integer, has_disliked integer, dislikes integer)
    LANGUAGE sql
    AS $$

    SELECT

    r.reply_id

    ,r.reply_content

    ,r.reply_timestamp

    ,TO_CHAR(r.reply_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS reply_date

    ,p.person_id

    ,p.person_name

    ,r.review_id

    ,l.has_reacted AS has_liked

    ,l.reaction_count AS likes

    ,d.has_reacted AS has_disliked

    ,d.reaction_count AS dislikes

    FROM reviewer.reply r

    JOIN reviewer.person p ON r.person_id = p.person_id

    LEFT OUTER JOIN reviewer.reply_with_reaction_type('like', p_current_person_id) l ON r.reply_id = l.reply_id

    LEFT OUTER JOIN reviewer.reply_with_reaction_type('dislike', p_current_person_id) d ON r.reply_id = d.reply_id

    GROUP BY r.reply_id, p.person_id, l.has_reacted, l.reaction_count, d.has_reacted, d.reaction_count

$$;


--
-- Name: review_with_reaction_type(reviewer.reaction_type, integer); Type: FUNCTION; Schema: reviewer; Owner: -
--

CREATE FUNCTION reviewer.review_with_reaction_type(p_review_reaction_type reviewer.reaction_type, p_current_person_id integer) RETURNS TABLE(review_id integer, has_reacted integer, reaction_count integer)
    LANGUAGE sql
    AS $$

    SELECT

    r.review_id

    ,COUNT(*) FILTER (WHERE rr.review_reaction_type = p_review_reaction_type AND rr.person_id = p_current_person_id) has_reacted

    ,COUNT(*) FILTER (WHERE rr.review_reaction_type = p_review_reaction_type) reaction_count

    FROM reviewer.review r

    LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id

    GROUP BY r.review_id

$$;


--
-- Name: review_with_reactions(integer); Type: FUNCTION; Schema: reviewer; Owner: -
--

CREATE FUNCTION reviewer.review_with_reactions(p_current_person_id integer) RETURNS TABLE(review_id integer, review_score integer, review_content text, review_date text, person_id integer, person_name text, has_liked integer, likes integer, has_disliked integer, dislikes integer)
    LANGUAGE sql
    AS $$

    SELECT

    r.review_id

    ,r.review_score

    ,r.review_content

    ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date

    ,p.person_id

    ,p.person_name

    ,l.has_reacted AS has_liked

    ,l.reaction_count AS likes

    ,d.has_reacted AS has_disliked

    ,d.reaction_count AS dislikes

    FROM reviewer.review r

    JOIN reviewer.person p ON r.person_id = p.person_id

    LEFT OUTER JOIN reviewer.review_with_reaction_type('like', p_current_person_id) l ON r.review_id = l.review_id

    LEFT OUTER JOIN reviewer.review_with_reaction_type('dislike', p_current_person_id) d ON r.review_id = d.review_id

    GROUP BY r.review_id, p.person_id, l.has_reacted, l.reaction_count, d.has_reacted, d.reaction_count

$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: genre; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.genre (
    genre_id integer NOT NULL,
    genre_name text NOT NULL
);


--
-- Name: genre_genre_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.genre ALTER COLUMN genre_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.genre_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: movie; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.movie (
    movie_id integer NOT NULL,
    movie_name text NOT NULL,
    release_date date NOT NULL
);


--
-- Name: movie_genre_bridge; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.movie_genre_bridge (
    movie_id integer NOT NULL,
    genre_id integer NOT NULL
);


--
-- Name: movie_movie_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.movie ALTER COLUMN movie_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.movie_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: movie_with_genres; Type: VIEW; Schema: reviewer; Owner: -
--

CREATE VIEW reviewer.movie_with_genres AS
 SELECT m.movie_id,
    m.movie_name,
    m.release_date,
    EXTRACT(year FROM m.release_date) AS release_year,
    g.genre_id,
    g.genre_name
   FROM ((reviewer.movie m
     JOIN reviewer.movie_genre_bridge mg ON ((m.movie_id = mg.movie_id)))
     JOIN reviewer.genre g ON ((mg.genre_id = g.genre_id)));


--
-- Name: movie_with_workers; Type: VIEW; Schema: reviewer; Owner: -
--

CREATE VIEW reviewer.movie_with_workers AS
SELECT
    NULL::integer AS movie_id,
    NULL::text AS movie_name,
    NULL::date AS release_date,
    NULL::numeric AS release_year,
    NULL::text AS positions,
    NULL::integer AS worker_id,
    NULL::text AS worker_name;


--
-- Name: movie_worker_bridge; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.movie_worker_bridge (
    movie_id integer NOT NULL,
    worker_id integer NOT NULL,
    movie_worker_position reviewer.movie_worker_position NOT NULL
);


--
-- Name: person; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.person (
    person_id integer NOT NULL,
    person_name text NOT NULL,
    email_address text NOT NULL,
    hashed_password text NOT NULL
);


--
-- Name: person_person_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.person ALTER COLUMN person_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.person_person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reply; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.reply (
    reply_id integer NOT NULL,
    reply_content text NOT NULL,
    reply_timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    person_id integer NOT NULL,
    review_id integer NOT NULL
);


--
-- Name: reply_reaction; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.reply_reaction (
    reply_reaction_id integer NOT NULL,
    reply_reaction_type reviewer.reaction_type NOT NULL,
    person_id integer NOT NULL,
    reply_id integer NOT NULL
);


--
-- Name: reply_reaction_reply_reaction_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.reply_reaction ALTER COLUMN reply_reaction_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.reply_reaction_reply_reaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reply_reply_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.reply ALTER COLUMN reply_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.reply_reply_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: review; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.review (
    review_id integer NOT NULL,
    review_score integer,
    review_content text,
    review_timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    person_id integer NOT NULL,
    movie_id integer NOT NULL,
    CONSTRAINT review_check CHECK (((review_score IS NOT NULL) OR (review_content IS NOT NULL))),
    CONSTRAINT review_review_score_check CHECK (((review_score >= 1) AND (review_score <= 10)))
);


--
-- Name: reply_with_review; Type: VIEW; Schema: reviewer; Owner: -
--

CREATE VIEW reviewer.reply_with_review AS
 SELECT rp.reply_id,
    rp.reply_timestamp,
    to_char((rp.reply_timestamp AT TIME ZONE 'America/New_York'::text), 'DD Mon YYYY'::text) AS reply_date,
    rp.person_id,
    rv.review_id,
    rv.review_score,
    to_char((rv.review_timestamp AT TIME ZONE 'America/New_York'::text), 'DD Mon YYYY'::text) AS review_date,
    p.person_name AS reviewer,
    m.movie_id,
    m.movie_name
   FROM (((reviewer.reply rp
     JOIN reviewer.review rv ON ((rp.review_id = rv.review_id)))
     JOIN reviewer.person p ON ((rv.person_id = p.person_id)))
     JOIN reviewer.movie m ON ((rv.movie_id = m.movie_id)));


--
-- Name: review_reaction; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.review_reaction (
    review_reaction_id integer NOT NULL,
    review_reaction_type reviewer.reaction_type NOT NULL,
    person_id integer NOT NULL,
    review_id integer NOT NULL
);


--
-- Name: review_reaction_review_reaction_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.review_reaction ALTER COLUMN review_reaction_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.review_reaction_review_reaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: review_review_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.review ALTER COLUMN review_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.review_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: review_with_person_and_movie; Type: VIEW; Schema: reviewer; Owner: -
--

CREATE VIEW reviewer.review_with_person_and_movie AS
 SELECT r.review_id,
    r.review_score,
    r.review_timestamp,
    to_char((r.review_timestamp AT TIME ZONE 'America/New_York'::text), 'DD Mon YYYY'::text) AS review_date,
    p.person_id,
    p.person_name AS reviewer,
    m.movie_id,
    m.movie_name
   FROM ((reviewer.review r
     JOIN reviewer.person p ON ((r.person_id = p.person_id)))
     JOIN reviewer.movie m ON ((r.movie_id = m.movie_id)));


--
-- Name: statistic; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.statistic (
    statistic_id integer NOT NULL,
    statistic_name reviewer.statistic_name NOT NULL,
    statistic_type reviewer.statistic_type NOT NULL,
    person_id integer NOT NULL,
    worker_id integer,
    review_id integer,
    CONSTRAINT statistic_check CHECK (((worker_id IS NOT NULL) OR (review_id IS NOT NULL)))
);


--
-- Name: statistic_statistic_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.statistic ALTER COLUMN statistic_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.statistic_statistic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: worker; Type: TABLE; Schema: reviewer; Owner: -
--

CREATE TABLE reviewer.worker (
    worker_id integer NOT NULL,
    worker_name text NOT NULL
);


--
-- Name: statistic_with_object; Type: VIEW; Schema: reviewer; Owner: -
--

CREATE VIEW reviewer.statistic_with_object AS
 SELECT s.statistic_id,
    s.statistic_name,
    s.statistic_type,
    s.person_id,
    w.worker_id,
    w.worker_name,
    r.review_id,
    r.review_score,
    to_char((r.review_timestamp AT TIME ZONE 'America/New_York'::text), 'DD Mon YYYY'::text) AS review_date,
    m.movie_id,
    m.movie_name
   FROM (((reviewer.statistic s
     LEFT JOIN reviewer.worker w ON ((s.worker_id = w.worker_id)))
     LEFT JOIN reviewer.review r ON ((s.review_id = r.review_id)))
     LEFT JOIN reviewer.movie m ON ((r.movie_id = m.movie_id)));


--
-- Name: worker_worker_id_seq; Type: SEQUENCE; Schema: reviewer; Owner: -
--

ALTER TABLE reviewer.worker ALTER COLUMN worker_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME reviewer.worker_worker_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: genre; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.genre (genre_id, genre_name) FROM stdin;
1	Thriller
2	Action
3	Horror
4	War
5	Drama
6	Science Fiction
7	Adventure
8	Fantasy
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.movie (movie_id, movie_name, release_date) FROM stdin;
1	Sinners	2025-04-18
2	Warfare	2025-04-11
3	Creed	2015-11-25
4	Creed II	2018-11-21
5	Civil War	2024-04-12
6	Ex Machina	2015-04-10
7	Spider-Man	2002-05-03
8	Spider-Man 2	2004-06-30
9	Spider-Man 3	2007-05-03
10	Nosferatu	2024-12-25
11	The Northman	2022-04-22
12	The Lighthouse	2019-10-18
13	Creed III	2023-03-03
\.


--
-- Data for Name: movie_genre_bridge; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.movie_genre_bridge (movie_id, genre_id) FROM stdin;
1	1
1	2
1	3
2	2
2	4
3	2
3	5
4	2
4	5
5	4
5	5
5	2
6	6
6	5
7	2
7	6
8	2
8	6
8	7
9	6
9	2
9	7
10	8
10	3
11	7
11	2
11	8
12	1
12	8
12	3
12	5
13	2
13	5
\.


--
-- Data for Name: movie_worker_bridge; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.movie_worker_bridge (movie_id, worker_id, movie_worker_position) FROM stdin;
1	1	director
1	1	writer
1	2	actor
1	3	actor
2	4	director
2	4	writer
2	5	director
2	5	writer
2	6	actor
2	7	actor
2	8	actor
3	1	director
3	1	writer
3	9	writer
3	2	actor
3	10	actor
3	11	actor
4	12	director
4	10	writer
4	13	writer
4	2	actor
4	10	actor
4	11	actor
5	5	director
5	5	writer
5	14	actor
5	15	actor
5	16	actor
6	5	director
6	5	writer
6	17	actor
6	18	actor
6	19	actor
7	22	director
7	23	writer
7	20	actor
7	21	actor
7	14	actor
8	22	director
8	25	writer
8	20	actor
8	14	actor
8	24	actor
9	22	director
9	25	writer
9	22	writer
9	26	writer
9	20	actor
9	14	actor
9	24	actor
10	30	director
10	30	writer
10	27	actor
10	28	actor
10	29	actor
11	30	director
11	34	writer
11	30	writer
11	31	actor
11	32	actor
11	33	actor
12	30	director
12	30	writer
12	37	writer
12	35	actor
12	21	actor
12	36	actor
13	2	director
13	39	writer
13	40	writer
13	2	actor
13	11	actor
13	38	actor
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.person (person_id, person_name, email_address, hashed_password) FROM stdin;
1	White Cat	whitecat@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$1N2rjz9e1/OVaPENfJFTXA$og654YPv3+njL27g0aLggny+NPQeosI/klklyq5PUfY
2	Black Dog	blackdog@hotmail.com	$argon2id$v=19$m=65536,t=3,p=4$WtVu+tpN5RFfVaylR8rcFw$7lSDBVrdEWzqQrlvIoDRBTi3IBfQTGMtu44vPYUs6KM
3	Reviewer in the Woods	reviewinthewoods@yahoo.com	$argon2id$v=19$m=65536,t=3,p=4$kc1VeMcRlCQZ8TnYcrJy1Q$oyXR4fvudLUkFtl5ipFumvItv/Q+ZE1w11IL4Gh+mZA
4	My Pet Seel Reviews	mypetseelreviews@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$R+ZZ91nBtzeXEPmHEKiV+Q$TAZjG+28XztVzDY6TsfMc0eLEu52oDrCcm/uitXPL7E
\.


--
-- Data for Name: reply; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.reply (reply_id, reply_content, reply_timestamp, person_id, review_id) FROM stdin;
1	Wow, you have a bad taste in movies	2025-12-11 18:02:06.663857-05	3	2
2	Who are you?	2025-12-11 19:02:06.663857-05	4	2
3	Black Dog is an awful person	2025-12-11 20:02:06.663857-05	1	2
4	Yeah, I thought this was the best as well!	2025-12-11 21:02:06.663857-05	3	4
\.


--
-- Data for Name: reply_reaction; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.reply_reaction (reply_reaction_id, reply_reaction_type, person_id, reply_id) FROM stdin;
1	dislike	2	1
2	dislike	2	2
3	dislike	2	3
4	like	1	1
5	like	1	2
6	like	4	1
7	like	3	2
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.review (review_id, review_score, review_content, review_timestamp, person_id, movie_id) FROM stdin;
1	8	Pretty good!	2025-12-09 17:02:06.663857-05	1	4
2	3	Absolutely awful...	2025-12-10 17:02:06.663857-05	2	1
3	7	Solid. I had a fun time	2025-12-10 18:02:06.663857-05	2	2
4	10	Amazing! Best movie of the year	2025-12-11 05:02:06.663857-05	4	1
\.


--
-- Data for Name: review_reaction; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.review_reaction (review_reaction_id, review_reaction_type, person_id, review_id) FROM stdin;
1	dislike	4	2
2	dislike	3	2
3	like	2	2
4	dislike	1	2
5	like	1	4
6	like	3	4
7	dislike	3	3
\.


--
-- Data for Name: statistic; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.statistic (statistic_id, statistic_name, statistic_type, person_id, worker_id, review_id) FROM stdin;
\.


--
-- Data for Name: worker; Type: TABLE DATA; Schema: reviewer; Owner: -
--

COPY reviewer.worker (worker_id, worker_name) FROM stdin;
1	Ryan Coogler
2	Michael B. Jordan
3	Hailee Steinfeld
4	Ray Mendoza
5	Alex Garland
6	D'Pharaoh Woon-A-Tai
7	Will Poulter
8	Cosmo Jarvis
9	Aaron Covington
10	Sylvester Stallone
11	Tessa Thompson
12	Steven Caple Jr.
13	Juel Taylor
14	Kirsten Dunst
15	Wagner Moura
16	Cailee Spaeny
17	Domhnall Gleeson
18	Alicia Vikander
19	Oscar Isaac
20	Tobey Maguire
21	Willem Dafoe
22	Sam Raimi
23	David Koepp
24	James Franco
25	Alvin Sargent
26	Ivan Raimi
27	Lily-Rose Depp
28	Nicholas Hoult
29	Bill Skarsgård
30	Robert Eggers
31	Alexander Skarsgård
32	Nicole Kidman
33	Claes Bang
34	Sjón
35	Robert Pattinson
36	Valeriia Karaman
37	Max Eggers
38	Jonathan Majors
39	Keenan Coogler
40	Zach Baylin
\.


--
-- Name: genre_genre_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.genre_genre_id_seq', 8, true);


--
-- Name: movie_movie_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.movie_movie_id_seq', 13, true);


--
-- Name: person_person_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.person_person_id_seq', 4, true);


--
-- Name: reply_reaction_reply_reaction_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.reply_reaction_reply_reaction_id_seq', 7, true);


--
-- Name: reply_reply_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.reply_reply_id_seq', 4, true);


--
-- Name: review_reaction_review_reaction_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.review_reaction_review_reaction_id_seq', 7, true);


--
-- Name: review_review_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.review_review_id_seq', 4, true);


--
-- Name: statistic_statistic_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.statistic_statistic_id_seq', 1, false);


--
-- Name: worker_worker_id_seq; Type: SEQUENCE SET; Schema: reviewer; Owner: -
--

SELECT pg_catalog.setval('reviewer.worker_worker_id_seq', 40, true);


--
-- Name: genre genre_genre_name_key; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.genre
    ADD CONSTRAINT genre_genre_name_key UNIQUE (genre_name);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (genre_id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (movie_id);


--
-- Name: person person_email_address_key; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.person
    ADD CONSTRAINT person_email_address_key UNIQUE (email_address);


--
-- Name: person person_person_name_key; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.person
    ADD CONSTRAINT person_person_name_key UNIQUE (person_name);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (person_id);


--
-- Name: reply reply_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply
    ADD CONSTRAINT reply_pkey PRIMARY KEY (reply_id);


--
-- Name: reply_reaction reply_reaction_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply_reaction
    ADD CONSTRAINT reply_reaction_pkey PRIMARY KEY (reply_reaction_id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (review_id);


--
-- Name: review_reaction review_reaction_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review_reaction
    ADD CONSTRAINT review_reaction_pkey PRIMARY KEY (review_reaction_id);


--
-- Name: statistic statistic_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.statistic
    ADD CONSTRAINT statistic_pkey PRIMARY KEY (statistic_id);


--
-- Name: worker worker_pkey; Type: CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.worker
    ADD CONSTRAINT worker_pkey PRIMARY KEY (worker_id);


--
-- Name: movie_with_workers _RETURN; Type: RULE; Schema: reviewer; Owner: -
--

CREATE OR REPLACE VIEW reviewer.movie_with_workers AS
 SELECT m.movie_id,
    m.movie_name,
    m.release_date,
    EXTRACT(year FROM m.release_date) AS release_year,
    string_agg((mw.movie_worker_position)::text, ' / '::text ORDER BY (mw.movie_worker_position)::text) AS positions,
    w.worker_id,
    w.worker_name
   FROM ((reviewer.movie m
     JOIN reviewer.movie_worker_bridge mw ON ((m.movie_id = mw.movie_id)))
     JOIN reviewer.worker w ON ((mw.worker_id = w.worker_id)))
  GROUP BY m.movie_id, w.worker_id;


--
-- Name: movie_genre_bridge movie_genre_bridge_genre_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.movie_genre_bridge
    ADD CONSTRAINT movie_genre_bridge_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES reviewer.genre(genre_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: movie_genre_bridge movie_genre_bridge_movie_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.movie_genre_bridge
    ADD CONSTRAINT movie_genre_bridge_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES reviewer.movie(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: movie_worker_bridge movie_worker_bridge_movie_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.movie_worker_bridge
    ADD CONSTRAINT movie_worker_bridge_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES reviewer.movie(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: movie_worker_bridge movie_worker_bridge_worker_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.movie_worker_bridge
    ADD CONSTRAINT movie_worker_bridge_worker_id_fkey FOREIGN KEY (worker_id) REFERENCES reviewer.worker(worker_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reply reply_person_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply
    ADD CONSTRAINT reply_person_id_fkey FOREIGN KEY (person_id) REFERENCES reviewer.person(person_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reply_reaction reply_reaction_person_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply_reaction
    ADD CONSTRAINT reply_reaction_person_id_fkey FOREIGN KEY (person_id) REFERENCES reviewer.person(person_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reply_reaction reply_reaction_reply_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply_reaction
    ADD CONSTRAINT reply_reaction_reply_id_fkey FOREIGN KEY (reply_id) REFERENCES reviewer.reply(reply_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: reply reply_review_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.reply
    ADD CONSTRAINT reply_review_id_fkey FOREIGN KEY (review_id) REFERENCES reviewer.review(review_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: review review_movie_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review
    ADD CONSTRAINT review_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES reviewer.movie(movie_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: review review_person_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review
    ADD CONSTRAINT review_person_id_fkey FOREIGN KEY (person_id) REFERENCES reviewer.person(person_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: review_reaction review_reaction_person_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review_reaction
    ADD CONSTRAINT review_reaction_person_id_fkey FOREIGN KEY (person_id) REFERENCES reviewer.person(person_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: review_reaction review_reaction_review_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.review_reaction
    ADD CONSTRAINT review_reaction_review_id_fkey FOREIGN KEY (review_id) REFERENCES reviewer.review(review_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: statistic statistic_person_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.statistic
    ADD CONSTRAINT statistic_person_id_fkey FOREIGN KEY (person_id) REFERENCES reviewer.person(person_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: statistic statistic_review_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.statistic
    ADD CONSTRAINT statistic_review_id_fkey FOREIGN KEY (review_id) REFERENCES reviewer.review(review_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: statistic statistic_worker_id_fkey; Type: FK CONSTRAINT; Schema: reviewer; Owner: -
--

ALTER TABLE ONLY reviewer.statistic
    ADD CONSTRAINT statistic_worker_id_fkey FOREIGN KEY (worker_id) REFERENCES reviewer.worker(worker_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: SCHEMA reviewer; Type: ACL; Schema: -; Owner: -
--

GRANT USAGE ON SCHEMA reviewer TO reviewer_user;


--
-- Name: TABLE genre; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.genre TO reviewer_user;


--
-- Name: TABLE movie; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.movie TO reviewer_user;


--
-- Name: TABLE movie_genre_bridge; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.movie_genre_bridge TO reviewer_user;


--
-- Name: TABLE movie_with_genres; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.movie_with_genres TO reviewer_user;


--
-- Name: TABLE movie_with_workers; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.movie_with_workers TO reviewer_user;


--
-- Name: TABLE movie_worker_bridge; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.movie_worker_bridge TO reviewer_user;


--
-- Name: TABLE person; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,DELETE,UPDATE ON TABLE reviewer.person TO reviewer_user;


--
-- Name: TABLE reply; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE reviewer.reply TO reviewer_user;


--
-- Name: TABLE reply_reaction; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,INSERT,DELETE ON TABLE reviewer.reply_reaction TO reviewer_user;


--
-- Name: TABLE review; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE reviewer.review TO reviewer_user;


--
-- Name: TABLE reply_with_review; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.reply_with_review TO reviewer_user;


--
-- Name: TABLE review_reaction; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,INSERT,DELETE ON TABLE reviewer.review_reaction TO reviewer_user;


--
-- Name: TABLE review_with_person_and_movie; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.review_with_person_and_movie TO reviewer_user;


--
-- Name: TABLE statistic; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT,INSERT,DELETE ON TABLE reviewer.statistic TO reviewer_user;


--
-- Name: TABLE worker; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.worker TO reviewer_user;


--
-- Name: TABLE statistic_with_object; Type: ACL; Schema: reviewer; Owner: -
--

GRANT SELECT ON TABLE reviewer.statistic_with_object TO reviewer_user;


--
-- PostgreSQL database dump complete
--

\unrestrict 9XGyodjbUIjc9ZHg5kwwX3Z5DHTTwW1g6RuSmV3j7JEufqRRlfcXRl7AAFSIGKF


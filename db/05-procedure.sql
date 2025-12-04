CREATE OR REPLACE PROCEDURE reviewer.generate_person_statistics(p_person_id INTEGER) AS $$
    DELETE FROM reviewer.statistic
    WHERE person_id = p_person_id;

    -- most viewed director
    INSERT INTO reviewer.statistic (statistic_type, person_id, worker_id)
    SELECT 'most_reviewed_director', p_person_id, worker_id FROM (
        SELECT mw.worker_id, COUNT(*) AS num_reviewed
        FROM reviewer.review r
        LEFT OUTER JOIN reviewer.movie m ON r.movie_id = m.movie_id
        LEFT OUTER JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
        WHERE r.person_id = p_person_id
        AND mw.movie_worker_position = 'Director'
        GROUP BY mw.worker_id
        ORDER BY num_reviewed DESC, mw.worker_id
        LIMIT 1
    );

    -- highest rated director
    INSERT INTO reviewer.statistic (statistic_type, person_id, worker_id)
    SELECT 'highest_rated_director', p_person_id, worker_id FROM (
        SELECT mw.worker_id, AVG(r.review_score) AS average_rating
        FROM reviewer.review r
        LEFT OUTER JOIN reviewer.movie m ON r.movie_id = m.movie_id
        LEFT OUTER JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
        WHERE r.person_id = p_person_id
        AND mw.movie_worker_position = 'Director'
        GROUP BY mw.worker_id
        ORDER BY average_rating DESC, mw.worker_id
        LIMIT 1
    );

    -- most controversial review
    INSERT INTO reviewer.statistic (statistic_type, person_id, review_id)
    SELECT 'most_controversial_review', p_person_id, review_id FROM (
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
$$ LANGUAGE SQL;
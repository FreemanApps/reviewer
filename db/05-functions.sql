CREATE OR REPLACE FUNCTION reviewer.review_with_reaction_type (p_review_reaction_type reaction_type, p_current_person_id INTEGER)
RETURNS TABLE(review_id INTEGER, has_reacted INTEGER, reaction_count INTEGER) AS $$
    SELECT
    r.review_id
    ,COUNT(*) FILTER (WHERE rr.review_reaction_type = p_review_reaction_type AND rr.person_id = p_current_person_id) has_reacted
    ,COUNT(*) FILTER (WHERE rr.review_reaction_type = p_review_reaction_type) reaction_count
    FROM reviewer.review r
    LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
    GROUP BY r.review_id
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION reviewer.review_with_reactions (p_current_person_id INTEGER)
RETURNS TABLE(review_id INTEGER, review_score INTEGER, review_content TEXT, review_date TEXT, person_id INTEGER, person_name TEXT, has_liked INTEGER, likes INTEGER, has_disliked INTEGER, dislikes INTEGER) AS $$
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
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION reviewer.reply_with_reaction_type (p_reply_reaction_type reaction_type, p_current_person_id INTEGER)
RETURNS TABLE(reply_id INTEGER, has_reacted INTEGER, reaction_count INTEGER) AS $$
    SELECT
    r.reply_id
    ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = p_reply_reaction_type AND rr.person_id = p_current_person_id) has_reacted
    ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = p_reply_reaction_type) reaction_count
    FROM reviewer.reply r
    LEFT OUTER JOIN reviewer.reply_reaction rr ON r.reply_id = rr.reply_id
    GROUP BY r.reply_id
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION reviewer.reply_with_reactions (p_current_person_id INTEGER)
RETURNS TABLE (reply_id INTEGER, reply_content TEXT, reply_timestamp TIMESTAMP WITH TIME ZONE, reply_date TEXT, person_id INTEGER, person_name TEXT, review_id INTEGER, has_liked INTEGER, likes INTEGER, has_disliked INTEGER, dislikes INTEGER) AS $$
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
$$ LANGUAGE SQL;
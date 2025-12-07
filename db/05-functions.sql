/*

CREATE OR REPLACE VIEW reviewer.review_with_reactions
AS
SELECT;

CREATE OR REPLACE VIEW reviewer.reply_with_reactions
AS
SELECT;

CREATE FUNCTION sum_n_product_with_tab (x int)
RETURNS TABLE(sum int, product int) AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;

*/
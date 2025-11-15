from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import psycopg

from ..services import shared

router = APIRouter()

@router.get("/review/{review_id}", response_class=HTMLResponse)
async def get_review(request: Request, review_id: int):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT
                            r.review_score
                            ,r.review_content
                            ,r.review_timestamp AT TIME ZONE 'America/New_York'
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
                            WHERE r.review_id = %s
                            GROUP BY r.review_id, p.person_id
                        ''', (review_id,))
            review_details = cur.fetchone()

            cur.execute('''
                            SELECT
                            r.reply_content
                            ,r.reply_timestamp AT TIME ZONE 'America/New_York'
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'dislike') dislikes
                            FROM reviewer.reply r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.reply_reaction rr ON r.reply_id = rr.reply_id
                            WHERE r.review_id = %s
                            GROUP BY r.reply_id, p.person_id
                            ORDER BY r.reply_timestamp                        
                        ''', (review_id,))
            replies = cur.fetchall()
    
    return shared.templates.TemplateResponse(request=request, name="review.jinja", context={"review_details": review_details, "replies": replies})
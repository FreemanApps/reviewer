from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import psycopg

from ..services import shared

router = APIRouter()

@router.get("/person/{person_id}", response_class=HTMLResponse)
async def get_person(request: Request, person_id: int):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT person_name
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (person_id,))
            person_details = cur.fetchone()

            cur.execute('''
                            SELECT
                            r.review_id
                            ,r.review_score
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'HH:MI:SS AM') AS review_time
                            ,m.movie_name
                            FROM reviewer.review r
                            JOIN reviewer.movie m ON r.movie_id = m.movie_id
                            WHERE r.person_id = %s
                            ORDER BY r.review_timestamp DESC
                        ''', (person_id,))
            reviews = cur.fetchall()

            cur.execute('''
                            SELECT
                            TO_CHAR(rp.reply_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS reply_date
                            ,TO_CHAR(rp.reply_timestamp AT TIME ZONE 'America/New_York', 'HH:MI:SS AM') AS reply_time
                            ,rv.review_id
                            ,rv.review_score
                            ,TO_CHAR(rv.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
                            ,TO_CHAR(rv.review_timestamp AT TIME ZONE 'America/New_York', 'HH:MI:SS AM') AS review_time
                            ,p.person_name AS reviewerer
                            ,m.movie_name
                            FROM reviewer.reply rp
                            JOIN reviewer.review rv ON rp.review_id = rv.review_id
                            JOIN reviewer.person p ON rv.person_id = p.person_id
                            JOIN reviewer.movie m ON rv.movie_id = m.movie_id
                            WHERE rp.person_id = %s
                            ORDER BY rp.reply_timestamp DESC
                        ''', (person_id,))
            replies = cur.fetchall()
    
    return shared.templates.TemplateResponse(request=request, name="person.jinja", context={"person_details": person_details, "reviews": reviews, "replies": replies})
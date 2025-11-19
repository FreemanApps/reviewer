from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()


@router.get("/person/{person_id}", response_class=HTMLResponse)
async def get_person(request: Request, person_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT person_name
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (person_id,))
            person_details = cur.fetchone()

        with conn.cursor() as cur:
            cur.execute('''
                            SELECT
                            r.review_id
                            ,r.review_score
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
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
                            ,rv.review_id
                            ,rv.review_score
                            ,TO_CHAR(rv.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
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
    
    return shared.templates.TemplateResponse(request=request, name="person.jinja", context={"current_person_id": current_person_id, "person_details": person_details, "reviews": reviews, "replies": replies})

@router.get("/settings", response_class=HTMLResponse)
async def get_current_person(request: Request, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT person_name, email_address
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (current_person_id,))
            current_person_details = cur.fetchone()
        return shared.templates.TemplateResponse(request=request, name="settings.jinja", context={"current_person_id": current_person_id, "current_person_details": current_person_details})

@router.post("/settings", response_class=HTMLResponse)
async def update_current_person(current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    person_name = 'TODO'
    email_address = 'TODO'
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            UPDATE reviewer.person
                            SET person_name = %s, email_address = %s
                            WHERE person_id = %s
                        ''', (person_name, email_address, current_person_id,))
    # TODO

@router.delete("/settings", response_class=HTMLResponse)
async def delete_current_person(current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            DELETE person_name
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (current_person_id,))
        # TODO
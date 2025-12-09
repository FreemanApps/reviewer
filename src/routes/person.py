from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row
from fastapi.exceptions import HTTPException

from ..services import shared

class EditPersonFormData(BaseModel):
    person_name: str
    email_address: str

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
                            SELECT review_id, review_score, review_date, movie_id, movie_name
                            FROM reviewer.review_with_person_and_movie
                            WHERE person_id = %s
                            ORDER BY review_timestamp DESC
                        ''', (person_id,))
            reviews = cur.fetchall()

            cur.execute('''
                            SELECT reply_date, review_id, review_score, review_date, reviewer, movie_id, movie_name
                            FROM reviewer.reply_with_review
                            WHERE person_id = %s
                            ORDER BY reply_timestamp DESC
                        ''', (person_id,))
            replies = cur.fetchall()

            cur.execute('''
                            SELECT statistic_name, statistic_type, worker_id, worker_name, review_id, review_score, review_date, movie_id, movie_name
                            FROM reviewer.statistic_with_object
                            WHERE person_id = %s
                            ORDER BY statistic_id
                        ''', (person_id,))
            statistics = cur.fetchall()

    if not person_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)    
    return shared.templates.TemplateResponse(request=request, name="person.jinja", context={"current_person_id": current_person_id, "person_details": person_details, "reviews": reviews, "replies": replies, "statistics": statistics})

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
    return shared.templates.TemplateResponse(request=request, name="settings/settings.jinja", context={"current_person_id": current_person_id, "current_person_details": current_person_details})

@router.get("/settings/edit", response_class=HTMLResponse)
async def get_editable_current_person(request: Request, current_person_id: Annotated[int, Depends(shared.get_current_person)]):    
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT person_name, email_address
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (current_person_id,))
            current_person_details = cur.fetchone()
    return shared.templates.TemplateResponse(request=request, name="settings/edit-user-details-form.jinja", context={"current_person_id": current_person_id, "current_person_details": current_person_details})

@router.patch("/person/me", response_class=HTMLResponse)
async def update_current_person(request: Request, form_data: Annotated[EditPersonFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    person_name = form_data.person_name
    email_address = form_data.email_address
    
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            with conn.transaction():
                cur.execute('''
                                UPDATE reviewer.person
                                SET person_name = %s, email_address = %s
                                WHERE person_id = %s
                            ''', (person_name, email_address, current_person_id,))

            cur.execute('''
                            SELECT person_name, email_address
                            FROM reviewer.person
                            WHERE person_id = %s
                        ''', (current_person_id,))
            current_person_details = cur.fetchone()
    return shared.templates.TemplateResponse(request=request, name="settings/user-details.jinja", context={"current_person_id": current_person_id, "current_person_details": current_person_details})

@router.delete("/person/me")
async def delete_current_person(request: Request, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            DELETE FROM reviewer.person
                            WHERE person_id = %s
                        ''', (current_person_id,))
            
    url = request.url_for("logout")
    return RedirectResponse(url, status.HTTP_303_SEE_OTHER)

@router.patch("/person/me/statistics")
async def update_current_person_statistics(request: Request, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            CALL reviewer.generate_person_statistics(p_person_id => %s)
                        ''', (current_person_id,))
            
    url = request.url_for("get_person", person_id=current_person_id)
    return RedirectResponse(url, status.HTTP_303_SEE_OTHER)
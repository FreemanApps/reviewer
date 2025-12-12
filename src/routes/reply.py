from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row
from fastapi.exceptions import HTTPException

from ..services import shared

class ReplyFormData(BaseModel):
    reply_content: str

router = APIRouter()

@router.post("/movie/{movie_id}/review/{review_id}/reply", response_class=HTMLResponse)
async def create_reply(request: Request, movie_id: int, review_id: int, form_data: Annotated[ReplyFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    reply_content = form_data.reply_content

    # validate form details
    error = {}
    if not reply_content:
        error["reply_content"] = "Reply must be inputted"

    # if validation failed, send back new reply form with details
    if len(error) > 0:
        response = shared.templates.TemplateResponse(request=request, name="review/new-reply-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "form_data": form_data, "error": error})
        response.headers["HX-Retarget"] = "#new-reply-form"
        return response

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            # insert new reply
            with conn.transaction():
                cur.execute('''
                                INSERT INTO reviewer.reply (reply_content, person_id, review_id)
                                VALUES (%s, %s, %s)
                            ''', (reply_content, current_person_id, review_id,))
            
            # get all replies for review
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()

    # send back replies section
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})

@router.get("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/edit", response_class=HTMLResponse)
async def get_editable_reply(request: Request, movie_id: int, review_id: int, reply_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        # get reply details
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT reply_content
                            FROM reviewer.reply
                            WHERE reply_id = %s
                        ''', (reply_id,))
            reply_details = cur.fetchone()

    # if needed, send 404 error; otherwise, send edit reply form
    if not reply_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)                  
    return shared.templates.TemplateResponse(request=request, name="review/edit-reply-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "reply_id": reply_id, "reply_details": reply_details})

@router.patch("/movie/{movie_id}/review/{review_id}/reply/{reply_id}", response_class=HTMLResponse)
async def update_reply(request: Request, movie_id: int, review_id: int, reply_id: int, form_data: Annotated[ReplyFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details    
    reply_content = form_data.reply_content

    # validate form details
    error = {}
    if not reply_content:
        error["reply_content"] = "Reply must be inputted"

    # if validation failed, send back edit reply form with details
    if len(error) > 0:
        response = shared.templates.TemplateResponse(request=request, name="review/edit-reply-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "reply_id": reply_id, "form_data": form_data, "error": error})
        response.headers["HX-Retarget"] = "#edit-reply-" + str(reply_id) + "-form"
        return response

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            # determine whether current person is owner
            cur.execute('''
                            SELECT COUNT(*) AS owns_reply
                            FROM reviewer.reply
                            WHERE reply_id = %s
                            AND person_id = %s
                        ''', (reply_id, current_person_id,))
            owns_reply = cur.fetchone()[0]

            # if current person is owner, then update reply
            if owns_reply:
                with conn.transaction():
                    cur.execute('''
                                    UPDATE reviewer.reply
                                    SET reply_content = %s
                                    WHERE reply_id = %s
                                ''', (reply_content, reply_id,))
            
            # get all replies for review
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()

    # send replies section  
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})

@router.delete("/movie/{movie_id}/review/{review_id}/reply/{reply_id}", response_class=HTMLResponse)
async def delete_reply(request: Request, movie_id: int, review_id: int, reply_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            # determine whether current person is owner
            cur.execute('''
                            SELECT COUNT(*) AS owns_reply
                            FROM reviewer.reply
                            WHERE reply_id = %s
                            AND person_id = %s
                        ''', (reply_id, current_person_id,))
            owns_reply = cur.fetchone()[0]

            # if current person is owner, then delete reply
            if owns_reply:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.reply
                                    WHERE reply_id = %s
                                ''', (reply_id,))
            
            # get all replies for review
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()

    # send replies section                
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})
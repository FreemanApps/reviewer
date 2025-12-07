from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

class ReplyFormData(BaseModel):
    reply_content: str

router = APIRouter()

@router.post("/movie/{movie_id}/review/{review_id}/reply", response_class=HTMLResponse)
async def create_reply(request: Request, movie_id: int, review_id: int, form_data: Annotated[ReplyFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_content = form_data.reply_content

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                cur.execute('''
                                INSERT INTO reviewer.reply (reply_content, person_id, review_id)
                                VALUES (%s, %s, %s)
                            ''', (reply_content, current_person_id, review_id,))
            
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()
                
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})

@router.get("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/edit", response_class=HTMLResponse)
async def get_editable_reply(request: Request, movie_id: int, review_id: int, reply_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT reply_content
                            FROM reviewer.reply
                            WHERE reply_id = %s
                        ''', (reply_id,))
            reply_details = cur.fetchone()
                
    return shared.templates.TemplateResponse(request=request, name="review/edit-reply-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "reply_id": reply_id, "reply_details": reply_details})

@router.patch("/movie/{movie_id}/review/{review_id}/reply/{reply_id}", response_class=HTMLResponse)
async def update_reply(request: Request, movie_id: int, review_id: int, reply_id: int, form_data: Annotated[ReplyFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_content = form_data.reply_content

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT COUNT(*) AS owns_reply
                            FROM reviewer.reply
                            WHERE reply_id = %s
                            AND person_id = %s
                        ''', (reply_id, current_person_id,))
            owns_reply = cur.fetchone()[0]

            if owns_reply:
                with conn.transaction():
                    cur.execute('''
                                    UPDATE reviewer.reply
                                    SET reply_content = %s
                                    WHERE reply_id = %s
                                ''', (reply_content, reply_id,))
            
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()
                
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})

@router.delete("/movie/{movie_id}/review/{review_id}/reply/{reply_id}", response_class=HTMLResponse)
async def delete_reply(request: Request, movie_id: int, review_id: int, reply_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT COUNT(*) AS owns_reply
                            FROM reviewer.reply
                            WHERE reply_id = %s
                            AND person_id = %s
                        ''', (reply_id, current_person_id,))
            owns_reply = cur.fetchone()[0]

            if owns_reply:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.reply
                                    WHERE reply_id = %s
                                ''', (reply_id,))

            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()
                
    return shared.templates.TemplateResponse(request=request, name="review/replies-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "replies": replies})
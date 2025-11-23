from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

class ReviewReactionFormData(BaseModel):
    review_id: int
    review_reaction_type: str

class ReplyReactionFormData(BaseModel):
    reply_id: int
    reply_reaction_type: str

router = APIRouter()

@router.post("/review_reaction", response_class=HTMLResponse)
async def create_review_reaction(request: Request, form_data: Annotated[ReviewReactionFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    review_id = form_data.review_id
    review_reaction_type = form_data.review_reaction_type

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.review_reaction
                            WHERE review_reaction_type = %s
                            AND person_id = %s
                            AND review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            if not has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
                                    VALUES (%s, %s, %s)
                                ''', (review_reaction_type, current_person_id, review_id, ))
                
            cur.execute('''
                            SELECT
                            COUNT(*) FILTER (WHERE review_reaction_type = %(review_reaction_type)s AND person_id = %(current_person_id)s) has_reacted
                            ,COUNT(*) FILTER (WHERE review_reaction_type = %(review_reaction_type)s) reaction_count
                            FROM reviewer.review_reaction
                            WHERE review_id = %(review_id)s
                        ''', {"review_reaction_type": review_reaction_type, "current_person_id": current_person_id, "review_id": review_id })
            review_details = cur.fetchone()
    
    return shared.templates.TemplateResponse(request=request, name="reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "object": 'review', "object_id": review_id, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.delete("/review_reaction", response_class=HTMLResponse)
async def delete_review_reaction(request: Request, review_id: int, review_reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.review_reaction
                            WHERE review_reaction_type = %s
                            AND person_id = %s
                            AND review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            if has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.review_reaction
                                    WHERE review_reaction_type = %s
                                    AND person_id = %s
                                    AND review_id = %s
                                ''', (review_reaction_type, current_person_id, review_id, ))
                
            cur.execute('''
                            SELECT
                            COUNT(*) FILTER (WHERE review_reaction_type = %(review_reaction_type)s AND person_id = %(current_person_id)s) has_reacted
                            ,COUNT(*) FILTER (WHERE review_reaction_type = %(review_reaction_type)s) reaction_count
                            FROM reviewer.review_reaction
                            WHERE review_id = %(review_id)s
                        ''', {"review_reaction_type": review_reaction_type, "current_person_id": current_person_id, "review_id": review_id })
            review_details = cur.fetchone()
    
    return shared.templates.TemplateResponse(request=request, name="reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "object": 'review', "object_id": review_id, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.post("/reply_reaction", response_class=HTMLResponse)
async def create_reply_reaction(request: Request, form_data: Annotated[ReplyReactionFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_id = form_data.reply_id
    reply_reaction_type = form_data.reply_reaction_type
    
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.reply_reaction
                            WHERE reply_reaction_type = %s
                            AND person_id = %s
                            AND reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            if not has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
                                    VALUES (%s, %s, %s)
                                ''', (reply_reaction_type, current_person_id, reply_id, ))
                
                cur.execute('''
                                SELECT
                                COUNT(*) FILTER (WHERE reply_reaction_type = %(reply_reaction_type)s AND person_id = %(current_person_id)s) has_reacted
                                ,COUNT(*) FILTER (WHERE reply_reaction_type = %(reply_reaction_type)s) reaction_count
                                FROM reviewer.reply_reaction
                                WHERE reply_id = %(reply_id)s
                            ''', {"reply_reaction_type": reply_reaction_type, "current_person_id": current_person_id, "reply_id": reply_id })
                reply_details = cur.fetchone()

    return shared.templates.TemplateResponse(request=request, name="reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "object": 'reply', "object_id": reply_id, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})

@router.delete("/reply_reaction", response_class=HTMLResponse)
async def delete_reply_reaction(request: Request, reply_id: int, reply_reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.reply_reaction
                            WHERE reply_reaction_type = %s
                            AND person_id = %s
                            AND reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            if has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.reply_reaction
                                    WHERE reply_reaction_type = %s
                                    AND person_id = %s
                                    AND reply_id = %s
                                ''', (reply_reaction_type, current_person_id, reply_id, ))
                
                cur.execute('''
                                SELECT
                                COUNT(*) FILTER (WHERE reply_reaction_type = %(reply_reaction_type)s AND person_id = %(current_person_id)s) has_reacted
                                ,COUNT(*) FILTER (WHERE reply_reaction_type = %(reply_reaction_type)s) reaction_count
                                FROM reviewer.reply_reaction
                                WHERE reply_id = %(reply_id)s
                            ''', {"reply_reaction_type": reply_reaction_type, "current_person_id": current_person_id, "reply_id": reply_id })
                reply_details = cur.fetchone()

    return shared.templates.TemplateResponse(request=request, name="reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "object": 'reply', "object_id": reply_id, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})
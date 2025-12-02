from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

class ReactionFormData(BaseModel):
    reaction_type: str

router = APIRouter()

@router.post("/movie/{movie_id}/review/{review_id}/react", response_class=HTMLResponse)
async def create_review_reaction(request: Request, movie_id: int, review_id: int, form_data: Annotated[ReactionFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    review_reaction_type = form_data.reaction_type

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
    
    url = request.url_for("delete_review_reaction", movie_id=movie_id, review_id=review_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "url": url, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.delete("/movie/{movie_id}/review/{review_id}/react", response_class=HTMLResponse)
async def delete_review_reaction(request: Request, movie_id: int, review_id: int, reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    review_reaction_type = reaction_type

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
    
    url = request.url_for("create_review_reaction", movie_id=movie_id, review_id=review_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "url": url, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.post("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/react", response_class=HTMLResponse)
async def create_reply_reaction(request: Request, movie_id: int, review_id: int, reply_id: int, form_data: Annotated[ReactionFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_reaction_type = form_data.reaction_type
    
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

    url = request.url_for("delete_reply_reaction", movie_id=movie_id, review_id=review_id, reply_id=reply_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "url": url, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})

@router.delete("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/react", response_class=HTMLResponse)
async def delete_reply_reaction(request: Request, movie_id: int, review_id: int, reply_id: int, reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_reaction_type = reaction_type

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

    url = request.url_for("create_reply_reaction", movie_id=movie_id, review_id=review_id, reply_id=reply_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "url": url, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})
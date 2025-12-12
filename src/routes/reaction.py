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
    # grab form details
    review_reaction_type = form_data.reaction_type

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # identify whether review reaction has occurred
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.review_reaction
                            WHERE review_reaction_type = %s
                            AND person_id = %s
                            AND review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            # if not, insert review reaction
            if not has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    INSERT INTO reviewer.review_reaction (review_reaction_type, person_id, review_id)
                                    VALUES (%s, %s, %s)
                                ''', (review_reaction_type, current_person_id, review_id, ))
                
            # grab review reaction details
            cur.execute('''
                            SELECT has_reacted, reaction_count
                            FROM reviewer.review_with_reaction_type(%s, %s)
                            WHERE review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id,))
            review_details = cur.fetchone()
    
    # send review reaction form
    url = request.url_for("delete_review_reaction", movie_id=movie_id, review_id=review_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "url": url, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.delete("/movie/{movie_id}/review/{review_id}/react", response_class=HTMLResponse)
async def delete_review_reaction(request: Request, movie_id: int, review_id: int, reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    review_reaction_type = reaction_type

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # identify whether review reaction has occurred
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.review_reaction
                            WHERE review_reaction_type = %s
                            AND person_id = %s
                            AND review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            # if so, delete review reaction
            if has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.review_reaction
                                    WHERE review_reaction_type = %s
                                    AND person_id = %s
                                    AND review_id = %s
                                ''', (review_reaction_type, current_person_id, review_id, ))

            # grab review reaction details
            cur.execute('''
                            SELECT has_reacted, reaction_count
                            FROM reviewer.review_with_reaction_type(%s, %s)
                            WHERE review_id = %s
                        ''', (review_reaction_type, current_person_id, review_id,))
            review_details = cur.fetchone()

    # send review reaction form
    url = request.url_for("create_review_reaction", movie_id=movie_id, review_id=review_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": review_details["has_reacted"], "url": url, "reaction_type": review_reaction_type, "reaction_count": review_details["reaction_count"]})

@router.post("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/react", response_class=HTMLResponse)
async def create_reply_reaction(request: Request, movie_id: int, review_id: int, reply_id: int, form_data: Annotated[ReactionFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    reply_reaction_type = form_data.reaction_type
    
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # identify whether reply reaction has occurred
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.reply_reaction
                            WHERE reply_reaction_type = %s
                            AND person_id = %s
                            AND reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id, ))
            has_reacted = cur.fetchone()["has_reacted"]
            
            # if not, insert reply reaction
            if not has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    INSERT INTO reviewer.reply_reaction (reply_reaction_type, person_id, reply_id)
                                    VALUES (%s, %s, %s)
                                ''', (reply_reaction_type, current_person_id, reply_id, ))

            # grab reply reaction details
            cur.execute('''
                            SELECT has_reacted, reaction_count
                            FROM reviewer.reply_with_reaction_type(%s, %s)
                            WHERE reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id,))
            reply_details = cur.fetchone()

    # send reply reaction form
    url = request.url_for("delete_reply_reaction", movie_id=movie_id, review_id=review_id, reply_id=reply_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "url": url, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})

@router.delete("/movie/{movie_id}/review/{review_id}/reply/{reply_id}/react", response_class=HTMLResponse)
async def delete_reply_reaction(request: Request, movie_id: int, review_id: int, reply_id: int, reaction_type: str, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    reply_reaction_type = reaction_type

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # identify whether reply reaction has occurred
            cur.execute('''
                            SELECT COUNT(*) AS has_reacted
                            FROM reviewer.reply_reaction
                            WHERE reply_reaction_type = %s
                            AND person_id = %s
                            AND reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id, ))
            has_reacted = cur.fetchone()["has_reacted"]

            # if so, delete reply reaction
            if has_reacted:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.reply_reaction
                                    WHERE reply_reaction_type = %s
                                    AND person_id = %s
                                    AND reply_id = %s
                                ''', (reply_reaction_type, current_person_id, reply_id, ))

            # grab reply reaction details                
            cur.execute('''
                            SELECT has_reacted, reaction_count
                            FROM reviewer.reply_with_reaction_type(%s, %s)
                            WHERE reply_id = %s
                        ''', (reply_reaction_type, current_person_id, reply_id,))
            reply_details = cur.fetchone()

    # send reply reaction form
    url = request.url_for("create_reply_reaction", movie_id=movie_id, review_id=review_id, reply_id=reply_id)
    return shared.templates.TemplateResponse(request=request, name="review/reaction-button.jinja", context={"current_person_id": current_person_id, "has_reacted": reply_details["has_reacted"], "url": url, "reaction_type": reply_reaction_type, "reaction_count": reply_details["reaction_count"]})
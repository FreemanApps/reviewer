from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg

from ..services import shared

class ReplyFormData(BaseModel):
    reply_content: str
    review_id: int

router = APIRouter()

@router.post("/reply", response_class=HTMLResponse)
async def create_reply(request: Request, form_data: Annotated[ReplyFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    reply_content = form_data.reply_content
    review_id = form_data.review_id

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                cur.execute('''
                                INSERT INTO reviewer.reply (reply_content, person_id, review_id)
                                VALUES (%s, %s, %s) 
                            ''', (reply_content, current_person_id, review_id,))
                
            cur.execute('''
                            SELECT
                            r.reply_id
                            ,r.reply_content
                            ,TO_CHAR(r.reply_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS reply_date
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'like' AND rr.person_id = %(current_person_id)s) has_liked
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'dislike' AND rr.person_id = %(current_person_id)s) has_disliked
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'dislike') dislikes
                            FROM reviewer.reply r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.reply_reaction rr ON r.reply_id = rr.reply_id
                            WHERE r.review_id = %(review_id)s
                            GROUP BY r.reply_id, p.person_id
                            ORDER BY r.reply_timestamp                        
                        ''', {"current_person_id": current_person_id, "review_id": review_id})
            replies = cur.fetchall()
                
    return shared.templates.TemplateResponse(request=request, name="replies.jinja", context={"current_person_id": current_person_id, "replies": replies, "review_id": review_id})        
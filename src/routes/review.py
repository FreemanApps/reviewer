from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

class ReviewFormData(BaseModel):
    review_score: int
    review_content: str

router = APIRouter()

@router.get("/movie/{movie_id}/review/new", response_class=HTMLResponse)
async def get_new_review_form(request: Request, movie_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    return shared.templates.TemplateResponse(request=request, name="review/new-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id})

@router.post("/movie/{movie_id}/review")
async def create_review(request: Request, movie_id: int, form_data: Annotated[ReviewFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    review_content = form_data.review_content
    review_score = form_data.review_score

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                cur.execute('''
                                INSERT INTO reviewer.review (review_score, review_content, person_id, movie_id)
                                VALUES (%s, %s, %s, %s)
                                RETURNING review_id
                            ''', (review_score, review_content, current_person_id, movie_id,))
                review_id = str(cur.fetchone()[0])

    url = request.url_for("get_review", movie_id=movie_id, review_id=review_id)
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    return response


@router.get("/movie/{movie_id}/review/{review_id}", response_class=HTMLResponse)
async def get_review(request: Request, movie_id: int, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                            r.review_id
                            ,r.review_score
                            ,r.review_content
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like' AND rr.person_id = %(current_person_id)s) has_liked
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike' AND rr.person_id = %(current_person_id)s) has_disliked
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
                            WHERE r.review_id = %(review_id)s
                            GROUP BY r.review_id, p.person_id
                        ''', {"current_person_id": current_person_id, "review_id": review_id})
            review_details = cur.fetchone()

        with conn.cursor() as cur:
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
    
    return shared.templates.TemplateResponse(request=request, name="review/review.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_details": review_details, "replies": replies})

@router.get("/movie/{movie_id}/review/{review_id}/edit", response_class=HTMLResponse)
async def get_editable_review(request: Request, movie_id: int, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT review_score, review_content
                            FROM reviewer.review
                            WHERE review_id = %s
                        ''', (review_id,))
            review_details = cur.fetchone()
                
    return shared.templates.TemplateResponse(request=request, name="review/edit-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "review_details": review_details})

@router.patch("/movie/{movie_id}/review/{review_id}", response_class=HTMLResponse)
async def update_review(request: Request, movie_id: int, review_id: int, form_data: Annotated[ReviewFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    review_score = form_data.review_score
    review_content = form_data.review_content

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT COUNT(*) AS owns_review
                            FROM reviewer.review
                            WHERE review_id = %s
                            AND person_id = %s
                        ''', (review_id, current_person_id,))
            owns_review = cur.fetchone()[0]

            if owns_review:
                with conn.transaction():
                    cur.execute('''
                                    UPDATE reviewer.review
                                    SET review_score = %s, review_content = %s
                                    WHERE review_id = %s
                                ''', (review_score, review_content, review_id,))

        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                            r.review_id
                            ,r.review_score
                            ,r.review_content
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like' AND rr.person_id = %(current_person_id)s) has_liked
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike' AND rr.person_id = %(current_person_id)s) has_disliked
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
                            WHERE r.review_id = %(review_id)s
                            GROUP BY r.review_id, p.person_id
                        ''', {"current_person_id": current_person_id, "review_id": review_id})
            review_details = cur.fetchone()
                
    return shared.templates.TemplateResponse(request=request, name="review/review-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_details": review_details})

@router.delete("/movie/{movie_id}/review/{review_id}")
async def delete_review(request: Request, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT COUNT(*) AS owns_review
                            FROM reviewer.review
                            WHERE review_id = %s
                            AND person_id = %s
                        ''', (review_id, current_person_id,))
            owns_review = cur.fetchone()[0]

            if owns_review:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.review
                                    WHERE review_id = %s
                                ''', (review_id,))

    url = request.url_for("get_movies")
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    return response
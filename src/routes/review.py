from pydantic import BaseModel
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row
from fastapi.exceptions import HTTPException

from ..services import shared

class ReviewFormData(BaseModel):
    review_score: str
    review_content: str

router = APIRouter()

@router.get("/movie/{movie_id}/review/new", response_class=HTMLResponse)
async def get_new_review_form(request: Request, movie_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # send to new review form
    return shared.templates.TemplateResponse(request=request, name="review/new-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id})

@router.post("/movie/{movie_id}/review")
async def create_review(request: Request, movie_id: int, form_data: Annotated[ReviewFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    review_content = form_data.review_content if form_data.review_content else None
    review_score = form_data.review_score if form_data.review_score else None

    # validate form details
    error = {}
    if not review_content and not review_score:
        error["form"] = "Review or score must be inputted"
    elif review_score:
        try:
            review_score = int(review_score)
            if review_score < 1 or review_score > 10:
                error["review_score"] = "Review score must be between 1 and 10"
        except:
            error["review_score"] = "Review score must be a number"

    # if validation failed, send back new review form page with details
    if len(error) > 0:
        response = shared.templates.TemplateResponse(request=request, name="review/new-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "form_data": form_data, "error": error})
        response.headers["HX-Push-Url"] = "false"
        return response

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            with conn.transaction():
                # insert new review
                cur.execute('''
                                INSERT INTO reviewer.review (review_score, review_content, person_id, movie_id)
                                VALUES (%s, %s, %s, %s)
                                RETURNING review_id
                            ''', (review_score, review_content, current_person_id, movie_id,))
                review_id = str(cur.fetchone()[0])

    # send to review page
    url = request.url_for("get_review", movie_id=movie_id, review_id=review_id)
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    return response


@router.get("/movie/{movie_id}/review/{review_id}", response_class=HTMLResponse)
async def get_review(request: Request, movie_id: int, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        # get review details
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT review_id, review_score, review_content, review_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.review_with_reactions(%s)
                            WHERE review_id = %s
                        ''', (current_person_id, review_id,))
            review_details = cur.fetchone()

        # get all replies for review
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT reply_id, reply_content, reply_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.reply_with_reactions(%s)
                            WHERE review_id = %s
                            ORDER BY reply_timestamp
                        ''', (current_person_id, review_id,))
            replies = cur.fetchall()

    # if needed, send 404 error; otherwise, send review page
    if not review_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)      
    return shared.templates.TemplateResponse(request=request, name="review/review.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_details": review_details, "replies": replies})

@router.get("/movie/{movie_id}/review/{review_id}/edit", response_class=HTMLResponse)
async def get_editable_review(request: Request, movie_id: int, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            # get review details
            cur.execute('''
                            SELECT review_score, review_content
                            FROM reviewer.review
                            WHERE review_id = %s
                        ''', (review_id,))
            review_details = cur.fetchone()

    # if needed, send 404 error; otherwise, send edit review form
    if not review_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)                  
    return shared.templates.TemplateResponse(request=request, name="review/edit-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "review_details": review_details})

@router.patch("/movie/{movie_id}/review/{review_id}", response_class=HTMLResponse)
async def update_review(request: Request, movie_id: int, review_id: int, form_data: Annotated[ReviewFormData, Form()], current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    # grab form details
    review_content = form_data.review_content if form_data.review_content else None
    review_score = form_data.review_score if form_data.review_score else None

    # validate form details
    error = {}
    if not review_content and not review_score:
        error["form"] = "Review or score must be inputted"
    elif review_score:
        try:
            review_score = int(review_score)
            if review_score < 1 or review_score > 10:
                error["review_score"] = "Review score must be between 1 and 10"
        except:
            error["review_score"] = "Review score must be a number"

    # if validation failed, send back edit review form with details
    if len(error) > 0:
        response = shared.templates.TemplateResponse(request=request, name="review/edit-review-form.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_id": review_id, "form_data": form_data, "error": error})
        response.headers["HX-Retarget"] = "#edit-review-form"
        return response

    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            # determine whether current person is owner
            cur.execute('''
                            SELECT COUNT(*) AS owns_review
                            FROM reviewer.review
                            WHERE review_id = %s
                            AND person_id = %s
                        ''', (review_id, current_person_id,))
            owns_review = cur.fetchone()[0]

            # if current person is owner, then update review
            if owns_review:
                with conn.transaction():
                    cur.execute('''
                                    UPDATE reviewer.review
                                    SET review_score = %s, review_content = %s
                                    WHERE review_id = %s
                                ''', (review_score, review_content, review_id,))

        # get review details
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''                        
                            SELECT review_id, review_score, review_content, review_date, person_id, person_name, has_liked, likes, has_disliked, dislikes
                            FROM reviewer.review_with_reactions(%s)
                            WHERE review_id = %s
                        ''', (current_person_id, review_id,))
            review_details = cur.fetchone()

    # send review section                
    return shared.templates.TemplateResponse(request=request, name="review/review-section.jinja", context={"current_person_id": current_person_id, "movie_id": movie_id, "review_details": review_details})

@router.delete("/movie/{movie_id}/review/{review_id}")
async def delete_review(request: Request, review_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            # determine whether current person is owner
            cur.execute('''
                            SELECT COUNT(*) AS owns_review
                            FROM reviewer.review
                            WHERE review_id = %s
                            AND person_id = %s
                        ''', (review_id, current_person_id,))
            owns_review = cur.fetchone()[0]

            # if current person is owner, then delete review
            if owns_review:
                with conn.transaction():
                    cur.execute('''
                                    DELETE FROM reviewer.review
                                    WHERE review_id = %s
                                ''', (review_id,))

    # send to home page
    url = request.url_for("get_movies")
    response = RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    return response
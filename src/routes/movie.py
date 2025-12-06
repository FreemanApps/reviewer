from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_movies(request: Request, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT movie_id, movie_name, EXTRACT(year FROM release_date) AS release_year
                            FROM reviewer.movie
                            ORDER BY movie_name, release_date
                        ''')
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="home.jinja", context={"current_person_id": current_person_id, "movies": movies})

@router.get("/movie/{movie_id}", response_class=HTMLResponse)
async def get_movie(request: Request, movie_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT movie_id, movie_name, TO_CHAR(release_date, 'DD Mon YYYY') AS release_year
                            FROM reviewer.movie
                            WHERE movie_id = %s
                        ''', (movie_id,))
            movie_details = cur.fetchone()

            cur.execute('''
                            SELECT ROUND(AVG(review_score), 2) AS average_review_score
                            FROM reviewer.review
                            WHERE movie_id = %s
                        ''', (movie_id,))
            reviews_details = cur.fetchone()

        with conn.cursor() as cur:
            cur.execute('''
                            SELECT worker_id, worker_name, positions
                            FROM reviewer.movie_with_workers
                            WHERE movie_id = %s
                            ORDER BY worker_name, positions
                        ''', (movie_id,))
            workers = cur.fetchall()

            cur.execute('''
                            SELECT genre_id, genre_name
                            FROM reviewer.movie_with_genres
                            WHERE movie_id = %s
                            ORDER BY genre_name
                        ''', (movie_id,))
            genres = cur.fetchall()

            # TODO
            cur.execute('''
                            SELECT
                            r.review_id
                            ,r.review_score
                            ,TO_CHAR(r.review_timestamp AT TIME ZONE 'America/New_York', 'DD Mon YYYY') AS review_date
                            ,p.person_name AS reviewer
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            WHERE r.movie_id = %s
                            ORDER BY r.review_timestamp DESC
                        ''', (movie_id,))
            reviews = cur.fetchall()

    return shared.templates.TemplateResponse(request=request, name="movie.jinja", context={"current_person_id": current_person_id, "movie_details": movie_details, "workers": workers, "genres": genres, "reviews_details": reviews_details, "reviews": reviews})
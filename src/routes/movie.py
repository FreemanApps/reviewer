from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()

@router.get("/movie/{movie_id}", response_class=HTMLResponse)
async def get_movie(request: Request, movie_id: int):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT movie_name, TO_CHAR(release_date, 'DD Mon YYYY') AS release_year
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
                            SELECT mw.movie_worker_position AS worker_position, w.worker_id, w.worker_name
                            FROM reviewer.movie_worker_bridge mw
                            JOIN reviewer.worker w ON mw.worker_id = w.worker_id
                            WHERE mw.movie_id = %s
                            ORDER BY mw.movie_worker_position, w.worker_name
                        ''', (movie_id,))
            workers = cur.fetchall()

            cur.execute('''
                            SELECT g.genre_id, g.genre_name
                            FROM reviewer.movie_genre_bridge mg
                            JOIN reviewer.genre g ON mg.genre_id = g.genre_id
                            WHERE mg.movie_id = %s
                            ORDER BY g.genre_name
                        ''', (movie_id,))
            genres = cur.fetchall()

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

    return shared.templates.TemplateResponse(request=request, name="movie.jinja", context={"movie_details": movie_details, "workers": workers, "genres": genres, "reviews_details": reviews_details, "reviews": reviews})
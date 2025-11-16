from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()

@router.get("/genre/{genre_id}", response_class=HTMLResponse)
async def get_genre(request: Request, genre_id: int):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT genre_name
                            FROM reviewer.genre
                            WHERE genre_id = %s
                        ''', (genre_id,))
            genre_details = cur.fetchone()

        with conn.cursor() as cur:
            cur.execute('''
                            SELECT m.movie_id, m.movie_name, EXTRACT(year FROM m.release_date) AS release_year
                            FROM reviewer.movie m
                            JOIN reviewer.movie_genre_bridge mg ON m.movie_id = mg.movie_id
                            WHERE mg.genre_id = %s
                            ORDER BY m.movie_name
                        ''', (genre_id,))
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="genre.jinja", context={"genre_details": genre_details, "movies": movies})
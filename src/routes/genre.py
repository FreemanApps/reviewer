from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row
from fastapi.exceptions import HTTPException

from ..services import shared

router = APIRouter()

@router.get("/genre/{genre_id}", response_class=HTMLResponse)
async def get_genre(request: Request, genre_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
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
                            SELECT movie_id, movie_name, release_year
                            FROM reviewer.movie_with_genres
                            WHERE genre_id = %s
                            ORDER BY movie_name
                        ''', (genre_id,))
            movies = cur.fetchall()

    if not genre_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return shared.templates.TemplateResponse(request=request, name="genre.jinja", context={"current_person_id": current_person_id, "genre_details": genre_details, "movies": movies})
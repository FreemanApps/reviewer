from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()

@router.get("/worker/{worker_id}", response_class=HTMLResponse)
async def get_worker(request: Request, worker_id: int):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT worker_name
                            FROM reviewer.worker
                            WHERE worker_id = %s
                        ''', (worker_id,))
            worker_details = cur.fetchone()

        with conn.cursor() as cur:
            cur.execute('''
                            SELECT
                            m.movie_id
                            ,m.movie_name
                            ,EXTRACT(year FROM m.release_date) AS release_year
                            ,STRING_AGG(mw.movie_worker_position, '/' ORDER BY mw.movie_worker_position) AS positions
                            FROM reviewer.movie m
                            JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
                            WHERE mw.worker_id = %s
                            GROUP BY m.movie_id
                            ORDER BY m.release_date
                        ''', (worker_id,))
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="worker.jinja", context={"worker_details": worker_details, "movies": movies})
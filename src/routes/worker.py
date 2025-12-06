from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
import psycopg
from psycopg.rows import dict_row

from ..services import shared

router = APIRouter()

@router.get("/worker/{worker_id}", response_class=HTMLResponse)
async def get_worker(request: Request, worker_id: int, current_person_id: Annotated[int, Depends(shared.get_current_person)]):
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
                            movie_id
                            ,movie_name
                            ,release_year
                            ,positions
                            FROM reviewer.movie_with_workers
                            WHERE worker_id = %s
                            ORDER BY release_date
                        ''', (worker_id,))
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="worker.jinja", context={"current_person_id": current_person_id, "worker_details": worker_details, "movies": movies})
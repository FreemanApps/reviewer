import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import psycopg

load_dotenv()
database_url = os.getenv("DATABASE_URL")
app = FastAPI()
app.mount("/public", StaticFiles(directory="src/public"), name="public")
templates = Jinja2Templates(directory="src/templates")

@app.get("/favicon.ico", response_class=RedirectResponse, status_code=301)
def get_icon():
    return "/public/favicon.ico"

@app.get("/", response_class=HTMLResponse)
async def get_movies(request: Request):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT movie_id, movie_name, EXTRACT(year FROM release_date) AS release_year
                            FROM reviewer.movie
                            ORDER BY movie_name, release_date
                        ''')
            movies = cur.fetchall()
    return templates.TemplateResponse(request=request, name="home.jinja", context={"movies": movies})

@app.get("/movie/{movie_id}", response_class=HTMLResponse)
async def get_movie(request: Request, movie_id: int):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT movie_name, TO_CHAR(release_date, 'DD Mon YYYY')
                            FROM reviewer.movie
                            WHERE movie_id = %s
                        ''', (movie_id,))
            movie_details = cur.fetchone()

            cur.execute('''
                            SELECT mw.movie_worker_position AS worker_position, w.worker_id, w.worker_name
                            FROM reviewer.movie m
                            JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
                            JOIN reviewer.worker w ON mw.worker_id = w.worker_id
                            WHERE m.movie_id = %s
                            ORDER BY mw.movie_worker_position, w.worker_name
                        ''', (movie_id,))
            workers = cur.fetchall()

            cur.execute('''
                            SELECT g.genre_id, g.genre_name
                            FROM reviewer.movie m
                            JOIN reviewer.movie_genre_bridge mg ON m.movie_id = mg.movie_id
                            JOIN reviewer.genre g ON mg.genre_id = g.genre_id
                            WHERE m.movie_id = %s
                            ORDER BY g.genre_name
                        ''', (movie_id,))
            genres = cur.fetchall()
    return templates.TemplateResponse(request=request, name="movie.jinja", context={"movie_details": movie_details, "workers": workers, "genres": genres})

@app.get("/worker/{worker_id}", response_class=HTMLResponse)
async def get_worker(request: Request, worker_id: int):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT worker_name
                            FROM reviewer.worker
                            WHERE worker_id = %s
                        ''', (worker_id,))
            worker_details = cur.fetchone()

            cur.execute('''
                            SELECT m.movie_id, m.movie_name, EXTRACT(year FROM m.release_date) AS release_year, STRING_AGG(mw.movie_worker_position, '/' ORDER BY mw.movie_worker_position) AS positions
                            FROM reviewer.movie m
                            JOIN reviewer.movie_worker_bridge mw ON m.movie_id = mw.movie_id
                            JOIN reviewer.worker w ON mw.worker_id = w.worker_id
                            WHERE w.worker_id = %s
                            GROUP BY m.movie_id
                            ORDER BY m.release_date
                        ''', (worker_id,))
            movies = cur.fetchall()
    return templates.TemplateResponse(request=request, name="worker.jinja", context={"worker_details": worker_details, "movies": movies})

@app.get("/genre/{genre_id}", response_class=HTMLResponse)
async def get_genre(request: Request, genre_id: int):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT genre_name
                            FROM reviewer.genre
                            WHERE genre_id = %s
                        ''', (genre_id,))
            genre_details = cur.fetchone()

            cur.execute('''
                            SELECT m.movie_id, m.movie_name, EXTRACT(year FROM m.release_date) AS release_year
                            FROM reviewer.movie m
                            JOIN reviewer.movie_genre_bridge mg ON m.movie_id = mg.movie_id
                            JOIN reviewer.genre g ON mg.genre_id = g.genre_id
                            WHERE g.genre_id = %s
                            ORDER BY m.movie_name
                        ''', (genre_id,))
            movies = cur.fetchall()
    return templates.TemplateResponse(request=request, name="genre.jinja", context={"genre_details": genre_details, "movies": movies})
            

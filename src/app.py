from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
import psycopg

from .services import shared
from .routes import genre, movie, person, review, worker

# set up app
app = FastAPI()
app.add_middleware(GZipMiddleware)
app.mount("/public", StaticFiles(directory="src/public"), name="public")

@app.get("/favicon.ico", response_class=RedirectResponse, status_code=301)
def get_icon():
    return "/public/favicon.ico"

@app.get("/", response_class=HTMLResponse)
async def get_movies(request: Request):
    with psycopg.connect(shared.database_url, cursor_factory=shared.LoggingCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT movie_id, movie_name, EXTRACT(year FROM release_date) AS release_year
                            FROM reviewer.movie
                            ORDER BY movie_name, release_date
                        ''')
            movies = cur.fetchall()
    return shared.templates.TemplateResponse(request=request, name="home.jinja", context={"movies": movies})

app.include_router(genre.router)
app.include_router(movie.router)
app.include_router(person.router)
app.include_router(review.router)
app.include_router(worker.router)
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
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') - COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') ordering
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
                            WHERE r.movie_id = %s
                            GROUP BY r.review_id, p.person_id
                            ORDER BY ordering DESC, r.review_date DESC
                        ''', (movie_id,))
            reviews = cur.fetchall()

    return templates.TemplateResponse(request=request, name="movie.jinja", context={"movie_details": movie_details, "workers": workers, "genres": genres, "reviews": reviews})

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
                            WHERE mg.genre_id = %s
                            ORDER BY m.movie_name
                        ''', (genre_id,))
            movies = cur.fetchall()
    return templates.TemplateResponse(request=request, name="genre.jinja", context={"genre_details": genre_details, "movies": movies})
            
@app.get("/review/{review_id}", response_class=HTMLResponse)
async def get_review(request: Request, review_id: int):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                            SELECT
                            r.review_score
                            ,r.review_content
                            ,r.review_date AT TIME ZONE 'America/New_York'
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.review_reaction_type = 'dislike') dislikes
                            FROM reviewer.review r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.review_reaction rr ON r.review_id = rr.review_id
                            WHERE r.review_id = %s
                            GROUP BY r.review_id, p.person_id
                        ''', (review_id,))
            review_details = cur.fetchall()

            cur.execute('''
                            SELECT
                            r.reply_content
                            ,r.reply_date AT TIME ZONE  'America/New_York'
                            ,p.person_id
                            ,p.person_name
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'like') likes
                            ,COUNT(*) FILTER (WHERE rr.reply_reaction_type = 'dislike') dislikes
                            FROM reviewer.reply r
                            JOIN reviewer.person p ON r.person_id = p.person_id
                            LEFT OUTER JOIN reviewer.reply_reaction rr ON r.reply_id = rr.reply_id
                            WHERE r.review_id = %s
                            GROUP BY r.reply_id, p.person_id
                            ORDER BY r.reply_date                        
                        ''', (review_id,))
            replies = cur.fetchall()
    
    return templates.TemplateResponse(request=request, name="review.jinja", context={"review_details": review_details, "replies": replies})

@app.get("/person/{person_id}", response_class=HTMLResponse)
async def get_person(request: Request, person_id: int):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute()
            person_details = cur.fetchall()

            cur.execute()
            reviews = cur.fetchall()

            cur.execute()
            replies = cur.fetchall()
    
    return templates.TemplateResponse(request=request, name="person.jinja", context={"person_details": person_details, "reviews": reviews, "replies": replies})